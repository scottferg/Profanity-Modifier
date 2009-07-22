from google.appengine.ext import db

class ProfaneWord( db.Model ):
    base_word = db.StringProperty( multiline = False )
    correct_word = db.StringProperty( multiline = True )
