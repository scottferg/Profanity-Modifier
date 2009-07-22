from waveapi import events
from waveapi import model
from waveapi import robot
from google.appengine.ext import db

from ProfanityDatabase import ProfaneWord

def OnContentCreated( properties, context ):
    """Called whenever a new wavelet or blip is created"""
    blip = context.GetBlipById( properties['blipId'] )
    contents = blip.GetDocument( ).GetText( )

    if 'LEARN/' in contents:
        if not SpecifyFilter( contents ):
            root_wavelet = context.GetRootWavelet( )
            root_wavelet.CreateBlip( ).GetDocument( ).SetText( "Sorry, but I already know that word." )
    else:
        blip.GetDocument().SetText( ReplaceProfanity( contents, blip ) )

def ReplaceProfanity( contents, blip ):
    """Replace each profane word with it's politically correct alternative"""
    result = contents.lower( );

    for word in contents.lower( ).split( ' ' ):
        # Remember to remove unnecessary whitespace on the word before searching for it
        matched_words = db.GqlQuery( 'SELECT * FROM ProfaneWord WHERE base_word = :1', " ".join( word.split( ) ) )

        for matched_word in matched_words:
            if matched_word.correct_word:
                result = '%s' % result.replace( word, matched_word.correct_word )

    return result

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
