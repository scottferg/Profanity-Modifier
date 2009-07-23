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

def OnBlipSubmitted( properties, context ):
    """Invoked when a new blip has been submitted"""
    blip = context.GetBlipById( properties['blipId'] )
    contents = blip.GetDocument( ).GetText( )

    if 'LEARN/' in contents:
        SpecifyFilter( contents ) 
    else:
        ReplaceProfanity( contents, blip )

def OnWaveletBlipCreated( properties, context ):
    """Invoked when a new wavelet has been submitted"""
    blip = context.GetBlipById( properties['blipId'] )
    contents = blip.GetDocument( ).GetText( )

    if 'LEARN/' in contents:
        SpecifyFilter( contents ) 
    else:
        ReplaceProfanity( contents, blip )

def ReplaceProfanity( contents, blip ):
    """Replace each profane word with it's politically correct alternative"""
    result = contents;

    for word in contents.lower( ).split( ' ' ):
        # Remember to remove unnecessary whitespace on the word before searching for it
        matched_words = db.GqlQuery( 'SELECT * FROM ProfaneWord WHERE base_word = :1', " ".join( word.split( ) ) )

        for matched_word in matched_words:
            if matched_word.correct_word:
                result = '%s' % result.replace( word.lower( ), matched_word.correct_word )
                blip.GetDocument().SetText( result )

def SpecifyFilter( contents ):
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
            return

    profane_word.put( )

if __name__ == '__main__':
	profanity_modifier = robot.Robot( 'ProfanityModifier',
	    image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
	    profile_url = 'http://profanity-modifier.appspot.com/' )
	profanity_modifier.RegisterHandler( events.BLIP_SUBMITTED, OnBlipSubmitted )
	profanity_modifier.RegisterHandler( events.WAVELET_BLIP_CREATED, OnWaveletBlipCreated )
	profanity_modifier.Run( )
