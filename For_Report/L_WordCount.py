#This program take a csv and calculate wordcount
import pandas as pd
from collections import Counter
word_count = Counter()
import re, nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Open csv file
reviews_df = pd.read_csv("C:/Users/Demir/Documents/GitHub/NLP-Natural-Language-Processing-/DataSet/London2.csv", encoding = "ISO-8859-1")   # read data !!!!!
reviews_df = reviews_df[reviews_df['Review Text'].str.contains("<U") == False] # Remove some reviews created full of unknown characters.
reviews_df_com = reviews_df[['Review Text']]
reviews_df_com = reviews_df_com.sample(frac=0.01, replace=False, random_state=42)  # Use  %01 of reviews.

# Preprocessing: All reviews  go into list which name is "text".
stringReviews = ""                                                # Create a String
text = []                                                         # Create a List
for review in reviews_df_com["Review Text"]:
    letters = re.sub('[^a-zA-Z]', ' ', review)                   # Remove everything which is not character from review.
    tokens = nltk.word_tokenize(letters)                         # ['Hotel', 'is', 'GOOD']
    lowercase = [l.lower() for l in tokens]                      # ['hotel', 'is', 'good']
    removeOneCharacter = [i for i in lowercase if len(i) > 2]    # Remove words whom below then 2 character.
    filtered_result = list(filter(lambda l: l not in stop_words, removeOneCharacter))
    text.append(' '.join(filtered_result))

# Convert list(name is text) to String(name is stringReviews)
for i in text:
    stringReviews = " ".join((stringReviews, i))

# Run WordCount Function on String of reviews.
word_count.update(stringReviews.split())

# print(word_count)                     # print all of them
print(word_count.most_common(30))       # Print first 30 member
for i in word_count.most_common(30):    # Print first 30 member one under the other.
    print(i)

# This example belongs to the fundemental function.
# lines = """delete acxount license key wordpress license when to add new apps""".splitlines()
# for line in lines:
#     word_count.update(line.split())
# print(word_count)
