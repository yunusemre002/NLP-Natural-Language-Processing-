import pandas as pd
from termcolor import colored
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

"""
1. reviews_df = pd.read_csv("file.cvs", encoding = "ISO-8859-1" )  önemli
"""
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text','Review Rating']]
reviews_df_com.insert(2,'Tag', 0, True) # tag diye kolon ekledim 2. sıraya ilkledim 0 diye

reviews_df_com.insert(3, 'staff', 0, True)
reviews_df_com.insert(3, 'location', 0, True)
reviews_df_com.insert(3, 'room', 0, True)
reviews_df_com.insert(3, 'breakfast', 0, True)
reviews_df_com.insert(3, 'bed', 0, True)
reviews_df_com.insert(3, 'service', 0, True)
reviews_df_com.insert(3, 'bathroom', 0, True)
reviews_df_com.insert(3, 'view', 0, True)
reviews_df_com.insert(3, 'food', 0, True)
reviews_df_com.insert(3, 'restaurant', 0, True)

reviews_df_com = reviews_df_com.dropna().copy() # boş yorum varsa kaldırır.
reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.count() , reviews_df_com.describe(), sep="\n")


#------------------------------------------------PREPROCCESSİNG---------------------------------------------------
from nltk.corpus import wordnet
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
def clean_text(text):
    text =str(text)
    text = text.lower()    # lower text
    text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens
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
    #print("Overall SA is : ", score)
    return score["compound"]

def findSubject(dizi,t):
    colName = str(dizi[0])
    for i in dizi:
        if i in reviews_df_com['Review Text'].values[t]:
            reviews_df_com[colName].values[t] = 1

if __name__ == "__main__":
    k = sonuc = posNumber = negNumber = notrNumber = 0
    attributes = ["staff", "location", "room", "breakfast", "bed", "service", "bathroom", "bathroom", "view", "food", "restaurant"]

    # Bunları word to vect ile genişleteceğiz.
    staff = ["staff"]
    loc = ["location"]
    room = ["room"]
    breakfast = ["breakfast"]
    bed = ["bed"]
    service = ["service"]
    bath = ["bathroom"]
    view = ["view"]
    food = ["food"]
    rest = ["restaurant"]

    for t in range(len(reviews_df_com)):
        i = str(reviews_df_com['Review Text'].values[t])
        #print("\n", i)
        sonuc = sentiment_scores(i)     # İlgili yorumu i dizisine aldık şimdi yorumu SA  yaptırıyoruz sonuçta compound dönüyor.
        #sentiment_scores(clean_text(i))

        if   sonuc > 0 :                                # Positive  23569
            reviews_df_com['Tag'].values[t] = 1
        elif sonuc == 0 :                               # Nötr    1538
            reviews_df_com['Tag'].values[t] = 0
        else:                                           # Negative // sonuc < 0  2223
            reviews_df_com['Tag'].values[t] = -1
            print(colored(i, 'red'))

        findSubject(staff, t)
        findSubject(loc, t)
        findSubject(room, t)
        findSubject(breakfast, t)
        findSubject(bed, t)
        findSubject(service, t)
        findSubject(bath, t)
        findSubject(view, t)
        findSubject(food, t)
        findSubject(rest, t)

        print(reviews_df_com.values[t])


    print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))


    for i in attributes:
        #print("\n", reviews_df_com[i].value_counts())
        #print("\n", reviews_df_com.count())

        print(i," : ",len(reviews_df_com[reviews_df_com[i] == 1]),"/", len(reviews_df_com.index))






    #staff = []
    # loc = []
    # room = []
    # breakfast = []
    # bed = []
    # service = []
    # bath = []
    # view = []
    # food = []
    # rest = []