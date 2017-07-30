from flask import Flask, Response, render_template, request, jsonify, redirect
from gtts import gTTS
from collections import Counter
from newspaper import Article
import json
import requests
from textblob import TextBlob
from collections import Counter
import json
app = Flask(__name__)

notallowed_domain = ['youtube.com', 'self.india', 'self.worldnews', 'self.upliftingnews', 'self.technology',
                     'self.UpliftingKhabre', 'self.tifu', 'self.jokes', 'self.PUBATTLEGROUNDS', 'self.ProRevenge',
                     'self.nba', 'self.MaliciousCompliance', 'self.ProRevenge',
                     'i.redd.it', 'i.imgur.com', 'i.redditmedia.com', 'youtu.be',
                     'twitter.com', 'imgur.com', 'pbs.twimg.com', 'streamable.com', 'self.Jokes', 'self.explainlikeimfive', 'gfycat.com',
                     'self.Showerthoughts', 'self.leagueoflegends', 'media.giphy.com', 'self.hearthstone', 'self.circlejerk', 'i.gyazo.com', 'self.AskReddit', 'clippituser.tv',
                     'self.worldpolitics','self.uncensorednews','self.environment','self.Economics']


@app.route('/audioandtext', methods=['GET'])
def audioandtext():
    sourceurl = request.args.get('sourceurl', None)
    language = request.args.get('lang', None)
    try:
        article = Article(sourceurl)
        article.download()
        article.parse()
        Qt = TextBlob(article.text)
        titletext = article.title
        if Counter(language) == Counter('en'):
            Qt = str(Qt)
            tt = gTTS(text=Qt, lang='en-us')
        else:
            Qt = str(Qt.translate(to=language))
            # print(Qt)
            titletext = TextBlob(article.title)
            titletext = str(titletext.translate(to=language))
            tt = gTTS(text=Qt, lang=language)

        tt.save("News.mp4")
    except:
        return redirect(sourceurl)
    # print("Done!")

    return render_template('Play.html', text=Qt, title=titletext, url=sourceurl)

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


@app.route('/nextpage', methods=['GET'])
def nextpage():
    # print(nextpagecount)
    global nextpagecount
    sortedwords = ['hot', 'new', 'controversial']
    isitsorted = request.args.get('sorted', None)
    after = request.args.get('after', None)
    subreddit = request.args.get('subreddit', None)
    payload = {'count': nextpagecount, 'after': after}
    if isitsorted in sortedwords:
        r = requests.get('http://www.reddit.com/r/{}/{}/.json'.format(subreddit, isitsorted),
                         params=payload, headers={'user-agent': 'Mozilla/5.0'})
    else:

        r = requests.get('http://www.reddit.com/r/{}/.json'.format(subreddit),
                         params=payload, headers={'user-agent': 'Mozilla/5.0'})
    print(r.url)
    d = {}
    json_results = []
    for post in r.json()['data']['children']:
        domain = post['data']['domain']
        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']}
            json_results.append(d)
    paginationnumber = r.json()['data']['after']

    # print("Done!")
    nextpagecount = nextpagecount + 25
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber)


@app.route('/search', methods=['GET', 'POST'])
def search():
    global nextpagecount
    nextpagecount = 25
    text = ''
    if request.method == 'POST':
        text = request.form['text']
        print(text)
    subreddit = text
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    try:
        for post in r.json()['data']['children']:
            # print(post)
            domain = post['data']['domain']
            if domain not in notallowed_domain:
                d = {'url': post['data']['url'],
                     'title': post['data']['title'],
                     'domain': post['data']['domain'],
                     'thumbnail': post['data']['thumbnail']

                     }
                json_results.append(d)
                paginationnumber = r.json()['data']['after']
    except KeyError:
        return render_template('searcherror.html', subreddit=subreddit)
    # print(newslist)
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/')
def all():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'news'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/india')
def india():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'India'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            print(post['data']['thumbnail'])
            json_results.append(d)
    paginationnumber = r.json()['data']['after']
    # print(newslist)
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/worldnews')
def worldnews():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'worldnews'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/technology')
def technology():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'Technology'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/upliftingnews')
def upliftingnews():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'UpliftingNews'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/uncensorednews')
def uncensorednews():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'uncensorednews'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/environment')
def environment():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'environment'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/economics')
def economics():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'economics'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/worldpolitics')
def worldpolitics():
    global nextpagecount
    nextpagecount = 25
    subreddit = 'worldpolitics'
    r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="no")


@app.route('/hot', methods=['GET'])
def hotarticle():
    global nextpagecount
    nextpagecount = 25
    subreddit = request.args.get('subreddit', None)
    r = requests.get('http://www.reddit.com/r/{}/hot.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="hot")


@app.route('/new', methods=['GET'])
def newarticle():
    global nextpagecount
    nextpagecount = 25
    subreddit = request.args.get('subreddit', None)
    r = requests.get('http://www.reddit.com/r/{}/new.json'.format(subreddit),
                     headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="new")


@app.route('/controversial', methods=['GET'])
def controversialarticle():
    global nextpagecount
    nextpagecount = 25
    subreddit = request.args.get('subreddit', None)
    r = requests.get('http://www.reddit.com/r/{}/controversial.json'.format(
        subreddit), headers={'user-agent': 'Mozilla/5.0'})
    d = {}
    json_results = []
    # print(r.json()['data']['children'][0])
    for post in r.json()['data']['children']:
        domain = post['data']['domain']

        if domain not in notallowed_domain:
            d = {'url': post['data']['url'],
                 'title': post['data']['title'],
                 'domain': post['data']['domain'],
                 'thumbnail': post['data']['thumbnail']

                 }
            json_results.append(d)
    # print(newslist)
    paginationnumber = r.json()['data']['after']
    return render_template('Index.html', completelist=json_results, redditname=subreddit, pagenumber=paginationnumber, sorted="controversial")


def temp():
    article = Article(
        "http://www.scmp.com/week-asia/geopolitics/article/2103656/indias-got-itself-fine-mess-doklam-its-time-get-out-and-let")
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
