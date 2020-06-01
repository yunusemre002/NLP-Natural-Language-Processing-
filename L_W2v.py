import pandas as pd
from nltk import pos_tag, re, word_tokenize
from gensim.models import FastText, Word2Vec
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
stop_words = set(stopwords.words('english'))

#-------------------------------------------------Import Data from CSV-------------------------------------------------------
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")  # Read data !!!!
reviews_df_com = reviews_df[['Review Text']]                                        # Remove except for  "Review Text"
reviews_df_com = reviews_df_com.dropna().copy()                                     # Remove empty reviews ,if there is.
#reviews_df_com = reviews_df_com.sample(frac=0.01, replace=False, random_state=42)  # Take %01 of reviews.
print(reviews_df_com.describe())

#------------------------------------------------PREPROCCESSİNG---------------------------------------------------
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
    text = text.lower()    # lower text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = word_tokenize(text)
    text = [x for x in text if x not in stop_words]     # remove stop words
    pos_tags = pos_tag(text)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    # text = [WordNetLemmatizer().lemmatize(t) for t in text]                                 # Other option of lemmatizer
    text = [t for t in text if len(t) > 1]     # remove words with only one letter or empty
    return (text)

# ------------------------------- Find and Print---------------------------------
def word2vectfonc(kdizi, k):
    dizi = list(model.wv.most_similar(positive=kdizi, topn=10))  # function return tuple. To chance it, convert to list.
    for i in range(len(dizi)):
        d = list(dizi[i])                                        # dizi[i] is tuple, so converted.
        d[1] = format(d[1], '.4f')                               # just take .0000 (4 decimal after dot.)
        dizi[i] = tuple(d)                                        # reformat to tuple
    print(str(k) + ". Most similar to {0}".format(kdizi), dizi)

if __name__ == "__main__":
    # These lists extends using W2V and Fasttext
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

    #-------------------------- Preproccessing ----------------------------------
    reviews = []
    for i in reviews_df_com["Review Text"]:
        reviews.append(clean_text(i))     #top.append(text)  # That is very IMPORTANT !!! :)

    # --------------------------- Word2Vect ----------------------------------
    model = Word2Vec(reviews, size=150, window=10, min_count=2, workers=10)
    model.train(reviews, total_examples=len(reviews), epochs=10)

    # ---------------------------- Fasttext ----------------------------------
    # model = FastText(size=170, window=10, min_count=2, workers=10)  # instantiate
    # model.build_vocab(sentences=reviews)
    # model.train(sentences=reviews, total_examples=len(reviews), epochs=10)  # train

    word_vectors = model.wv

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
