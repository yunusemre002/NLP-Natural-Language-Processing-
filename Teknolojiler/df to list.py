import re, nltk, seaborn
import pandas as pd
from operator import itemgetter
from collections import OrderedDict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()

df = pd.read_csv('C:/Users/Demir/PycharmProjects/untitled11/venv/Include/Others/datasets/Hotel_Reviews_n15.csv')
df_com = df[['Hotel_Name', 'Reviewer_Score', 'Negative_Review', 'Review_Total_Negative_Word_Counts', 'Positive_Review','Review_Total_Positive_Word_Counts', 'Total_Number_of_Reviews', 'Total_Number_of_Reviews_Reviewer_Has_Given']]

neg = []
for i in df_com['Negative_Review']:
    letters = re.sub('[^a-zA-Z]', ' ', i)  #sadece harflerden oluşsun noktalamaları/sayıları kaldır.
    tokens = nltk.word_tokenize(letters)  # herbir kelimeyi ayrı birer string yapar kelimeler listesi yapar
    lowercase = [l.lower() for l in tokens]
    filtered_result = list(filter(lambda l: l not in stop_words, lowercase))
    lemmas = [wordnet_lemmatizer.lemmatize(t) for t in filtered_result]   #hiçbişi yapmıyor :) sondaki çoğul eki kaldırması beklenir ama gidip us un s sini kaldırır :)
    neg.append(' '.join(lemmas))  #dizinin sonuna ekle

#-----------------------------------------Kelime Sayaci------------------------------------------------------------

def convert(lst):
    return ([i for item in lst for i in item.split()])
# Driver code
say = convert(neg)

wordcount = {}
for word in say:
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

sorted_x = OrderedDict(sorted(wordcount.items(), key=itemgetter(1)))
for key in sorted_x.keys():
    if sorted_x[key] > 600:
        print("%s %s " % (key, sorted_x[key]))
###Kelime Sayma