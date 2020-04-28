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
    sentence = "I think that Semih is a lazy person"
    print("\n1st statement :  ", sentence)

    # function calling
    sentiment_scores(sentence)

    #sentence = "study is going on as usual"
    sentence = "This is a book"
    print("\n2nd Statement :    ", sentence)
    sentiment_scores(sentence)

    sentence = "I will win the games because I'm a good player"
    print("\n3rd Statement :    ", sentence)
    sentiment_scores(sentence)