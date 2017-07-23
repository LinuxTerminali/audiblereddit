from flask import Flask,Response
from gtts import gTTS
from collections import Counter
from newspaper import Article

app = Flask(__name__)


@app.route('/')
def hello():
	article = Article("https://www.bloomberg.com/news/articles/2017-07-23/japan-captures-more-photographs-of-likely-melted-fukushima-fuel")
	article.download()
	article.parse()
	tt = gTTS(text=article.text, lang="hi")
	tt.save("News.wav")
	print("Done!")
	return 'Hello world'

@app.route("/wav")
def streamwav():
    def generate():
        with open("News.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")	

if __name__ == '__main__':
    app.run(debug=True)
