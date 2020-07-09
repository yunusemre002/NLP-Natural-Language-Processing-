import pandas as pd
from nltk import pos_tag, re, word_tokenize, pprint
from gensim.models import FastText, Word2Vec
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
stop_words = set(stopwords.words('english'))

#-------------------------------------------------Import Data from CSV-------------------------------------------------------
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London1.csv", encoding = "ISO-8859-1")  # Read data !!!!
reviews_df_com = reviews_df[['Review Text']]                                        # Remove except for  "Review Text"
reviews_df_com = reviews_df_com.dropna().copy()                                     # Remove empty reviews ,if there is.
reviews_df_com = reviews_df_com.sample(frac=0.01, replace=False, random_state=42)  # Take %01 of reviews.
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
    # text = [WordNetLemmatizer().lemmatize(t) for t in text]                                # Other option of lemmatizer
    text = [t for t in text if len(t) > 1]     # remove words with only one letter or empty
    return (text)

# ------------------------------- Find and Print---------------------------------
def word2vectfonc(kdizi, k):
    dizi = [list(x) for x in model.wv.most_similar(positive=kdizi, topn=10)]  # function return tuple of tuple . To chance it, convert to list of list.
    dizi_w2v = [list(x) for x in model_w2v.wv.most_similar(positive=kdizi, topn=10)]

    d=[]
    d_w2v=[]
    for i in range(len(dizi)):
        d.append(dizi[i][0])                                       # dizi[i] is tuple, so converted.
        d_w2v.append(dizi_w2v[i][0])
        dizi[i][1]= format(dizi[i][1], '.4f')                      # just take .0000 (4 decimal after dot.)
        dizi_w2v[i][1]= format(dizi_w2v[i][1], '.4f')

    print(str(k) + ". Most similar to {0}".format(kdizi), dizi)
    print(str(k) + ". Most similar to (w2v) {0}".format(kdizi), dizi_w2v)

    count = 0
    outF.write(kdizi)
    for line in d:
        outF.write(",")
        outF.write(str(line))
        count +=1
    for line in d_w2v:
        if line not in d:                           # If it wrote before, don't write
            outF.write(",")
            outF.write(str(line))
            count +=1
        # else:                                     # İf you want to are there any similar word you can use else: ...
        #     print("  same : ", line)
    #outF.write(str(count))           # Can you delete it. This shows the number of word count
    outF.write("\n")

if __name__ == "__main__":

    # --------------- TAKING WORD WHICH ARE İNPUT FOR W2V AND FASTTEX FROM attributes.TXT ---------------
    # attributes.TXT has a list of attributes which define to hotel. (it can be cahnge by users easily.)
    outF = open("attributes.txt", "r")
    attributes = outF.readlines()               # Taking a str and put it in list[0] so we parse it from ,
    attributes = attributes[0].split(",")       # Convert attributes to list.
    print(attributes)

    attMatrix = [[] for _ in range(len(attributes))]  # Create len(attributes) different list in list ** important! wirte like this!
    #pprint(attMatrix)

    for i in range(len(attributes)):                  # Put attributes to matrix 0. column m[0][0], m[1][0], m[2][0] like this.
        attMatrix[i].append(attributes[i])
    # pprint(attMatrix)                               # Printing good matrix

    #-------------------------- Preproccessing ----------------------------------
    reviews = []
    for i in reviews_df_com["Review Text"]:
        reviews.append(clean_text(i))     #top.append(text)  # That is very IMPORTANT !!! :)

    # --------------------------- Word2Vect ----------------------------------
    model_w2v = Word2Vec(reviews, size=150, window=10, min_count=2, workers=10)
    model_w2v.train(reviews, total_examples=len(reviews), epochs=10)

    # ---------------------------- Fasttext ----------------------------------
    model = FastText(size=170, window=10, min_count=2, workers=10)  # instantiate
    model.build_vocab(sentences=reviews)
    model.train(sentences=reviews, total_examples=len(reviews), epochs=10)  # train

    word_vectors = model.wv
    word_vectors_w2v = model_w2v.wv

    outF = open("myOutFile1.txt", "w+")

    for i in range(len(attributes)):            # Each attributes send to word2vectfonc fonction to use w2v and fasttex.
        word2vectfonc(attMatrix[i][0], i)

    outF.close()