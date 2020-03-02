import pandas as pd
import re

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/hotel-reviews/7282_1.csv")   # read data
reviews_df_com = reviews_df[['reviews.rating','reviews.text','reviews.title']]
reviews_df_com = reviews_df_com.sample(frac = 0.1, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.count())

#------------------------------------------------PREPROCCESSİNG---------------------------------------------------
from nltk.corpus import wordnet

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    text =str(text)
    text = text.lower()    # lower text
    text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens"""
    pos_tags = pos_tag(text)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    text = [t for t in text if len(t) > 1]     # remove words with only one letter
    text = " ".join(text)
    print(text)
    return (text)

#------------------------------------------------SENTİMENT ANALYSES---------------------------------------------------
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()    # Create a SentimentIntensityAnalyzer object.
    score = sid_obj.polarity_scores(sentence)
    print("Overall sentiment dictionary is : ", score)
    return score["compound"]

if __name__ == "__main__":
    k = 0
    sonuc = 0
    for i in reviews_df_com['reviews.text']:
        print("\n", i)
        sonuc += sentiment_scores(clean_text(i))    #sentiment_scores(i)
        k+=1
    print(sonuc/k)


# stop wordü temizlemezisek bazı satırlar için