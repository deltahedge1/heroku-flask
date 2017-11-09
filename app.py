from flask import Flask
from textblob import TextBlob
from nltk import word_tokenize

a = TextBlob("Ishtiaq is my name")

b = list(a.words)

c = word_tokenize("Ishtiaq is nice")
                  
app = Flask(__name__)

@app.route("/")
def index():
           return "hello" + str(c[0])

if __name__ == "__main__":
           app.run()
