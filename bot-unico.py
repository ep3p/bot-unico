import tweepy
import re
import random

consumer_key =         ''
consumer_secret =      ''
access_token =         ''
access_token_secret =  ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

pattern = re.compile('.*soy\s*(el|la)\s*(ú|u)nic(a|o).*\?.*', re.IGNORECASE)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if (not hasattr(status, 'retweeted_status')
            and not status.in_reply_to_screen_name):
            matched = pattern.match(status.text)
            if matched:
                articulo = matched.groups()[0]
                genero = matched.groups()[2].lower()
                variacion = []
                variacion.append('Sí, eres {} únic{}.'.format(articulo, genero))
                variacion.append('Sí cariño, {} únic{}.'.format(articulo, genero))
                variacion.append('Sí corazón, {} únic{}.'.format(articulo, genero))
                variacion.append('Sí. {} únic{}.'.format(articulo.title(), genero))
                reply = '{0} https://twitter.com/{1}/status/{2}'.format(random.choice(variacion),                                                                            
                                                                        status.user.screen_name,
                                                                        status.id)
                api.update_status(status=reply, in_reply_to_status_id=status.id)

myListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myListener)

myStream.filter(track=['unico', 'unica', 'único', 'única'], async=True)
