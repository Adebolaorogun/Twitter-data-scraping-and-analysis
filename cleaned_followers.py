import tweepy
import webbrowser 
import time 
import pandas as pd 

## Input the credentials 

#consumer_key =##......
#consumer_secret = ##...
#access_token = ##....
#access_token_secret = ## 

## Verification 
callback_uri = "oob"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
redirect_url= auth.get_authorization_url()
print(redirect_url)
webbrowser.open(redirect_url)
user_pin_input = input("What's is the user pin?")
auth.get_access_token(user_pin_input)

api = tweepy.API(auth)
me = api.me()

## Import the dataset 
df = pd.read_csv("./contributions new.csv")

d4 = pd.DataFrame(df.groupby(by="handle")["amount_in_usdt"].sum())
d4.reset_index(drop=False, inplace=True)
d4 = d4.sort_values(by="amount_in_usdt", ascending=False)
d4.reset_index(inplace=True, drop=True)

account = d4.loc[:100, :].handle.values


my_index = []
for i in range(df.shape[0]):
    if df.loc[i, "handle"] in account:
        my_index.append(i)

d1 = df.loc[my_index, :]
d1.index = d1.handle
d1.dropna(subset=["twitter_handle"], axis=0, inplace=True)
d1.rename({"handle": "handles"}, axis=1, inplace=True)
d1 = pd.DataFrame(d1.groupby("handle")["amount_in_usdt"].sum())
d2 = d1.sort_values(by="amount_in_usdt", ascending=False)

my_index = []
for i in range(df.shape[0]):
    if df.loc[i, "handle"] in d2.index:
        my_index.append(i)



dataset = df.dropna(subset=["twitter_handle"], axis=0)
dd1 = pd.DataFrame(dataset.groupby("twitter_handle")["amount_in_usdt"].sum())
dd2 = pd.DataFrame(dataset.groupby("handle")["amount_in_usdt"].sum())

df2 = dataset.dropna(subset=["twitter_handle"], axis=0)

dd1.sort_values(by="amount_in_usdt", ascending=False, inplace=True)
dd2.sort_values(by="amount_in_usdt", ascending=False, inplace=True)

dd1.reset_index(drop=False, inplace=True)
dd2.reset_index(drop=False, inplace=True)

dd = dd1.merge(dd2, on ="amount_in_usdt", how="outer", suffixes=("", "__"))

#### Loop to get the number of followers

followers4 = []

for i in dd.twitter_handle:
    if i != "clemente_DCode":
        user = api.get_user(i)
        followers4.append(user.followers_count)

#Clemente_DCode has no twitter account
followers4.insert(7, "Not found")
dd["followers"] = followers4

