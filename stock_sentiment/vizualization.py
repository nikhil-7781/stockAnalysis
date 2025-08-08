import matplotlib.pyplot as plt
import io
import base64

def plot_sentiment_counts(bullish, bearish, neutral):
    plt.figure(figsize=(6,4))
    plt.bar(['Bullish', 'Bearish', 'Neutral'], [bullish, bearish, neutral], color=['green', 'red', 'gray'])
    plt.title('Sentiment Analysis Results')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    
    return image_base64

def plot_stock_price(stock_data):
    plt.figure(figsize=(8,4))
    plt.plot(stock_data['Close'], marker='o')
    plt.title('Stock Price Over Last Week')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    
    return image_base64
