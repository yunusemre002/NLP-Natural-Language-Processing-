from nltk.sentiment.vader import SentimentIntensityAnalyzer
# function to print sentiments of the sentence.
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()                 # Create a SentimentIntensityAnalyzer object.

    # Polarity_scores method of SentimentIntensityAnalyzer # Oject gives a sentiment dictionary.
    # Which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print(sentiment_dict['neg'] * 100, "% Negative")
    print(sentiment_dict['neu'] * 100, "% Neutral")
    print(sentiment_dict['pos'] * 100, "% Positive")

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

    sentence = "I think that Semih is a lazy person"
    print("\n1.", sentence)
    sentiment_scores(sentence)

    sentence = "This is a book"
    print("\n2.", sentence)
    sentiment_scores(sentence)

    sentence = "I love him but he have some bad side"
    print("\n3.", sentence)
    sentiment_scores(sentence)