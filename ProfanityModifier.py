from waveapi import events
from waveapi import model
from waveapi import robot

def OnParticipantsChanged( properties, context ):
	"""Invoked when any participants have been added/removed"""
	added = properties['participantsAdded']
	
	for p in added:
		Notify( context )

def OnRobotAdded( properties, context ):
	"""Invoked when the robot has been added"""
	root_wavelet = context.GetRootWavelet( )
	root_wavelet.CreateBlip( ).GetDocument( ).SetText( "I'm alive!" )

def OnBlipSubmitted( properties, context ):
	"""Invoked when a new blip has been submitted"""
	root_wavelet = context.GetRootWavelet( )
	root_wavelet.CreateBlip( ).GetDocument( ).SetText( properties.keys( ) )
	

def Notify( context ):
	root_wavelet = context.GetRootWavelet( )
	root_wavelet.CreateBlip( ).GetDocument( ).SetText( "Hi everybody!" )

if __name__ == '__main__':
	myRobot = robot.Robot( 'ProfanityModifier',
		image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
		profile_url = 'http://profanity-modifier.appspot.com/' )
	myRobot.RegisterHandler( events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged )
	myRobot.RegisterHandler( events.WAVELET_SELF_ADDED, OnRobotAdded )
	myRobot.RegisterHandler( events.BLIP_SUBMITTED, OnBlipSubmitted )
	myRobot.Run( )
