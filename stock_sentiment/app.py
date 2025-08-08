from flask import Flask, render_template, request
from main import run_analysis

app = Flask(__name__)

# List of BSE Stock Tickers
STOCKS = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'HINDUNILVR']

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_stock = None
    results = {}

    if request.method == 'POST':
        selected_stock = request.form.get('stock')
        results = run_analysis(selected_stock)

    return render_template('index.html',
                           stocks=STOCKS,
                           selected_stock=selected_stock,
                           latest_price=results.get('latest_price'),
                           decision=results.get('decision'),
                           sentiment_img=results.get('sentiment_img'),
                           summaries=results.get('summaries', []),
                           price_chart=results.get('price_chart'),
                           sentiment_chart=results.get('sentiment_chart')
                           )

if __name__ == '__main__':
    app.run(debug=True)
