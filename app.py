from flask import Flask, jsonify, render_template, request
import pandas as pd
import plotly.graph_objects as go
import base64

app = Flask(__name__)

def generate_time_series_plot(data):
    fig = go.Figure(data=[go.Candlestick(x=data['timestamp'],
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])

    fig.update_layout(title='Stock Candlestick Chart', xaxis_title='Date', yaxis_title='Price', showlegend=False)

    # Convert the plot to a div string using Plotly's to_html method
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # Encode the plot div string to base64
    encoded_plot = base64.b64encode(plot_div.encode()).decode('utf-8')
    
    return encoded_plot

@app.route('/')
def index():
    return render_template('stock_prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        ticker = request.form['ticker']
        # Retrieve historical data
        stock_data = pd.read_csv('Final_Merge.csv')
        stock_data = stock_data[stock_data['Symbol'] == ticker]

        # Calculate the 10-day rolling average
        stock_data['10_day_MA'] = stock_data['close'].rolling(window=10).mean()
        
        # Get the last row of the data (latest date)
        last_row = stock_data.iloc[0]

        prediction = {
            'Name': last_row['Name'],
            'Symbol': ticker,
            'RecentDate': last_row['timestamp'],
            'Last Close Price': last_row['close'],
            'Open': last_row['open'],
            'High': last_row['high'],
            'Low': last_row['low'],
            'Country': last_row['Country'],
            'Sector': last_row['Sector'],
            'Industry': last_row['Industry'],
            '10_day_MA': last_row['10_day_MA']  # Adding 10-day MA to prediction
        }

        # Generate time series plot
        plot_url = generate_time_series_plot(stock_data)

        return render_template('stock_prediction.html', prediction=prediction, ticker=ticker, plot_url=plot_url)
    
    except Exception as e:
        print(e)  # Print the actual exception for debugging
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)