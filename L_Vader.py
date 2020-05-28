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
reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.describe())

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

if __name__ == "__main__":
    k = sonuc = posNumber = negNumber = notrNumber = 0
    attributes = ["staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food", "restaurant"]

    # #Bunları word to vect ile genişleteceğiz.
    # staff = ["staff"]
    # loc = ["location"]
    # room = ["room"]
    # breakfast = ["breakfast"]
    # bed = ["bed"]
    # service = ["service"]
    # bath = ["bathroom"]
    # view = ["view"]
    # food = ["food"]
    # rest = ["restaurant"]

    # This outputs created by us. It is handmade but when it was created, W2V and Fasttext algorithms used (in L_W2V.pf).
    staff = ["staff", 'team', 'employee', 'everyone', 'host', 'staf', 'staffer', 'staffmember']
    loc = ["location", 'position', 'located', 'spot', 'locatie', 'located', 'localisation']
    room = ["room", 'bedroom', 'rooom', 'roooms']
    breakfast = ["breakfast", 'breackfast', 'breakfeast', 'breakfats', 'brekfast', 'breakfest', 'bfast']
    bed = ["bed", 'pillow', 'mattress', 'chair', 'bedding', 'bedsheets', 'beds']
    service = ["service", 'sevice', 'presentation', 'deliver', 'housekeep', 'seervice', 'roomservice', 'servicing']
    bath = ["bathroom", 'bathrooms', 'bath', 'bathtub', 'shower', 'tub', 'toilet', 'bathrooom', 'bathrom']
    view = ["view", 'overlook',  'views', 'viewing', 'vieuw', 'viewpoint', 'overview']
    food = ["food", 'meal', 'dish', 'menu', 'lunch', 'dinner']
    rest = ["restaurant", 'restaurants', 'restaruant', 'eatery', 'dining', 'restuarant', 'hotelrestaurant']

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

        #-------------------------Graphic---------------------------
        activities = ['Positive', 'Negative', 'Notr']
        slices = [dfpos, dfneg, dfnotr]
        colors = ['g', 'r', 'y']
        plt.pie(slices, labels=activities, colors=colors, startangle=90, explode=(0, 0.1, 0), radius=1.2, autopct='%1.1f%%')
        plt.legend()

        plt.show()



