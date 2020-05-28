import gensim as gensim
import nltk
import pandas as pd

#-------------Clean_text_new()----------------------
from gensim.models import FastText
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()
#---------------------------------------------------

# 1. reviews_df = pd.read_csv("file.cvs", encoding = "ISO-8859-1" )  önemli
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text','Review Rating']]
reviews_df_com.insert(2,'Tag', 0, True)
reviews_df_com.insert(3, 'staff', 0, True)
reviews_df_com.insert(4, 'location', 0, True)
reviews_df_com.insert(5, 'room', 0, True)
reviews_df_com.insert(6, 'breakfast', 0, True)
reviews_df_com.insert(7, 'bed', 0, True)
reviews_df_com.insert(8, 'service', 0, True)
reviews_df_com.insert(9, 'bathroom', 0, True)
reviews_df_com.insert(10, 'view', 0, True)
reviews_df_com.insert(11, 'food', 0, True)
reviews_df_com.insert(12, 'restaurant', 0, True)
# ['My cat ... 5 1 0 0 0 1 0 0 1 1 0 1] DF toplam 13 column. 2.S, user's star: 5/5. 3-13.S Vader  (1 0 -1) = + nötr -.

reviews_df_com = reviews_df_com.dropna().copy() # boş yorum varsa kaldırır.
# reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Yorumların %01'ini =  150/15000 taneyi işle.
print(reviews_df_com.describe())


#------------------------------------------------PREPROCCESSİNG---------------------------------------------------
from nltk.corpus import wordnet
import string
from nltk import pos_tag, re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
    text =str(text)
    text = text.lower()    # lower text
    #text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = nltk.word_tokenize(text)
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens
    pos_tags = pos_tag(text)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    text = [t for t in text if len(t) > 1]     # remove words with only one letter
    return (text)

def clean_text_new(text):
    pletters = re.sub('[^a-zA-Z]', ' ', text)
    ptokens = nltk.word_tokenize(pletters)
    plowercase = [l.lower() for l in ptokens]
    pfiltered_presult = list(filter(lambda l: l not in stop_words, plowercase))
    plemmas = [wordnet_lemmatizer.lemmatize(t) for t in pfiltered_presult]
    return plemmas


def word2vectfonc(kdizi, k):
    print(str(k) + ". Most similar to {0}".format(kdizi), model.wv.most_similar(positive=kdizi, topn=20))
    dizi = model.wv.most_similar(positive=kdizi, topn=20)
    for i in dizi:
        kdizi.append(i[0])

if __name__ == "__main__":
    k = sonuc = posNumber = negNumber = notrNumber = 0
    attributes = ["staff", "location", "room", "breakfast", "bed", "service", "bathroom", "view", "food", "restaurant"]

    # Bunları word to vect ile genişleteceğiz.
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

    #---------------------------- Word2Vec ----------------------------------
    top = []
    for i in reviews_df_com["Review Text"]:
        top.append(clean_text_new(i))     #top.append(text)  # şu okadar önemliki anlayamazsınız :)
    #print(top)

    #----------------------- Word2Vect kullanarak---------------
    # model = gensim.models.Word2Vec(top, size=150, window=10, min_count=2, workers=10)
    # model.train(top, total_examples=len(top), epochs=10)

    # ----------------------- Fasttext kullanarak---------------
    model = FastText(size=170, window=10, min_count=2, workers=10)  # instantiate
    model.build_vocab(sentences=top)
    model.train(sentences=top, total_examples=len(top), epochs=10)  # train


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