import pandas as pd
from nltk import word_tokenize, pprint
from termcolor import colored
from colorama import Fore, Back, Style
import csv
import matplotlib.pyplot as plt

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

with open("C:/Users/Demir/Desktop/Final_Project/DataSets/adjectives.csv", encoding = "ISO-8859-1", ) as f:
    reader = csv.reader(f)                  # Read adjactives list from csv
    data = list(reader)                     # output: list of list, each row is a list which is in list.
adjList = sum(data, [])                     # list of list convert to list of string.
print(len(adjList))

# ---------------------- TAKING WORD WHICH ARE İNPUT FOR W2V AND FASTTEX FROM attributes.TXT ---------------------------
# attributes.TXT has a list of attributes which define to hotel. (it can be cahnge by users easily.)
outF = open("Dataset/txt files/attributes.txt", "r")
attributes = outF.readlines()  # Taking a str and put it in list[0] so we parse it from ,
attributes = attributes[0].split(",")  # Convert attributes to list.
print(attributes)

# ---------------------------------------------- Open/Read CSV File-------------------------------------------------------------
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")  # Read data. Important!
print('\t\t\t\t\t--------Hotels--------\n', reviews_df['Property Name'].unique())
isim = input("Please enter hotel name?")
reviews_df_com = reviews_df[(reviews_df['Property Name'] == isim)][['Review Text','Review Rating', 'Property Name']]
# reviews_df_com = reviews_df[['Review Text','Review Rating', 'Property Name']]

extraColumnName = ["Tag", "vaderStar"] + attributes
for index, columnName in enumerate(extraColumnName):
    reviews_df_com.insert((index+2), columnName, 0, True)
# ['My mother and myself..., 5, Hotel London, 1 0 0 0 1 0 0 1 1 0 1] DF has totally 15 column.
# [ 0.Colunm: belong to review. , 1.Col: "Review Rating" given by users, 1 to 5. , 2.Col: "Property Name" = Hotel Name ,
# 3.Col: "Tag" Using Vader (lexion based sentiment analysis method) find polarity of review. (1 0 -1) =  (+ - notr)
# Between 4-14 columns names like below(hotel, staff,....). That is hotels attributes which is defined by us. And this colums
# just take a value that is 0 or 1. For a review (row): if 4. column is 0, we get not to mensioned about staff at this review.
# And if 5. column is 1, we get there some thing about location because, this word : "location" is used in this review. ]

reviews_df_com = reviews_df_com.dropna().copy() # Remove emty review.
#reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.describe())

#------------------------------------------------SENTİMENT ANALYSES---------------------------------------------------
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()    # Create a SentimentIntensityAnalyzer object.
    score = sid_obj.polarity_scores(sentence)
    #print("Overall SA is : ", score)
    #print(sentence, score)
    return score["compound"]

# it doesn't matter whether the words are in sentence, or sentence is contains the words.
def findSubject(dizi,t):            # This function searchs that does the review has got input word or not.
    colName = str(dizi[0])          # if there is (any), set this column to 1
    for i in dizi:
        tokenReview = word_tokenize(reviews_df_com['Review Text'].values[t])
        if i in tokenReview:        # t : ilgili yorumun indisi sadece bir yoruma bakıyor
            reviews_df_com[colName].values[t] = 1

if __name__ == "__main__":
    k = sonuc = posNumber = negNumber = notrNumber = 0
    # attributes = ["hotel", "staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food", "restaurant"]

    # ------------------- W2V and Fasttex ile genişletilmiş olan kelimeleri alacağız. ------------------
    outF = open("Dataset/txt files/myOutFile1.txt", "r")
    listOfAttribute = outF.readlines()
    print(listOfAttribute)

    # ------------------ Create a matrix. it can be thought looks like txt. -----------------------------------------
    attMatrix = [[] for _ in range(len(attributes))]  # Create len(attributes) different list in list *important! write like this!
    # pprint(attMatrix)

    for i in range(len(attributes)):                  # Put attributes to matrix
        loa = listOfAttribute[i].split(",")           # taking listOfAttribute which was created by L_W2V_file. Convert it to a list.
        for a in loa:
            attMatrix[i].append(a)                    # Create a matrix each row is equals to 1 attributes(and similars) of hotel.
    # pprint(attMatrix)

    outF.close()

    #------------------------------ Vader -----------------------------------------
    for t in range(len(reviews_df_com)):                        # iterate for each object
        i = str(reviews_df_com['Review Text'].values[t])        # Take just reviews to String : i
        sonuc = sentiment_scores(i)     # İlgili yorumu i dizisine aldık şimdi yorumu SA yaptırıyoruz sonuçta compound dönüyor.
        #sentiment_scores(clean_text(i))
        sonucNolmal5 = round((((sonuc - (-1.0)) * (5.0 - 1.0)) / (1.0 - (-1.0))) + 1.0)
        reviews_df_com['vaderStar'].values[t] = sonucNolmal5

        # Given compound put in variable which name is sonuc then we will decide the review is positive, negtive
        # or notr. After we decide that, we set the "tag" columns like decided.
        if   sonuc > 0.05 :                                # Positive
            reviews_df_com['Tag'].values[t] = 1
        elif sonuc > -0.05 :                               # Nötr
            reviews_df_com['Tag'].values[t] = 0
        else:                                              # Negative // sonuc < -0.05
            reviews_df_com['Tag'].values[t] = -1
            # print(colored(i, 'red'), sonuc)

        for i in range(len(attributes)):  # Each attributes send to word2vectfonc fonction to use w2v and fasttex.
            findSubject(attMatrix[i], t)

        #print(reviews_df_com.values[t])

    print(reviews_df_com.pivot_table(index=['Tag'], aggfunc='size'))

    countGeneral = len(reviews_df_com.index)
    sumRatingGeneral = reviews_df_com['vaderStar'].sum(axis=0, skipna=True)  # Calculate for each attributes avarage score
    avgRatingGeneral = float(format(sumRatingGeneral / countGeneral, '.4f'))
    sumRatingUserGeneral = reviews_df_com['Review Rating'].sum(axis=0, skipna=True)  # Calculate for each attributes avarage score
    avgRatingUserGeneral = float(format(sumRatingUserGeneral / countGeneral, '.4f'))
    # avgRatingUserGeneral = 4.52
    print(Fore.YELLOW + "Avg Rating - Vader:{} User :{} Vader-User :{}".format(avgRatingGeneral, avgRatingUserGeneral,
                                                                             format(avgRatingGeneral - avgRatingUserGeneral, '.4f')))
    print()

    for i in attributes:
        df1 = reviews_df_com[reviews_df_com[i] == 1]    # Take just wanted attributes reviews into df1.
                                                        # (All column is still exist. Just irrelevant row delete.)
        dfpos  = len(df1[df1["Tag"] ==  1])               # The number of pos, neg and notr are calculated.
        dfneg  = len(df1[df1["Tag"] == -1])
        dfnotr = len(df1[df1["Tag"] ==  0])

        count = len(df1.index)
        sumRating = df1['vaderStar'].sum(axis=0, skipna = True)     # Calculate for each attributes avarage score
        avgRating = float(format(sumRating/count, '.4f'))

        sumRatingUser = df1['Review Rating'].sum(axis=0, skipna=True)  # Calculate for each attributes avarage score
        avgRatingUser = float(format(sumRatingUser / count, '.4f'))

        print(i, " : ", len(reviews_df_com[reviews_df_com[i] == 1]), "/", len(reviews_df_com.index), " rewiew is relevant. ", end="")
        print(Fore.BLUE + "Avg Rating - Vader:{} User :{} Vader-User :{}".format(avgRating, avgRatingUser, format(avgRating-avgRatingUser, '.4f')))

        print(Fore.GREEN  +  " + : {} / {} ".format(dfpos,  len(reviews_df_com[reviews_df_com[i] == 1])))
        print(Fore.YELLOW +  " 0 : {} / {} ".format(dfnotr, len(reviews_df_com[reviews_df_com[i] == 1])))
        print(Fore.RED    +  " - : {} / {} ".format(dfneg,  len(reviews_df_com[reviews_df_com[i] == 1])))
        print(Style.RESET_ALL)
        print()

        #-------------------------Graphic---------------------------
        # activities = ['Positive', 'Negative', 'Notr']
        # slices = [dfpos, dfneg, dfnotr]
        # colors = ['g', 'r', 'y']
        # plt.pie(slices, labels=activities, colors=colors, startangle=90, explode=(0, 0.1, 0), radius=1.2, autopct='%1.1f%%')
        # plt.legend()
        # plt.show()

    #----------------------- Print reviews colorful --------------
    print(attributes)
    look = look1 = input("Please, chose wanted review from above?")     # Take attributes name
    # look will pointer to point list of wanted word. look1 will use to divide dataFrame

    if attributes.index(look):
        indis = attributes.index(look)      # look = wanted list
        look = attMatrix[indis]
        print(look)
    else:
        print("Wrong choices")

    df2 = reviews_df_com[reviews_df_com[look1] == 1]                        # Divide just wanted department
    print(len(df2.index))
    for index, i in enumerate(df2['Review Text']):                          # Take review
        print(index, end='. ')
        i = word_tokenize(i)                                                # Tokenize review
        for t in i:                                                         # Take each token word
            if t in look:                                                   # if token word is one of the attributes
                print(colored(t, 'blue'), end=' ')                          # print blue
            elif t in adjList:                                              # Token is adjective, so if it is in adjactives.csv
                print(colored(t, 'green'), end=' ')                         # print green
            else:
                print(t, end=' ')                                           # any of above print token word like normal.
        print()
