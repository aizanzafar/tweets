from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import twitter_credentials as tc
import json
import pandas as pd

##########
df = pd.DataFrame(columns = ["Serial_no.", "Name", "screen_name", "reply_to_screen_name", "Tweet"])

print(df)

with open('tweets.csv', 'a') as f:
	df.to_csv(f)

f.close()
##########

ckey = tc.ckey
csecret = tc.csecret
atoken = tc.atoken
asecret = tc.asecret

i = 1
##########

class listener(StreamListener):

	def on_data(self, data):

		global i

		##########

		try:
			info = json.loads(data)

			##########

			if 'extended_tweet' in info.keys():
				text = info['extended_tweet']['full_text']
			elif 'retweeted_status' in info.keys():
				text = info['retweeted_status']['extended_tweet']['full_text']
			else:
				text = info['text']

			##########

			# print("Name = ", info['user']['name'])
			# print("User_id = ", info['user']['id'])
			# print("Reply_to_id = ", info['in_reply_to_user_id'])
			# print("Message = ", text)
			# print('\n\n')

			##########

			file = open('tweetDB.txt', 'a')
			
			file.write("Serial no = "+str(i)+'\n')
			file.write("Name = "+info['user']['name']+'\n')
			file.write("User_id = "+str(info['user']['id'])+'\n')
			file.write("Reply_to_id = "+str(info['in_reply_to_user_id'])+'\n')
			file.write("Reply_to_id = "+str(info['in_reply_to_screen_name'])+'\n')
			file.write("Message = "+text+'\n')
			#file.write(str(info.keys())+'\n')
			#file.write(data+'\n')
			file.write('\n\n\n')
			
			file.close()

			##########

			data = [str(i), info['user']['name'],info['user']["screen_name"],
					str(info['in_reply_to_screen_name']), text]

			df.loc[i-1] = data
			with open('tweets.csv', 'w') as f:

				df.to_csv(f)

			f.close()

			i = i+1

			return(True)

		##########

		except BaseException as e:
			print("Failed on data", str(e))

		##########

	def on_error(self, status):
		print("Error: ", status)

##########

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener(), tweet_mode='extended')
twitterStream.filter(track=["CoronaVirus", "coronavirus", "COVID_19", "covid_19", "covid19", "Covid19", "CoronaVirusUpdate", "Covid_19", "CoronavirusPandemic"], languages=['en'])
