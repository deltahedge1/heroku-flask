from flask import Flask, render_template, request
from nltk import sent_tokenize, word_tokenize
import docx2txt
import os
import re

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# extract text from word documents into python
def extract_text_and_clean_up(file_path):
    #extract the text
    text = docx2txt.process(file_path)
    #get a list split by newlines
    text = text.split("\n")
    
    #clean the text
    cleaned_text = []
    for i in text:
        if len(i)>1: #only want to look and append any item which is not a space
            
            i = i.replace("\t","") #remove any tabs
            i = re.sub("[^A-Za-z0123456789 _+-.,!@#$%^&*();\\/|<>\"'?=:\s]","", i) #remove anything that is not normal
            
            sentTokenized = sent_tokenize(i) #added this tokenize any sentences
            
            for sentence in sentTokenized:
                cleaned_text.append(sentence)
            
    return(cleaned_text)

#######################################################################################################################        


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

    text = extract_text_and_clean_up(destination)
    
    #f = open(destination, "r")
    #r = [word for sentence in f.readlines() for word in word_tokenize(sentence)]
    #f.close()

    os.remove(destination)
    
    return render_template("completed.html", r = text)

if __name__ == '__main__':
   app.run(debug = True)
