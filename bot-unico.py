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
                    variacion = []
                    variacion.append('Sí, eres ' +  matched.groups()[0])
                    variacion.append('Sí cariño, ' +  matched.groups()[0])
                    variacion.append('Sí corazón, ' +  matched.groups()[0])
                    variacion.append('Sí. ' +  matched.groups()[0].title())
                    reply = '{4} únic{2}. https://twitter.com/{0}/status/{3}'.format(status.user.screen_name,
                                                                                     matched.groups()[0],
                                                                                     matched.groups()[2].lower(),
                                                                                     status.id,
                                                                                     random.choice (variacion))
                    api.update_status(status=reply, in_reply_to_status_id=status.id)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['unico', 'unica', 'único', 'única'], async=True)
