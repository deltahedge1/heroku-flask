from flask import Flask, render_template, request
from collections import Counter
import nltk
from nltk import sent_tokenize, word_tokenize
from auditanalyser import auditAnalyser
import pandas
import docx2txt
import os
import re

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# code to find out if there are long sentences
def long_sentences_count(text):
    temp = nltk.word_tokenize(text)
    return len(temp)

#count verbs in a sentence
def count_verbs(text):
    tokenize = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenize, tagset="universal")
    
    tags = [tag for word,tag in tagged if len(word)>4] #count a verb if it has a length more than 5 words
    dictionary_tagged = dict(Counter(tags))
        
    try:
        return dictionary_tagged["VERB"]
    except:
        return 0

#return matched verbs in a sentence
def matched_verbs(text):
    tokenize = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenize, tagset="universal")
    tags = [word for word,tag in tagged if tag == "VERB" if len(word)>4]
    
    w = "|"
    for i in tags:
            w = w+i+"|"
            
    return w
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

    target = os.path.join(APP_ROOT, "static/") #path to save and upload files
    search_words_path = os.path.join(APP_ROOT,"search words/") #path to look for check and alert words
    
    #opening checkwords
    f = open(search_words_path+"check_words.txt", "r")
    check_words = f.readlines()
    check_words = [word.replace("\n","") for word in check_words]
    f.close()
    
    #opening alert words 
    f = open(search_words_path+"alert_words.txt","r")
    alert_words = f.readlines()
    alert_words = [word.replace("\n","") for word in alert_words]
    f.close()
    
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
    
    return render_template("completed.html", r = alert_words)

if __name__ == '__main__':
   app.run(debug = True)
