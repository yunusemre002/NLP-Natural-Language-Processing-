import gensim as gensim
import nltk
import pandas as pd
from termcolor import colored
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

"""
1. reviews_df = pd.read_csv("file.cvs", encoding = "ISO-8859-1" )  önemli
"""
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text','Review Rating']]
reviews_df_com.insert(2,'Tag', 0, True) # tag diye kolon ekledim 2. sıraya ilkledim 0 diye
"""['My mother, daughter, and myself... 5 1 0 0 0 1 0 0 1 1 0 1] DF toplam 13 sütun/başlıktan müteşekkildir. 
1. Colunm belong to reviews.
2. sütun, kullanıcının verdiği yıldızı temsil eder. 5 üzerinden değerlendirilir.
3. sütun lexion based sentiment analysis yöntemi olan Vader ile cümlenin (1 0 -1) + - or nötr olduğu hususu temsil edilir.
Between 4-13 columns names like below(staff,location....). That is hotels attributes which is defined by us. And this colums 
just take a value that is 0 or 1. For a review (row): if 4. column is 0, we get not to mensioned about staff at this review.
And if 5. column is 1, we get there some thing about location because, this word : "location" is used in this review. 
"""
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
#reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.describe())


#------------------------------------------------PREPROCCESSİNG---------------------------------------------------
from nltk.corpus import wordnet
import string
from nltk import pos_tag, re
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
    #text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = nltk.word_tokenize(text)
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens
    pos_tags = pos_tag(text)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    text = [t for t in text if len(t) > 1]     # remove words with only one letter
    return (text)

#------------------------------------------------SENTİMENT ANALYSES---------------------------------------------------
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()    # Create a SentimentIntensityAnalyzer object.
    score = sid_obj.polarity_scores(sentence)
    #print("Overall SA is : ", score)
    return score["compound"]

def findSubject(dizi,t):            # This function searchs that does the review has got input word or not.
    colName = str(dizi[0])          # if there is (any), set this column to 1
    for i in dizi:
        if i in reviews_df_com['Review Text'].values[t]:
            reviews_df_com[colName].values[t] = 1

def word2vectfonc(kdizi, k):

    print(str(k) + ". Most similar to {0}".format(kdizi), model.wv.most_similar(positive=kdizi, topn=5))
    dizi = model.wv.most_similar(positive=kdizi, topn=5)
    for i in dizi:
        kdizi.append(i[0])

if __name__ == "__main__":
    k = sonuc = posNumber = negNumber = notrNumber = 0
    attributes = ["staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food", "restaurant"]

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

    #---------------------------- Word2Vec ----------------------------------
    top = []
    for i in reviews_df_com["Review Text"]:
        top.append(clean_text(i))     #top.append(text)  # şu okadar önemliki anlayamazsınız :)
    print(top)

    model = gensim.models.Word2Vec(top, size=150, window=10, min_count=2, workers=10)
    model.train(top, total_examples=len(top), epochs=10)

    word_vectors = model.wv
    # if 'hotel' in word_vectors.vocab:
    #     print(model.wv.most_similar(positive='hotel'))
    # else:
    #     print("nedeeeeeeeeeeeeeeeeeeeeeeeeeeeeen")
    # for i in word_vectors.vocab:
    #     print(i)

    word2vectfonc(staff, 1)
    word2vectfonc(loc, 2)
    word2vectfonc(room, 3)
    word2vectfonc(breakfast, 4)
    word2vectfonc(bed, 5)
    word2vectfonc(service, 6)
    word2vectfonc(bath, 7)
    word2vectfonc(view, 8)
    word2vectfonc(food, 9)
    word2vectfonc(rest, 10)

    #------------------------------ Vader -----------------------------------------
    for t in range(len(reviews_df_com)):                        # iterate for each object
        i = str(reviews_df_com['Review Text'].values[t])        # Take just reviews to String : i
        #print("\n", i)
        sonuc = sentiment_scores(i)     # İlgili yorumu i dizisine aldık şimdi yorumu SA yaptırıyoruz sonuçta compound dönüyor.
        #sentiment_scores(clean_text(i))

        # given compound put in variable which name is sonuc then we will decide the review is positive, negtive
        # or notr. After we decide that, we set the "tag" columns like decided.
        if   sonuc > 0 :                                # Positive  23569
            reviews_df_com['Tag'].values[t] = 1
        elif sonuc == 0 :                               # Nötr    1538
            reviews_df_com['Tag'].values[t] = 0
        else:                                           # Negative // sonuc < 0  2223
            reviews_df_com['Tag'].values[t] = -1
            #print(colored(i, 'red'))

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

        #print(reviews_df_com.values[t])

    #print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))

    for i in attributes:
        df1 = reviews_df_com[reviews_df_com[i] == 1]    # Sadece ilgili atribute içeren reviewlerden bir df1
                                                        # oluşturuldu diğer sütun isimleri duruyır sadece stırlar elendi
        dfpos = len(df1[df1["Tag"] == 1])               # df1 den pos neg notr olnlar ayrıldı.
        dfneg = len(df1[df1["Tag"] == -1])
        dfnotr = len(df1[df1["Tag"] == 0])

        print(i, " : ", len(reviews_df_com[reviews_df_com[i] == 1]), "/", len(reviews_df_com.index), " rewiew is relevant")
        print(" + : ", dfpos,"/", len(reviews_df_com[reviews_df_com[i] == 1]))
        print(" - : ", dfneg,"/", len(reviews_df_com[reviews_df_com[i] == 1]))
        print(" 0 : ", dfnotr,"/", len(reviews_df_com[reviews_df_com[i] == 1]))
        print()
        #
        # # defining labels
        # activities = ['Positive', 'Negative', 'Notr']
        # slices = [dfpos, dfneg, dfnotr]
        # colors = ['g', 'r', 'y']
        # plt.pie(slices, labels=activities, colors=colors, startangle=90, explode=(0, 0.1, 0), radius=1.2, autopct='%1.1f%%')
        # plt.legend()
        # plt.show()



