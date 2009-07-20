from waveapi import events
from waveapi import model
from waveapi import robot

def OnRobotAdded( properties, context ):
	"""Invoked when the robot has been added"""
	root_wavelet = context.GetRootWavelet( )
	root_wavelet.CreateBlip( ).GetDocument( ).SetText( "Sup prudes?" )

def OnBlipSubmitted( properties, context ):
    """Invoked when a new blip has been submitted"""
    blip = context.GetBlipById(properties['blipId'])
    contents = blip.GetDocument().GetText()
    
    if '???' in contents:
        q = '"%s"' % contents.replace('???', '*').replace('"', ' ')
    
        start = 0
        res = {}
        for i in range(6):
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&start=%d&q=%s' % (start, urllib.quote(q))
            js = urlfetch.fetch(url=url).content
        
            for fragment in simplejson.loads(js)['responseData']['results']:
                for m in re.findall('\<b\>([^\<]*)', fragment['content']):
                    m = m.lower()
                    
                    if m == '...':
                        continue
                    res[m] = res.get(m, 0) + 1
            start += 5
    
        if res:
            res = res.items()
            res.sort(lambda a,b: -cmp(a[1], b[1]))
            blip.GetDocument().SetText(res[0][0])

if __name__ == '__main__':
    profanity_modifier = robot.Robot( 'ProfanityModifier',
	    image_url = 'http://profanity-modifier.appspot.com/assets/icon.jpg',
		version = '1',
	    profile_url = 'http://profanity-modifier.appspot.com/' )
    profanity_modifier.RegisterHandler( events.WAVELET_SELF_ADDED, OnRobotAdded )
    profanity_modifier.RegisterHandler( events.BLIP_SUBMITTED, OnBlipSubmitted )
    profanity_modifier.Run( )
