from waveapi import events
from waveapi import model
from waveapi import robot

def OnRobotAdded( properties, context ):
	"""Invoked when the robot has been added"""
	root_wavelet = context.GetRootWavelet( )
	root_wavelet.CreateBlip( ).GetDocument( ).SetText( "Sup prudes?" )

def OnBlipSubmitted( properties, context ):
    """Invoked when a new blip has been submitted"""
    profane_words = [ "shit" ]
    politically_correct_words = [ "poop" ]

    blip = context.GetBlipById( properties['blipId'] )
    contents = blip.GetDocument( ).GetText( )
    
    

    for word in profane_words:
        if word in contents:
            """Replace each profane word with it's politically correct alternative"""
            q = '"%s"' % contents.replace( word, politically_correct_words[ profane_words.index( word ) ] )
            blip.GetDocument().SetText( q )

if __name__ == '__main__':
    profanity_modifier = robot.Robot( 'ProfanityModifier',
	    image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
	    profile_url = 'http://profanity-modifier.appspot.com/' )
    profanity_modifier.RegisterHandler( events.WAVELET_SELF_ADDED, OnRobotAdded )
    profanity_modifier.RegisterHandler( events.BLIP_SUBMITTED, OnBlipSubmitted )
    profanity_modifier.Run( )
