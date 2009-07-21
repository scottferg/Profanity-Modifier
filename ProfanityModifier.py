from waveapi import events
from waveapi import model
from waveapi import robot

def OnBlipSubmitted( properties, context ):
    """Invoked when a new blip has been submitted"""
    blip = context.GetBlipById( properties['blipId'] )
    ReplaceProfanity( blip )

def OnWaveletBlipCreated( properties, context ):
    """Invoked when a new wavelet has been submitted"""
    blip = context.GetBlipById( properties['blipId'] )
    ReplaceProfanity( blip )

def ReplaceProfanity( blip ):
    profane_words = [ "shit", "fuck", "rape", "damn", "cunt" ]
    politically_correct_words = [ "poop", "gently caress", "surprise sex", "gosh darn", "beef curtains" ]

    for word in profane_words:
        contents = blip.GetDocument( ).GetText( )
		
        if word in contents.lower( ):
			"""Replace each profane word with it's politically correct alternative"""
			q = '%s' % contents.lower( ).replace( word, politically_correct_words[ profane_words.index( word ) ] )
			blip.GetDocument().SetText( q )

if __name__ == '__main__':
	profanity_modifier = robot.Robot( 'ProfanityModifier',
	    image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
	    profile_url = 'http://profanity-modifier.appspot.com/' )
	profanity_modifier.RegisterHandler( events.BLIP_SUBMITTED, OnBlipSubmitted )
	profanity_modifier.RegisterHandler( events.WAVELET_BLIP_CREATED, OnWaveletBlipCreated )
	profanity_modifier.Run( )
