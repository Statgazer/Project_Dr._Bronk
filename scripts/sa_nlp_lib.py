import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Initialize the VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Reading content from the JSON file
with open('/Users/roshen_abraham/Desktop/PC/RA/DR. CHRIS BRONK/project/target files/tass_com.json', 'r') as file:
    data = json.load(file)

# Going through each article in the data
for article in data:
    title = article['title']
    content = article['content']

    # Converting content to lowercase
    content = content.lower()

    # Perform sentiment analysis using VADER
    vader_sentiment_scores = vader_analyzer.polarity_scores(content)

    # Perform sentiment analysis using TextBlob
    textblob_analysis = TextBlob(content)
    textblob_sentiment = textblob_analysis.sentiment

    # Print title and sentiment scores for both approaches
    print(f"Title: {title}")
    print(f"VADER Sentiment - Positive: {vader_sentiment_scores['pos']:.2f}, Negative: {vader_sentiment_scores['neg']:.2f}, Compound: {vader_sentiment_scores['compound']:.2f}")
    print(f"TextBlob Sentiment - Polarity: {textblob_sentiment.polarity:.2f}, Subjectivity: {textblob_sentiment.subjectivity:.2f}\n")