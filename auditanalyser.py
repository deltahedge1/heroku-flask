# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:28:14 2017

@author: ihassan1
"""

import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from stemming.porter2 import stem
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))
#checkwords = open('C:/Users/ihassan1/AAA/ANZ Breech Local/searchwords.txt').read().splitlines()
lemmatizer = WordNetLemmatizer()

class auditAnalyser(object):
    
    def __init__(self, checkwords=[]):
        self.checkwords = self._clean_checkwords(checkwords)
        
        
    def _clean_checkwords(self, checkwords):
        
        checkwords = [word.lower() for word in checkwords] #lower the word
        
        checkwords_stemmed = []
        for phrase in checkwords:
            temp = []
            for word in word_tokenize(phrase):
                temp.append(stem(word))
            
            stemmed_phrase = " ".join(temp)
            checkwords_stemmed.append([phrase, stemmed_phrase])
        
        return checkwords_stemmed
    
    
    def _clean_text(self, text):
        text = text.lower()
        text = [stem(word) for word in word_tokenize(text)]
        text = " ".join(text)
        
        return text
    
    
    def count_phrases(self, text):
        text = self._clean_text(text)
        
        word_count = 0
        for word, stemmedword in self.checkwords:
            word_count = word_count + len(re.findall(r"\b%s\b" %(stemmedword), text))
        return word_count
    
    
    def matched_words(self,text):
        text = self._clean_text(text)
        

        matched_words = []
        for word, stemmedword in self.checkwords:
            
            matches = re.findall(r"\b%s\b" %(stemmedword), text)
            
            if bool(matches) == True:
                for match_word in matches:
                    matched_words.append(word)
        
        matched_string = "|"
        
        for word in matched_words:
            matched_string = matched_string+word+"|"
        
        return matched_string
        
    
check_words = ["renumeration report"]
uA = auditAnalyser(check_words)
#uA.count_phrases("I want to be review and then you can also review me")
uA.matched_words("renumeration reporting and renumeration report")            



               
            
        
        
        
    
