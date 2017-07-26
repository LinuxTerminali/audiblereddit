import json, requests
from collections import Counter

subreddit = 'India'

r = requests.get(
    'http://www.reddit.com/r/{}.json'.format(subreddit),
    headers={'user-agent': 'Mozilla/5.0'}
)

# view structure of an individual post
# print(json.dumps(r.json()['data']['children'][0]))
notallowed_domain = ['youtube.com','self.india','i.redd.it','i.imgur.com','i.redditmedia.com','youtu.be']
for post in r.json()['data']['children']:
	domain = post['data']['domain']
	if domain not in notallowed_domain:
		print(post['data']['url'])