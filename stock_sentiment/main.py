import os
import uuid
import yfinance as yf
import requests
from transformers import pipeline
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Hugging Face pipelines
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Create static folder if not exists
os.makedirs('static', exist_ok=True)

def fetch_news(stock):
    """
    Fetch latest news headlines for a stock using Google News RSS
    """
    query = stock + " stock news"
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    response = requests.get(url)
    news_items = []

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.iter('item'):
            title = item.find('title').text
            news_items.append(title)
    else:
        print(f"Failed to fetch news for {stock}. Status code: {response.status_code}")
    
    return news_items

def generate_price_chart(stock_data, stock):
    """
    Generate and save stock price chart
    """
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label=f'{stock} Close Price')
    plt.title(f'{stock} Stock Price - Last 7 Days')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.grid(True)
    filename = f"static/{uuid.uuid4().hex}_price.png"
    plt.savefig(filename)
    plt.close()
    return filename

def generate_sentiment_chart(sentiments):
    """
    Generate and save sentiment distribution chart
    """
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for s in sentiments:
        if s in sentiment_counts:
            sentiment_counts[s] += 1
        else:
            sentiment_counts["NEUTRAL"] += 1

    plt.figure(figsize=(6, 4))
    sns.barplot(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), palette="viridis")
    plt.title("Sentiment Distribution")
    plt.ylabel("Count")
    filename = f"static/{uuid.uuid4().hex}_sentiment.png"
    plt.savefig(filename)
    plt.close()
    return filename

def run_analysis(stock):
    """
    Perform price fetching, news summarization, sentiment analysis, and decision making
    """
    # Fetch stock price
    stock_data = yf.download(stock + ".BO", period="7d", interval="1h", auto_adjust=False)
    
    if stock_data.empty:
        print(f"No stock data found for {stock}")
        return {}

    latest_price = float(stock_data['Close'].iloc[-1])

    # Fetch News
    news_items = fetch_news(stock)
    if not news_items:
        print(f"No news found for {stock}")
        return {}

    # Summarize News
    try:
        summaries = []
        for item in news_items[:5]:  # top 5 headlines
            short_summary = summarizer(item, max_length=min(50, len(item.split()) // 2), min_length=20, do_sample=False)[0]['summary_text']
            summaries.append(short_summary)
    except Exception as e:
        print(f"Summarization failed: {e}")
        summaries = ["Summary not available."]

    # Sentiment Analysis
    try:
        sentiments = []
        for item in summaries:
            result = sentiment_pipeline(item)[0]
            sentiments.append(result['label'])
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        sentiments = ["NEUTRAL"]

    # Overall Decision
    if sentiments.count("POSITIVE") > sentiments.count("NEGATIVE"):
        decision = "Bullish 📈"
        sentiment_img_path = "static/bullish.png"
    elif sentiments.count("NEGATIVE") > sentiments.count("POSITIVE"):
        decision = "Bearish 📉"
        sentiment_img_path = "static/bearish.png"
    else:
        decision = "Neutral 🤝"
        sentiment_img_path = "static/neutral.png"

    # Charts
    price_chart_path = generate_price_chart(stock_data, stock)
    sentiment_chart_path = generate_sentiment_chart(sentiments)

    return {
        "latest_price": latest_price,
        "decision": decision,
        "sentiment_img": sentiment_img_path,
        "summaries": summaries,
        "price_chart": price_chart_path,
        "sentiment_chart": sentiment_chart_path
    }
