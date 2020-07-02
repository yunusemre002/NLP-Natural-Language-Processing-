from django.shortcuts import render
# from django.http import HttpResponse neden gerek kalmadı?
from .models import Post
from .models import Page
#from .urls import rety
import json



postsaaa = [
    {'author': 'CoreyMS','title': 'Blog Post 1','content': 'First post content','date_posted': 'August 27, 2018'},
    {'author': 'Jane Doe','title': 'Blog Post 2','content': 'Second post content','date_posted': 'August 28, 2018'}]

x=[]
global run1
run1=0
y=[]
scores=[]
counts=[]
dizim=[]
dizim2=[]
kats=[]

import pandas as pd
from nltk import word_tokenize
from termcolor import colored
import csv

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")   # read data !!!!!

def home(request):
    hotel_names = reviews_df['Property Name'].unique()
    context = {
        'posts': Post.objects.all(), 
        'hotel_names': hotel_names
    }
    return render(request, 'blog/home.html',context)

def grafik(request):
    x.clear()
    scores.clear()
    counts.clear()
    val1 = (request.POST['num1'])

    with open("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1") as f:
        reader = csv.reader(f)  # Read adjactives list from csv
        data = list(reader)  # output: list of list, each row is a list which is in list.
    adjList = sum(data, [])  # list of list convert to list of string.

    #val1='City View Hotel'
    isim = val1
    print(val1)
    reviews_df_com = reviews_df[(reviews_df['Property Name'] == isim)][
        ['Review Text', 'Review Rating', 'Property Name']]
    # reviews_df_com = reviews_df[['Review Text','Review Rating', 'Property Name']]

    extraColumnName = ["Tag", "hotel", "staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view",
                       "food", "restaurant"]
    for index, columnName in enumerate(extraColumnName):
        reviews_df_com.insert((index + 2), columnName, 0, True)
    # ['My mother and myself..., 5, Hotel London, 1 0 0 0 1 0 0 1 1 0 1] DF has totally 15 column.
    # [ 0.Colunm: belong to review. , 1.Col: "Review Rating" given by users, 1 to 5. , 2.Col: "Property Name" = Hotel Name ,
    # 3.Col: "Tag" Using Vader (lexion based sentiment analysis method) find polarity of review. (1 0 -1) =  (+ - notr)
    # Between 4-14 columns names like below(hotel, staff,....). That is hotels attributes which is defined by us. And this colums
    # just take a value that is 0 or 1. For a review (row): if 4. column is 0, we get not to mensioned about staff at this review.
    # And if 5. column is 1, we get there some thing about location because, this word : "location" is used in this review. ]

    reviews_df_com = reviews_df_com.dropna().copy()  # Remove emty review.
    # reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
    print(reviews_df_com.describe())

    # ------------------------------------------------SENTİMENT ANALYSES---------------------------------------------------
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    def sentiment_scores(sentence):
        sid_obj = SentimentIntensityAnalyzer()  # Create a SentimentIntensityAnalyzer object.
        score = sid_obj.polarity_scores(sentence)
        # print("Overall SA is : ", score)
        # print(sentence, score)
        return score["compound"]

    # it doesn't matter whether the words are in sentence, or sentence is contains the words.
    def findSubject(dizi, t):  # This function searchs that does the review has got input word or not.
        colName = str(dizi[0])  # if there is (any), set this column to 1
        for i in dizi:
            if i in reviews_df_com['Review Text'].values[t]:  # t : ilgili yorumun indisi sadece bir yoruma bakıyor
                reviews_df_com[colName].values[t] = 1

    k = sonuc = posNumber = negNumber = notrNumber = basarili = basarisiz = 0
    attributes = ["hotel", "staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food",
                  "restaurant"]

    hotel = ["hotel", "otel", "motel", "hotels", 'accommodation']
    staff = ["staff", 'team', 'employee', 'everyone', 'host', 'staf', 'staffer', 'staffmember']
    loc = ["location", 'position', 'located', 'spot', 'locatie', 'located', 'localisation']
    room = ["room", 'bedroom', 'rooom', 'roooms']
    breakfast = ["breakfast", 'breackfast', 'breakfeast', 'breakfats', 'brekfast', 'breakfest', 'bfast']
    bed = ["bed", 'pillow', 'mattress', 'chair', 'bedding', 'bedsheets', 'beds']
    service = ["service", 'sevice', 'presentation', 'deliver', 'housekeep', 'seervice', 'roomservice', 'servicing']
    bath = ["bathroom", 'bathrooms', 'bath', 'bathtub', 'shower', 'tub', 'toilet', 'bathrooom', 'bathrom']
    view = ["view", 'overlook', 'views', 'viewing', 'vieuw', 'viewpoint', 'overview']
    food = ["food", 'meal', 'dish', 'menu', 'lunch', 'dinner']
    rest = ["restaurant", 'restaurants', 'restaruant', 'eatery', 'dining', 'restuarant', 'hotelrestaurant']

    # ------------------------------ Vader -----------------------------------------
    for t in range(len(reviews_df_com)):  # iterate for each object
        i = str(reviews_df_com['Review Text'].values[t])  # Take just reviews to String : i

        sonuc = sentiment_scores(
            i)  # İlgili yorumu i dizisine aldık şimdi yorumu SA yaptırıyoruz sonuçta compound dönüyor.
        # sentiment_scores(clean_text(i))

        if sonuc > 0.05:  # Positive
            reviews_df_com['Tag'].values[t] = 1
            basarili += 1
        elif sonuc > -0.05:  # Nötr
            reviews_df_com['Tag'].values[t] = 0
        else:  # Negative // sonuc < -0.05
            reviews_df_com['Tag'].values[t] = -1
            basarisiz += 1
            # print(colored(i, 'red'), sonuc)

        findSubject(hotel, t)
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

    x.append(basarili)
    x.append(basarisiz)
    print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))

    for i in attributes:
        df1 = reviews_df_com[reviews_df_com[i] == 1]  # Take just wanted attributes reviews into df1.
        # (All column is still exist. Just irrelevant row delete.)
        dfpos = len(df1[df1["Tag"] == 1])  # The number of pos, neg and notr are calculated.
        dfneg = len(df1[df1["Tag"] == -1])
        dfnotr = len(df1[df1["Tag"] == 0])

        sumRating = df1['Review Rating'].sum(axis=0, skipna=True)  # Calculate for each attributes avarage score
        count = len(df1.index)
        if count!=0:
            avgRating = format(sumRating / count, '.4f')
        else:
            avgRating=0
        print(i, " : ", len(reviews_df_com[reviews_df_com[i] == 1]), "/", len(reviews_df_com.index),
              " rewiew is relevant.", "Avarage Rating:", avgRating)
        scores.append(round(float(avgRating),1))
        counts.append(len(reviews_df_com[reviews_df_com[i] == 1]))
        print(" + : {} / {} ".format(dfpos,  len(reviews_df_com[reviews_df_com[i] == 1])))
        print(" 0 : {} / {} ".format(dfnotr, len(reviews_df_com[reviews_df_com[i] == 1])))
        print(" - : {} / {} ".format(dfneg,  len(reviews_df_com[reviews_df_com[i] == 1])))
        kats.append(dfpos)
        kats.append(dfneg)


    # ----------------------- Print reviews colorful --------------
    print(attributes)
    look = look1 = "hotel"  # Take attributes name
    # look will pointer to point list of wanted word
    if look == 'hotel':
        look = hotel  # look1 will use to divide dataFrame
    elif look == 'staff':
        look = staff  # look = wanted list
    elif look == 'location':
        look = loc
    elif look == 'room':
        look = room
    elif look == 'breakfast':
        look = breakfast
    elif look == 'bed':
        look = bed
    elif look == 'service':
        look = service
    elif look == 'bathroom':
        look = bath
    elif look == 'view':
        look = view
    elif look == 'food':
        look = food
    elif look == 'restaurant':
        look = rest
    else:
        print("Wrong choices")

    df2 = reviews_df_com[reviews_df_com[look1] == 1]  # Divide just wanted department
    print(len(df2.index))
    for index, i in enumerate(df2['Review Text']):  # Take review
        print(index, end='. ')

        dizim2.append(i)
        i = word_tokenize(i)
        # Tokenize review
        # for t in i:  # Take each token word
        #     if t in adjList:  # Token is adjective, so if it is in adjactives.csv
        #         print(t, end=' ')  # any of above print token word like normal.
        # print()
    #x[0] basarili x[1] basarisiz x[2]-x[12] kategori puanları
    x.append(scores[0])
    x.append(scores[1])
    x.append(scores[2])
    x.append(scores[3])
    x.append(scores[4])
    x.append(scores[5])
    x.append(scores[6])
    x.append(scores[7])
    x.append(scores[8])
    x.append(scores[9])
    x.append(scores[10])
    ort=0
    rev_count=0
    for ali,veli in zip(range(len(scores)),range(len(counts))):
        rev_count+=counts[veli]
        ort=ort+(scores[ali]*counts[veli])
    print(ort/rev_count)
    ort=round(ort/rev_count,2)
    x.append(ort)
    # kats[21] kategorilerin yüzdeleri
    gg=[] #otel ismi
    gg.append(val1)
    return render(request, ['blog/grafik.html', 'blog/p_hotelRating.html'],{'array1':val1,'array2':x})


def bos(request):
    son2()
    return render(request, 'blog/bos.html',{'dizi':dizim2})
def olumlu(request):
    return render(request, 'blog/olumlu.html',{'title': 'Olumlu'})
def kategoriler(request):
    return render(request, 'blog/kategoriler.html',{'array2': kats})

def yorumlar(request):
    #son2()
    lale=[]
    lale.append('ali')
    lale.append('mehmet')
    return render(request, 'blog/yorumlar.html',{'dizi':dizim2})


def yorumlar12(request):

    x = [99] * 7
    context = {
        'pages': x       #yeşil olan posts'u diğer html'de yönlendirme için kullanacağım
    }
    return render(request, 'blog/yorumlar.html',context)

