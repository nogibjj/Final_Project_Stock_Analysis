from flask import Flask, jsonify, render_template, request

import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stock_prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        ticker = request.form['ticker']
        # retreive historical data
        stock_data = pd.read_csv('Final_Merge.csv')
        stock_data = stock_data[stock_data['Symbol'] == ticker]

        # Calculate the 10-day moving average
        stock_data['10_day_MA'] = stock_data['close'].rolling(window=10).mean()

        # Get the last row of the data (latest date)
        last_row = stock_data.iloc[0]

        prediction = {
            'Name': last_row['Name'],
            'Symbol': ticker,
            'RecentDate': last_row['timestamp'],
            'Last Close Price': last_row['close'],
            '10 Day moving Average': last_row['10_day_MA'],
            'Open': last_row['open'],
            'High': last_row['high'],
            'Low': last_row['low'],
            'Country': last_row['Country'],
            'Sector': last_row['Sector'],
            'Industry': last_row['Industry']
        }

        return render_template('stock_prediction.html', prediction=prediction, ticker=ticker)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)