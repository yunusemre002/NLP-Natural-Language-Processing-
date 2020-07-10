from django.shortcuts import render
from .models import Post
from nltk import word_tokenize
from termcolor import colored
import csv, json, csv
import pandas as pd
from .models import Page
import random

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
hotelnames = []

df3= pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London2.csv", encoding = "ISO-8859-1", nrows = 1)  # read data !!!!!

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London2.csv", encoding = "ISO-8859-1")

with open("C:/Users/Demir/Desktop/Final_Project/DataSets/olumluAdj.csv", encoding = "ISO-8859-1")  as f:
    reader = csv.reader(f)  # Read adjactives list from csv
    data = list(reader)     # output: list of list, each row is a list which is in list.
posAdj = sum(data, [])     # list of list convert to list of string.
with open("C:/Users/Demir/Desktop/Final_Project/DataSets/olumsuzAdj.csv", encoding = "ISO-8859-1")  as f:
    reader = csv.reader(f)  # Read adjactives list from csv
    data = list(reader)     # output: list of list, each row is a list which is in list.
negAdj = sum(data, [])     # list of list convert to list of string.

# ------ TXT'den alınacak W2V ve Fasttext'ten gelecek olan attributelerin benzerleri okunuyor alttaki iki satırda. ----------
outF = open("C:/Users/Demir/Documents/GitHub/NLP-Natural-Language-Processing-/django_project/blog/inputs/myOutFile.txt", "r")
listOfAttribute = outF.readlines()

# ---------------------- TAKING WORD WHICH ARE İNPUT FOR W2V AND FASTTEX FROM attributes.TXT ---------------------------
# attributes.TXT has a list of attributes which define to hotel. (it can be cahnge by users easily.)
outF = open("C:/Users/Demir/Documents/GitHub/NLP-Natural-Language-Processing-/django_project/blog/inputs/attributes.txt", "r")
attributes = outF.readlines()  # Taking a str and put it in list[0] so we parse it from ,
attributes = attributes[0].split(",")  # Convert attributes to list.

attMatrix = [[] for _ in range(len(attributes))]  # Create len(attributes) different list in list *important! write like this!
allAttributes = []

for i in range(len(attributes)):             # Put attributes to matrix
    loa = listOfAttribute[i].split(",")      # taking listOfAttribute which was created by L_W2V_file. Convert it to a list.
    for a in loa:
        if '\n' in a:                        # When reading elements from txt, '\n'  also is added to end words .
            a = a[:-2]                       # Because of get rid of that, wrote this if condition. Delete 2 character end of str
            attMatrix[i].append(a)           # Create a list which contains full words of attributes for colored when print.(+similar) 
            allAttributes.append(a)          # Create a matrix each row is equals to 1 attributes(and similars) of hotel.
        else:
            attMatrix[i].append(a)          
            allAttributes.append(a)         # Create a matrix each row is equals to 1 attributes(and similars) of hotel.


def home(request):
    posG.clear()
    negG.clear()
    x.clear()
    scores.clear()
    counts.clear()
    kats.clear()
    hotelnames.clear()

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

        reviews_df_com = reviews_df[(reviews_df['Property Name'] == isim)][['Review Text', 'Review Rating', 'Property Name']]
        
        attMatrixGrafik = attMatrix
        attributesChart = attributes
        extraColumnName = ["Tag", "vaderStar"] + attributesChart
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
            sid_obj = SentimentIntensityAnalyzer()              # Create a SentimentIntensityAnalyzer object.
            score = sid_obj.polarity_scores(sentence)
            return score["compound"]

        # it doesn't matter whether the words are in sentence, or sentence is contains the words.
        def findSubject(dizi, t):               # This function searchs that does the review has got input word or not.
            colName = str(dizi[0])              # if there is (any), set this column to 1
            text = word_tokenize(reviews_df_com['Review Text'].values[t])
            for i in dizi:
                if i in text:  # t : ilgili yorumun indisi sadece bir yoruma bakıyor
                    reviews_df_com[colName].values[t] = 1

        k = sonuc = 0
      
        # ------------------------------ Vader -----------------------------------------
        for t in range(len(reviews_df_com)):                     # iterate for each object
            i = str(reviews_df_com['Review Text'].values[t])     # Take just reviews to String : i
            sonuc = sentiment_scores(i)  # İlgili yorumu i dizisine aldık şimdi yorumu SA yaptırıyoruz sonuçta compound dönüyor.
            sonucNolmal5 = round((((sonuc - (-1.0)) * (5.0 - 1.0)) / (1.0 - (-1.0))) + 1.0)
            reviews_df_com['vaderStar'].values[t] = sonucNolmal5

            if sonuc > 0.05:                            # Positive
                reviews_df_com['Tag'].values[t] = 1
            elif sonuc > -0.05:                         # Nötr
                reviews_df_com['Tag'].values[t] = 0
            else:                                       # Negative // sonuc < -0.05
                reviews_df_com['Tag'].values[t] = -1


            for i in range(len(attributesChart)):  # Each attributes send to word2vectfonc fonction to use w2v and fasttex.
                findSubject(attMatrixGrafik[i], t)

        x.append(len(reviews_df_com[reviews_df_com['Tag'] ==  1]))   # total positive of hotel review
        x.append(len(reviews_df_com[reviews_df_com['Tag'] == -1]))   # total negative of hotel review

        # print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))
        
        posGeneraldf  = reviews_df_com.loc[reviews_df_com['Tag'] ==  1]
        negGeneraldf  = reviews_df_com.loc[reviews_df_com['Tag'] == -1]
        notrGeneraldf = reviews_df_com.loc[reviews_df_com['Tag'] ==  0]  # select
        posGeneral  =  posGeneraldf['Review Text'].values.tolist()  # convert df to list
        negGeneral  =  negGeneraldf['Review Text'].values.tolist()
        notrGeneral = notrGeneraldf['Review Text'].values.tolist()
        
        for k in posGeneral:
            posG.append(k)
        for l in notrGeneral:
            notrG.append(l)
        for m in negGeneral:
            negG.append(m)
        
        for i in attributesChart:
            df1 = reviews_df_com[reviews_df_com[i] == 1]  # Take just wanted attributes reviews into df1.
            # (All column is still exist. Just irrelevant row delete.)
            dfpos  = len(df1[df1["Tag"] ==  1])  # The number of pos, neg and notr are calculated.
            dfneg  = len(df1[df1["Tag"] == -1])
            dfnotr = len(df1[df1["Tag"] ==  0])

            sumRating = df1['vaderStar'].sum(axis=0, skipna = True)     # Calculate for each attributes avarage score
            count = len(df1.index)
            if count!=0:
                avgRating = format(sumRating / count, '.4f')
            else:
                avgRating=0

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

        hotelnames.append(val1)

    else:
        print("a")

    return render(request, ['blog/grafik.html', 'blog/p_hotelRating.html'], {'hotelnames': hotelnames, 'array2': x })

def kategoriler(request):
    return render(request, 'blog/kategoriler.html',{'array2': kats})

# This string is used all yorum pages. Firstly list convert to str than send to yorum page like str. 
# Secondly it is parsed form brackets for converting to  list 
# allAttributesStr = '*-'.join([i for i in allAttributes])
negAdjStr = '*-'.join([i for i in negAdj])
posAdjStr = '*-'.join([i for i in posAdj])

def yorumlar(request):
    allAttributesStr = '*-'.join([i for i in allAttributes]) 
    global posG
    global negG
    if len(posG) > 25 :
        posG = random.choices(posG, k=25)
    
    if len(negG) > 25:
        negG = random.choices(negG, k=25)
    return render(request, 'blog/yorumlar.html',{'dizi':posG,'mizi':negG, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarhotel(request):
    d=attArama("hotel")
    allAttributesStr = '*-'.join([i for i in attMatrix[0]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarstaff(request):
    d=attArama("staff")
    allAttributesStr = '*-'.join([i for i in attMatrix[1]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarlocation(request):
    d=attArama("location")
    allAttributesStr = '*-'.join([i for i in attMatrix[2]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarroom(request):
    d=attArama("room")
    allAttributesStr = '*-'.join([i for i in attMatrix[3]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarbreakfast(request):
    d=attArama("breakfast")
    allAttributesStr = '*-'.join([i for i in attMatrix[4]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarbed(request):
    d=attArama("bed")
    allAttributesStr = '*-'.join([i for i in attMatrix[5]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative,'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarservice(request):
    d=attArama("service")
    allAttributesStr = '*-'.join([i for i in attMatrix[6]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarbathroom(request):
    d=attArama("bathroom")
    allAttributesStr = '*-'.join([i for i in attMatrix[7]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarview(request):
    d=attArama("view")
    allAttributesStr = '*-'.join([i for i in attMatrix[8]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarfood(request):
    d=attArama("food")
    allAttributesStr = '*-'.join([i for i in attMatrix[9]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})
def yorumlarrestaurant(request):
    d=attArama("restaurant")
    allAttributesStr = '*-'.join([i for i in attMatrix[10]])
    return render(request, 'blog/yorumlar.html',{'dizi':positive,'mizi':negative, 'negAdjStr': negAdjStr , 'posAdjStr': posAdjStr, 'allAttributesStr' : allAttributesStr})

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

outF.close()