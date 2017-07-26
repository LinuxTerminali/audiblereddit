from flask import Flask,Response,render_template,request
from gtts import gTTS
from collections import Counter
from newspaper import Article
import json, requests
from collections import Counter
app = Flask(__name__)


@app.route('/b', methods=['GET'])
def b():
   # view structure of an individual post
   # print(json.dumps(r.json()['data']['children'][0]))
   my_var = request.args.get('my_var', None)
   print(my_var)
   subreddit = 'India'
   article = Article(my_var)
   article.download()
   article.parse()
   tt = gTTS(text=article.text, lang="hi")
   tt.save("News.mp4")
   print("Done!")
   return render_template('Play.html',text = article.text)

   '''r = requests.get(
    'http://www.reddit.com/r/{}.json'.format(subreddit),
    headers={'user-agent': 'Mozilla/5.0'} 
   )
   notallowed_domain = ['youtube.com','self.india','i.redd.it','i.imgur.com','i.redditmedia.com','youtu.be']
   for post in r.json()['data']['children']:
	   domain = post['data']['domain']
	   newslist = []
	   if domain not in notallowed_domain:
		   newslist.append(post['data']['url'])
		   print(post['data']['url'])
	   return newslist	   '''



@app.route('/')
def hello():
	subreddit = 'India'
	r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),headers={'user-agent': 'Mozilla/5.0'} )
	notallowed_domain = ['youtube.com','self.india','i.redd.it','i.imgur.com','i.redditmedia.com','youtu.be']
	newsurl = []
	newstitle = []
	dictk = {}
	for post in r.json()['data']['children']:
	    domain = post['data']['domain']

	    if domain not in notallowed_domain:
		    newsurl.append(post['data']['url'])
		    newstitle.append(post['data']['title'])
		    dictk.update({post['data']['url']:post['data']['title']})
	#print(newslist)
	#print(dictk)

	return  render_template('Index.html',completelist = dictk)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']


def temp():
	article = Article("http://www.scmp.com/week-asia/geopolitics/article/2103656/indias-got-itself-fine-mess-doklam-its-time-get-out-and-let")
	article.download()
	article.parse()
	tt = gTTS(text=article.text, lang="hi")
	tt.save("News.wav")
	print("Done!")
@app.route("/wav")
def streamwav():
    def generate():
        with open("News.mp4", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")	

if __name__ == '__main__':
    app.run(debug=True)
