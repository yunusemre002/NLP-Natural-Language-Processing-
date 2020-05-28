# lines = """delete acxount license key wordpress license when to add new apps""".splitlines()
# for line in lines:
#     word_count.update(line.split())
# print(word_count)
# The function is fundamental function.

import re
from collections import Counter
import pandas as pd
word_count = Counter()

# import for preproccessing
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()

# open csv file
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text']]
#reviews_df_com = reviews_df_com.sample(frac=0.01, replace=False, random_state=42)  # Yorumların %01'ini işle.

# Preproccessing işlemi ile tüm metni "pos" isimli bir liste atıyoruz.
res = ""
pos = []
for i in reviews_df_com["Review Text"]:
    pletters = re.sub('[^a-zA-Z]', ' ', i)
    ptokens = nltk.word_tokenize(pletters)
    plowercase = [l.lower() for l in ptokens]
    pfiltered_presult = list(filter(lambda l: l not in stop_words, plowercase))
    plemmas = [wordnet_lemmatizer.lemmatize(t) for t in pfiltered_presult]
    pos.append(' '.join(plemmas))

# pos isimli listi tek bir stringe çevirdik
for i in pos:
    res = " ".join((res, i))
#print(res)

# String üzerinde WordCount uyguladık.
word_count.update(res.split())
#print(word_count)
print(word_count.most_common(30)) # ilk 30 u yazdır.

for i in word_count.most_common(40):
    print(i)
