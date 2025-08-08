from transformers import pipeline

# Load model once globally
sentiment_pipeline = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def analyze_sentiment(texts):
    results = sentiment_pipeline(texts)
    sentiments = []
    for result in results:
        label = result['label'].lower()
        sentiments.append(label)
    return sentiments
