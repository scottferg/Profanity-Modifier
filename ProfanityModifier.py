# Copyright (c) 2009, Scott Ferguson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the software nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY SCOTT FERGUSON ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SCOTT FERGUSON BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from waveapi import events
from waveapi import model
from waveapi import robot
from google.appengine.ext import db

from ProfanityDatabase import ProfaneWord

def OnContentCreated( properties, context ):
    """Called whenever a new wavelet or blip is created"""
    blip = context.GetBlipById( properties['blipId'] )
    contents = blip.GetDocument( ).GetText( )

    # Do not try to learn a term if it wasn't the explicit blip
    if contents.find( 'LEARN/' ) == 0:
        if not SpecifyFilter( contents ):
            root_wavelet = context.GetRootWavelet( )
            root_wavelet.CreateBlip( ).GetDocument( ).SetText( "Sorry, but I already know that word." )
    else:
        ReplaceProfanity( contents, blip )

def ReplaceProfanity( contents, blip ):
    """Replace each profane word with it's politically correct alternative"""
    # Only update the blip if the content has actually been modified
    content_changed = False
    result = contents.lower( );
    # We store the entire list locally because it's easier and I don't feel
    # like working out a fancier solution
    total_word_list = db.GqlQuery( 'SELECT * FROM ProfaneWord' ) 

    for word in total_word_list:
        if word.base_word in contents.lower( ):
            result = '%s' % result.replace( word.base_word, " ".join( word.correct_word.split( ) ) )
            content_changed = True

    if content_changed:
        blip.GetDocument().SetText( result )

def SpecifyFilter( contents ):
    # v0.5.2 hotfix - Removed the LEARN/ feature to avoid further abuse
    return True

    new_words = contents.split( '/' )[1:]

    profane_word = ProfaneWord( )
    profane_word.base_word = " ".join( new_words[0].split( ) )
    profane_word.correct_word = new_words[1]
    
    # Query to see if we already have this word
    matched_words = db.GqlQuery( 'SELECT * FROM ProfaneWord WHERE base_word = :1', profane_word.base_word )

    for matched_word in matched_words:
        if matched_word.correct_word:
            # We already have this word,
            # don't write it
            return False

    profane_word.put( )

    return True

if __name__ == '__main__':
	profanity_modifier = robot.Robot( 'ProfanityModifier',
	    image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
	    profile_url = 'http://profanity-modifier.appspot.com/' )
	profanity_modifier.RegisterHandler( events.BLIP_SUBMITTED, OnContentCreated )
	profanity_modifier.RegisterHandler( events.WAVELET_BLIP_CREATED, OnContentCreated )
	profanity_modifier.Run( )
