# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 20:27:13 2020

@author: GUPTA50
"""

#Importing the required libraries
import re
import nltk
import heapq


article_text = ""


#Reading the data from the text file and creating article text
def text_read():
    with open("Economy.txt", "r") as f:
        paragraphs = f.readlines()
    return paragraphs


def Text_processing():
    global article_text
    paragraphs = text_read()
    for p in paragraphs:
        article_text += p
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    #Creating a list of the stopwords using nltk library
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    #Creating a dictionary, which has the frequence for each word like if GST is encountered seven times it will be like "GST": 7
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())
    #to find the weighted frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    sentence_list = nltk.sent_tokenize(article_text)
    #Calcultion of sentence scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
                    
    return sentence_scores
#Taking the top 10 sentence to create the brief summary of the article                    

def summary():
    summary_sentences = heapq.nlargest(10, Text_processing(), key=Text_processing().get)
    summary = ' '.join(summary_sentences)
    with open("Economic_Summarization.txt", "w") as f:
        f.write(summary)  
        

if __name__ == '__main__': 
    summary()