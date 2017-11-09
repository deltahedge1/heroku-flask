from flask import Flask, render_template, request
from nltk import sent_tokenize, word_tokenize
import docx2txt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET","POST"])
def upload():

    for file in request.files.getlist("file"):
        filename = file.filename
        #destination = "/".join([target, filename])  
    
    f = open(filename, "r")
    r = [word for sentence in f.readlines() for word in sentence]
    
    f.close()
        
    return render_template("completed.html", r = r)

if __name__ == '__main__':
   app.run(debug = True)
