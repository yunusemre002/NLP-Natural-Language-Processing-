from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{} = {}".format(sentence, str(score)))


sentiment_analyzer_scores("The phone is super cool.")
sentiment_analyzer_scores("She's not terrific but not terrible either")
sentiment_analyzer_scores("This CD isn't horrid.")
sentiment_analyzer_scores("it is just not acceptable")
sentiment_analyzer_scores("not good")
