from flask import Flask, render_template, request
from nltk import sent_tokenize, word_tokenize
import docx2txt
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET","POST"])
def upload():

    target = os.path.join(APP_ROOT, "static/")

    if not os.path.isdir(target):
        os.mkdir(target)
        
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)


    f = open(destination, "r")
    r = [word for sentence in f.readlines() for word in word_tokenize(sentence)]
    f.close()

    os.remove(destination)
    
    return render_template("completed.html", r = r)

if __name__ == '__main__':
   app.run(debug = True)
