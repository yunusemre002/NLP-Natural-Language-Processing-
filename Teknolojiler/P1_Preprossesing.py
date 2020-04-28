import pandas as pd

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/Hotel_Reviews_n15.csv")   # read data
reviews_df["review"] = reviews_df["Negative_Review"] + reviews_df["Positive_Review"] # append the positive and negative text reviews
reviews_df["is_bad_review"] = reviews_df["Reviewer_Score"].apply(lambda x: 1 if x < 5 else 0)   # create the label  # Yani 1 ler negtif 0 lar pozitif yorum oluyor.
reviews_df = reviews_df[["review", "is_bad_review"]]    # select only relevant columns # dataFrame'im sadece 2 kolondan müteşekkil artık. Yorumlar (Karışık ve 0/1 olduğu değerler.)
print(reviews_df.count())

reviews_df = reviews_df.sample(frac = 0.1, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
# random_state=42 ise bir seed oluşturu ve her random deyişimde yine aynı randomları seçer bunu çok iyi düşünmüşler. Böylelikle tekrarlanabilirlik sağlanmış olur.
# Eğer random_state kullanamsaydım her run edişimde farklı sampleler seçilecekti ve Stabil bir uygulamam olmayacaktı gibi.
reviews_df["review"] = reviews_df["review"].apply(lambda x: x.replace("No Negative", "").replace("No Positive", ""))    # remove 'No Negative' or 'No Positive' from text
print(reviews_df.count())

# return the wordnet object value corresponding to the POS tag
from nltk.corpus import wordnet

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

import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    print("")
    text = text.lower()    # lower text
    print("LOVER: ", text)
    text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    print("TOKENIZE: ", text)
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    print("ALFAPHE: ", text)
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens
    print("STOP: ", text)
    pos_tags = pos_tag(text)
    print("POS_TAG: ", pos_tags)# pos tag text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    print("LEMMA: ", text)
    text = [t for t in text if len(t) > 1]     # remove words with only one letter
    text = " ".join(text)    # join all
    return (text)

"""
text    : ['great', 'location', 'easy', 'access', 'buses', 'trains', 'anywhere', 'london']
pos_tag : [('great', 'JJ'), ('location', 'NN'), ('easy', 'JJ'), ('access', 'NN'), ('buses', 'NNS'), ('trains', 'NNS')]
lemmas  : ['great', 'location', 'easy', 'access', 'bus', 'train']"""

# clean text data
reviews_df["review_clean"] = reviews_df["review"].apply(lambda x: clean_text(x))