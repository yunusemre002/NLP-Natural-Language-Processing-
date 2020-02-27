from nltk.corpus import wordnet
# Stopword'ü kaldır ?
# Stopword'ü revize et ?
# Stopword'LÜ Dene ?
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
    text = text.lower()    # lower text
    print("LOVER: ", text)
    text = [word.strip(string.punctuation) for word in text.split(" ")]     # tokenize text and remove puncutation
    print("TOKENIZE: ", text)
    text = [word for word in text if not any(c.isdigit() for c in word)]    # remove words that contain numbers
    print("ALFAPHE: ", text)
    """stop = stopwords.words('english')
    text = [x for x in text if x not in stop]     # remove stop words
    text = [t for t in text if len(t) > 0]        # remove empty tokens
    print("STOP: ", text)"""
    pos_tags = pos_tag(text)
    print("POS_TAG: ", pos_tags)# pos tag text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]    # lemmatize text  -ing, -ed, s,ss,
    print("LEMMA: ", text)
    text = [t for t in text if len(t) > 1]     # remove words with only one letter
    text = " ".join(text)    # join all
    return (text)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
# function to print sentiments of the sentence.
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()    # Create a SentimentIntensityAnalyzer object.

    # Polarity_scores method of SentimentIntensityAnalyzer
    # Oject gives a sentiment dictionary.
    # Which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

    print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")
    elif sentiment_dict['compound'] <= - 0.05:
        print("Negative")
    else:
        print("Neutral")
    # Driver code

if __name__ == "__main__":
    #sentence = "Geeks For Geeks is the best portal for the computer science engineering students."
    sentence = "I think that Semih is not a lazy person"
    sentence = clean_text(sentence)
    print("\n1st statement :  ", sentence)
    # function calling
    sentiment_scores(sentence)

    #sentence = "study is going on as usual"
    sentence = "This is a book"
    print("\n2nd Statement :    ", sentence)
    sentence = clean_text(sentence)
    sentiment_scores(sentence)

    sentence = "I will't win the games because I'm not a good player"
    print("\n3rd Statement :    ", sentence)
    sentence = clean_text(sentence)
    sentiment_scores(sentence)