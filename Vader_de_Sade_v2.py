import pandas as pd
from termcolor import colored

"""
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/hotel-reviews/7282_1.csv")   # read data
print(reviews_df.columns)
reviews_df_com = reviews_df[['reviews.rating','reviews.text','reviews.title']]
reviews_df_com = reviews_df_com.sample(frac = 0.1, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.count())
print(reviews_df_com.describe())
"""

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/Hotel_Reviews_n15.csv")   # read data
reviews_df["review"] = reviews_df["Negative_Review"] + reviews_df["Positive_Review"] # append the positive and negative text reviews
reviews_df_com = reviews_df[["review","Reviewer_Score"]]    # select only relevant columns # dataFrame'im sadece 2 kolondan müteşekkil artık. Yorumlar (Karışık ve 0/1 olduğu değerler.)
reviews_df_com = reviews_df.sample(frac = 0.1, replace = False, random_state=42)
reviews_df_com["review"] = reviews_df["review"].apply(lambda x: x.replace("No Negative", "").replace("No Positive", ""))    # remove 'No Negative' or 'No Positive' from text
print(reviews_df_com.count())
print(reviews_df_com.describe())

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
    sonuc = score["compound"]
    NewValue = (((sonuc - (-1.0)) * (10.0 - 1.0)) / (1.0 - (-1.0))) + 1.0
    print("Overall sentiment dictionary is : ", score, " Yeni :", round(NewValue), end="")
    return score["compound"]


if __name__ == "__main__":
    k = 0
    sonuc = 0
    pos=0
    neg=0
    pos20=0
    neg20=0
    edited = reviews_df_com.dropna().copy()
    for t in range(len(edited)):
        i = str(edited['review'].values[t])
        real = int(edited['Reviewer_Score'].values[t])
        print("\n", i)
        i = str(i)
        sonuc = sentiment_scores(i) #sentiment_scores(clean_text(i))
        print("   Raiting", real)
        sonuc10 = (((sonuc - (-1.0)) * (10.0 - 1.0)) / (1.0 - (-1.0))) + 1.0
        sonuc10= round(sonuc10)

        if (real>5):
            pos += 1
        else:
            neg += 1
            print(colored (i, 'red'))
            #print(colored(i, 'red'), colored('world', 'green'))

        if ((sonuc10-sonuc10*0.25< real) and (sonuc10+sonuc10*0.25>= real)):
            pos20 += 1
        else:
            neg20 +=1

    print(pos, "\n",neg)
    print("Başarı oranı : %",pos*100/(pos+neg))
    print("neg oranı",neg*100/(pos+neg))

    print(pos20, "\n",neg20)
    print("%20 Başarı oranı : %",pos20*100/(pos20+neg20))
    print("%20 hata  oranı",neg20*100/(pos20+neg20))

# stop wordü temizlemezisek bazı satırlar için



