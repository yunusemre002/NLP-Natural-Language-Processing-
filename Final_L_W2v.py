import pandas as pd
from nltk import pos_tag, re, word_tokenize, pprint
from gensim.models import FastText, Word2Vec
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
stop_words = set(stopwords.words('english'))

import time
start_time = time.time()
print("%s" % (time.time()-start_time))

#-------------------------------------------------Import Data from CSV--------------------------------------------------------
reviews_df_com = pd.read_csv("C:/Users/Demir/Documents/GitHub/NLP-Natural-Language-Processing-/Dataset/London2.csv",
                             usecols=['Review Text'] ,encoding = "ISO-8859-1")  # Read data!  # Take Just "Review Text" column
reviews_df_com = reviews_df_com.dropna().copy()                                 # Remove empty reviews ,if there is.
# reviews_df_com = reviews_df_com.sample(frac=0.01, replace=False, random_state=42)  # Take %01 of reviews.
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
    text = text.lower()                                 # lower text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = word_tokenize(text)
    text = [x for x in text if x not in stop_words]     # remove stop words
    pos_tags = pos_tag(text)                            # ('park', 'NN'), ('london', 'JJ') -> NN = Noun, JJ = adj.
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    # text = [WordNetLemmatizer().lemmatize(t) for t in text]                                # Other option of lemmatizer
    text = [t for t in text if len(t) > 1]     # remove words with only one letter or empty
    return (text)

# ------------------------------- Find and Print---------------------------------
def word2vectfonc(kdizi, k):
    dizi_w2v = [list(x) for x in model_w2v.wv.most_similar(positive=kdizi, topn=10)]      # Function return tuple of tuple .
    dizi_ft = [list(x) for x in model_fasttext.wv.most_similar(positive=kdizi, topn=10)]  # To chance it, convert to list of list.

    #-------- it turns tuple. Tuples 2. element is nearest value. We will get rid of them. Just take 1. element.-------
    d_ft=[]
    d_w2v=[]
    for i in range(len(dizi_ft)):
        d_ft.append(dizi_ft[i][0])                                     # dizi_ft[i] is tuple, so converted.
        d_w2v.append(dizi_w2v[i][0])
        dizi_ft[i][1] = format(dizi_ft[i][1], '.2f')                   # just take .00 (2 decimal after dot.)
        dizi_w2v[i][1]= format(dizi_w2v[i][1], '.2f')

    print(str(k) + ". Most similar to (Ftx) {0}".format(kdizi), dizi_ft)       # for just key of dict: d_ft
    print(str(k) + ". Most similar to (w2v) {0}".format(kdizi), dizi_w2v)      # for just key of dict: d_w2v

    # --------------------- Write to myoutFile.txt (Don't write two times same word)-----------------------------------
    count = 0
    outF.write(kdizi)
    for line in d_ft:
        outF.write(",")
        outF.write(str(line))
        count +=1
    for line in d_w2v:
        if line not in d_ft:                           # If it wrote before, don't write
            outF.write(",")
            outF.write(str(line))
            count +=1
        # else:                                     # İf you want to are there any similar word you can use else: ...
        #     print("  same : ", line)
    #outF.write(str(count))           # Can you delete it. This shows the number of word count
    outF.write("\n")

if __name__ == "__main__":

    # --------------- TAKING WORD WHICH ARE İNPUT FOR W2V AND FASTTEX FROM attributes.TXT ---------------
    # attributes.TXT has a list of attributes define the hotel. (it can be changed by users easily.)
    outF = open("Dataset/txt files/attributes.txt", "r")
    attributes = outF.readlines()               # Taking a str and put it in list[0] so we parse it from ',' (There are just one line)
    attributes = attributes[0].split(",")       # Convert attributes to list.
    print(attributes)

    attMatrix = [[] for _ in range(len(attributes))]  # Create len(attributes) different list in list ** important! wirte like this!
    # pprint(attMatrix)

    for i in range(len(attributes)):                  # Put attributes to matrix 0. column m[0][0], m[1][0], m[2][0] like this.
        attMatrix[i].append(attributes[i])
    # pprint(attMatrix)                                 # Printing good matrix

    # -------------------------------- Preproccessing -------------------------------------------
    reviews = []
    for i in reviews_df_com["Review Text"]:
        reviews.append(clean_text(i))     #top.append(text)  # That is very IMPORTANT !!! :)

    # ---------------------------------- Word2Vect -----------------------------------------------
    model_w2v = Word2Vec(reviews, size=150, window=10, min_count=2, workers=10, sg=0 )  #sg=0 cbow
    model_w2v.train(reviews, total_examples=len(reviews), epochs=12)

    # ---------------------------------- Fasttext -----------------------------------------------
    model_fasttext = FastText(size=170, window=10, min_count=2, workers=10, sg=0)  # instantiate
    model_fasttext.build_vocab(sentences=reviews)
    model_fasttext.train(sentences=reviews, total_examples=len(reviews), epochs=12)  # train

    word_vectors = model_fasttext.wv
    word_vectors_w2v = model_w2v.wv

    outF = open("Dataset/txt files/myOutFile1.txt", "w+")

    for i in range(len(attributes)):            # Each attributes send to word2vectfonc fonction to use w2v and fasttex.
        word2vectfonc(attMatrix[i][0], i)

    outF.close()