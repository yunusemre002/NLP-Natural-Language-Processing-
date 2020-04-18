import pandas as pd
from termcolor import colored

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
    print("Overall sentiment dictionary is : ", score, " Predict :", NewValue, end="")
    return score["compound"]

if __name__ == "__main__":
    k = sonuc = pos = neg = 0
    edited = reviews_df_com.dropna().copy()
    for t in range(len(edited)):
        i = str(edited['review'].values[t])
        real = int(edited['Reviewer_Score'].values[t])
        print("\n", i)
        sonuc = sentiment_scores(i) #sentiment_scores(clean_text(i))
        print("   User raiting :", real)
        sonuc10 = (((sonuc - (-1.0)) * (10.0 - 1.0)) / (1.0 - (-1.0))) + 1.0

        if ((real >= 7) and (sonuc10 >= 7)):          # Positive
            pos += 1
        elif ((real >=3.01 ) and (sonuc10 >= 3.01)):  # Nötr
            pos += 1
        elif ((real <= 3) and (sonuc10 <= 3)):        # Negative
            pos += 1
        else:
            neg += 1
            print(colored(i, 'red'))

    print(pos,neg)
    print("Başarı oranı : % ",pos*100/(pos+neg))
    print("Başarısızlık oranı : % ",neg*100/(pos+neg))