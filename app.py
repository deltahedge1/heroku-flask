from flask import Flask, render_template
from textblob import TextBlob
from nltk import word_tokenize

f = open("test1.txt","r")

sentences = f.readlines()

list1 = [word for sentence in sentences for word in word_tokenize(sentence)]

                  
app = Flask(__name__)

@app.route("/")
def index():
           return render_template("index.html", r = list1)

if __name__ == "__main__":
           app.run()
