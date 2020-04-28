import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

"""
1. reviews_df = pd.read_csv("file.cvs", encoding = "ISO-8859-1" )  önemli
"""
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text','Review Rating']]
reviews_df_com = reviews_df_com.dropna().copy() # boş yorum varsa kaldırır.
reviews_df_com = reviews_df_com.sample(frac = 0.1, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
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
    NewValue = (((score["compound"] - (-1.0)) * (5.0 - 1.0)) / (1.0 - (-1.0))) + 1.0
    print("Overall sentiment dictionary is : ", score, " Yeni :", NewValue, end="")
    return score["compound"]

if __name__ == "__main__":
    k = sonuc = basarili = basarisiz =0
    predict = []
    realDizi = reviews_df_com['Review Rating'].values

    for t in range(len(reviews_df_com)):
        i = str(reviews_df_com['Review Text'].values[t])
        real = int(reviews_df_com['Review Rating'].values[t])
        print("\n", i)
        sonuc = sentiment_scores(i) #sentiment_scores(clean_text(i))
        print("   Raiting", real)
        sonucNolmal5= (((sonuc - (-1.0)) * (5.0 - 1.0)) / (1.0 - (-1.0))) + 1.0
        predict.append(round(sonucNolmal5))

        if ((real >= 4) and (sonucNolmal5 >= 4)):        # Positive
            basarili += 1
        elif ((real >= 2.7) and (sonucNolmal5 >= 2.7)):  # Nötr
            basarili += 1
        elif ((real < 2.7) and (sonucNolmal5 < 2.7)):  # Negative
            basarili += 1
        else:
            basarisiz += 1
            print(colored (i, 'red'))

    print(basarili,basarisiz)
    print("Başarı oranı : %",basarili*100/(basarili+basarisiz))
    print("Başarısızlık oranı",basarisiz*100/(basarili+basarisiz))

#-----------------GOOD ÇIKTI ANALİZ-------------------------------------
    results = confusion_matrix(realDizi, predict)
    print('Confusion Matrix :', results, sep="\n")
    print('Accuracy Score :', accuracy_score(realDizi, predict))
    print('Report : ', classification_report(realDizi, predict), sep="\n")

#--------------------- PLOT2---------------------------------------------
    cm = confusion_matrix(realDizi, predict)
    df_cm = pd.DataFrame(cm, range(5), range(5))
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 11})  # font size
    plt.show()
