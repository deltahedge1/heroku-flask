from flask import Flask, render_template
from textblob import TextBlob
from nltk import word_tokenize

a = TextBlob("Ishtiaq is my name")
b = list(a.words)

c = word_tokenize("Samantha is nice")
                  
app = Flask(__name__)

@app.route("/")
def index():
           return render_template("index.html", r = c)

if __name__ == "__main__":
           app.run()
