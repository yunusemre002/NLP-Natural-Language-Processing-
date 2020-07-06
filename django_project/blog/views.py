from django.shortcuts import render
from .models import Post
from nltk import word_tokenize
from termcolor import colored
import csv, json, csv
import pandas as pd
from .models import Page

x=[]
scores=[]
counts=[]
dizim=[]
dizim2=[]
kats=[]
posG= []
negG= []
notrG=[]
positiveAttdf = []
positiveAtt = []
positive = []
negativeAttdf = []
negativeAtt = []
negative = []
notrAttdf = []
notrAtt = []
notr=[]


df3= pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")  # read data !!!!!

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")
with open("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")  as f:
    reader = csv.reader(f)  # Read adjactives list from csv
    data = list(reader)     # output: list of list, each row is a list which is in list.
adjList = sum(data, [])     # list of list convert to list of string.


def home(request):
    posG.clear()
    negG.clear()
    x.clear()
    scores.clear()
    counts.clear()
    kats.clear()

    hotel_names = reviews_df['Property Name'].unique()
    context = {
        'posts': Post.objects.all(), 
        'hotel_names': hotel_names
    }
    return render(request, 'blog/home.html',context)

def grafik(request):
    if not x:
        val1 = (request.POST['num1'])
        isim = val1
        print(val1)

        reviews_df_com = reviews_df[(reviews_df['Property Name'] == isim)][['Review Text', 'Review Rating', 'Property Name']]
        extraColumnName = ["Tag", "vaderStar", "hotel", "staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view",
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

        # ------------------------------------------------SENTİMENT ANALYSES---------------------------------------------------
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        def sentiment_scores(sentence):
            sid_obj = SentimentIntensityAnalyzer()  # Create a SentimentIntensityAnalyzer object.
            score = sid_obj.polarity_scores(sentence)
            return score["compound"]

        # it doesn't matter whether the words are in sentence, or sentence is contains the words.
        def findSubject(dizi, t):   # This function searchs that does the review has got input word or not.
            colName = str(dizi[0])  # if there is (any), set this column to 1
            for i in dizi:
                if i in reviews_df_com['Review Text'].values[t]:  # t : ilgili yorumun indisi sadece bir yoruma bakıyor
                    reviews_df_com[colName].values[t] = 1

        k = sonuc = posNumber = negNumber = notrNumber = chartpos = chartneg = 0
        attributes = ["hotel", "staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food", "restaurant"]

        hotel     = ["hotel", "otel", "motel", "hotels", 'accommodation']
        staff     = ["staff", 'team', 'employee', 'everyone', 'host', 'staf', 'staffer', 'staffmember']
        loc       = ["location", 'position', 'located', 'spot', 'locatie', 'located', 'localisation']
        room      = ["room", 'bedroom', 'rooom', 'roooms']
        breakfast = ["breakfast", 'breackfast', 'breakfeast', 'breakfats', 'brekfast', 'breakfest', 'bfast']
        bed       = ["bed", 'pillow', 'mattress', 'chair', 'bedding', 'bedsheets', 'beds']
        service   = ["service", 'sevice', 'presentation', 'deliver', 'housekeep', 'seervice', 'roomservice', 'servicing']
        bath      = ["bathroom", 'bathrooms', 'bath', 'bathtub', 'shower', 'tub', 'toilet', 'bathrooom', 'bathrom']
        view      = ["view", 'overlook', 'views', 'viewing', 'vieuw', 'viewpoint', 'overview']
        food      = ["food", 'meal', 'dish', 'menu', 'lunch', 'dinner']
        rest      = ["restaurant", 'restaurants', 'restaruant', 'eatery', 'dining', 'restuarant', 'hotelrestaurant']

        # ------------------------------ Vader -----------------------------------------
        for t in range(len(reviews_df_com)):  # iterate for each object
            i = str(reviews_df_com['Review Text'].values[t])  # Take just reviews to String : i
            sonuc = sentiment_scores(i)  # İlgili yorumu i dizisine aldık şimdi yorumu SA yaptırıyoruz sonuçta compound dönüyor.
            sonucNolmal5 = round((((sonuc - (-1.0)) * (5.0 - 1.0)) / (1.0 - (-1.0))) + 1.0)
            reviews_df_com['vaderStar'].values[t] = sonucNolmal5

            if sonuc > 0.05:  # Positive
                reviews_df_com['Tag'].values[t] = 1
                chartpos += 1
            elif sonuc > -0.05:  # Nötr
                reviews_df_com['Tag'].values[t] = 0
            else:  # Negative // sonuc < -0.05
                reviews_df_com['Tag'].values[t] = -1
                chartneg += 1

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

        x.append(chartpos)    # İlk 
        x.append(chartneg)
        # print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))
        
        posGeneraldf = reviews_df_com.loc[reviews_df_com['Tag'] == 1]
        negGeneraldf = reviews_df_com.loc[reviews_df_com['Tag'] == -1]
        notrGeneraldf = reviews_df_com.loc[reviews_df_com['Tag'] == 0]  # select
        posGeneral = posGeneraldf['Review Text'].values.tolist()  # convert df to list
        negGeneral = negGeneraldf['Review Text'].values.tolist()
        notrGeneral = notrGeneraldf['Review Text'].values.tolist()
        
        for k in range(len(posGeneral)):
            posG.append(posGeneral[k])
        for l in range(len(notrGeneral)):
            notrG.append(notrGeneral[l])
        for m in range(len(negGeneral)):
            negG.append(negGeneral[m])
        
        for i in attributes:
            df1 = reviews_df_com[reviews_df_com[i] == 1]  # Take just wanted attributes reviews into df1.
            # (All column is still exist. Just irrelevant row delete.)
            dfpos = len(df1[df1["Tag"] == 1])  # The number of pos, neg and notr are calculated.
            dfneg = len(df1[df1["Tag"] == -1])
            dfnotr = len(df1[df1["Tag"] == 0])

            sumRating = df1['vaderStar'].sum(axis=0, skipna = True)     # Calculate for each attributes avarage score
            count = len(df1.index)
            if count!=0:
                avgRating = format(sumRating / count, '.4f')
            else:
                avgRating=0

            # print(i, " : ", len(reviews_df_com[reviews_df_com[i] == 1]), "/", len(reviews_df_com.index),
            #             " rewiew is relevant." , "Avarage Rating:",avgRating )
            # print(" + : {} / {} ".format(dfpos,  len(reviews_df_com[reviews_df_com[i] == 1])))
            # print(" 0 : {} / {} ".format(dfnotr, len(reviews_df_com[reviews_df_com[i] == 1])))
            # print(" - : {} / {} ".format(dfneg,  len(reviews_df_com[reviews_df_com[i] == 1])))

            scores.append(round(float(avgRating),1))
            counts.append(len(reviews_df_com[reviews_df_com[i] == 1]))
            kats.append(dfpos)
            kats.append(dfneg)
            
        global df3
        df3 = pd.DataFrame(None)
        df3=reviews_df_com.copy()
        # Eşlenik toplamı
        for i in range(len(scores)):        #x[0] basarili x[1] basarisiz x[2]-x[12] kategori puanları
            x.append(scores[i])

        ort=rev_count=0
        for scr,cnt in zip(range(len(scores)),range(len(counts))):
            rev_count+=counts[cnt]
            ort=ort+(scores[scr]*counts[cnt])
        ort=round(ort/rev_count,2)
        x.append(ort)                   # x[13]

        hotelname = val1

        context = {
            'hotelname': hotelname,
            'array2': x
        }

    else:
        print("a")

    return render(request, ['blog/grafik.html', 'blog/p_hotelRating.html'], context)


def kategoriler(request):
    return render(request, 'blog/kategoriler.html',{'array2': kats})

def yorumlar(request):
    print(posG[0])
    print(negG[0])
    return render(request, 'blog/yorumlar.html',{'dizi':posG,'mizi':negG})

def yorumlarhotel(request):
    d=attArama("hotel")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarstaff(request):
    d=attArama("staff")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarlocation(request):
    d=attArama("location")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarroom(request):
    d=attArama("room")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarbreakfast(request):
    d=attArama("breakfast")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarbed(request):
    d=attArama("bed")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarservice(request):
    d=attArama("service")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarbathroom(request):
    d=attArama("bathroom")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarview(request):
    d=attArama("view")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarfood(request):
    d=attArama("food")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})
def yorumlarrestaurant(request):
    d=attArama("restaurant")
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative})

def attArama(attName):
    positive.clear()
    negative.clear()
    notr.clear()
    df4 = df3[df3[attName] == 1]  # Divide just wanted department
    positiveAttdf = df4.loc[df4['Tag'] == 1]
    positiveAtt = positiveAttdf['Review Text'].values.tolist()  # convert df to list
    for k in range(len(positiveAtt)):
        positive.append(positiveAtt[k])
    negativeAttdf = df4.loc[df4['Tag'] == -1]
    negativeAtt = negativeAttdf['Review Text'].values.tolist()
    for l in range(len(negativeAtt)):
        negative.append(negativeAtt[l])
    notrAttdf = df4.loc[df4['Tag'] == 0]
    notrAtt = notrAttdf['Review Text'].values.tolist()
    for m in range(len(notrAtt)):
        notr.append(notrAtt[m])
    c=0
    return c

