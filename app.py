from flask import Flask, jsonify, render_template, request, url_for, redirect, session
import pandas as pd
import plotly.graph_objects as go
import base64
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy import text
import http.client, urllib.parse
import json

import os  # Import the 'os' module to generate a secret key

app = Flask(__name__)

# Configure SQLAlchemy for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'  # SQLite database file path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'udyansachdev2@gmail.com'
app.config['MAIL_PASSWORD'] = 'hmoe jevw caji ewrc'
#app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
with app.app_context():
    db.session.execute(text('DROP TABLE IF EXISTS prediction'))
    db.session.commit()

# Recreate the Prediction table based on the updated model
with app.app_context():
    db.create_all()

# Define the Prediction model for SQLAlchemy
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    name = db.Column(db.String(100))
    recent_date = db.Column(db.String(20))
    last_close_price = db.Column(db.Float)  # Adding last_close_price column
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    country = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    ten_day_ma = db.Column(db.Float)
    
# Create tables in the database (run this once to create the tables)
with app.app_context():
    db.create_all()

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
        
                # Fetch news data for the selected ticker
        conn = http.client.HTTPSConnection('api.marketaux.com')
        params = urllib.parse.urlencode({
            'api_token': '2YOdCqufLnYAbWCgPU0cZajCbMn8wtkU7Jw4KOmb',
            'symbols': ticker,  # Fetch news data for selected ticker
            'limit': 10,
        })
        conn.request('GET', '/v1/news/all?{}'.format(params))
        res = conn.getresponse()
        news_data = res.read()

        json_format = json.loads(news_data.decode('utf-8'))
        
        final = []
        for i in range(0, 3):
            entities = json_format['data'][i]
            df = pd.DataFrame(entities.items())
            df.columns =['metric', 'values']
            final.append(df)

        # Merge DataFrames based on the 'symbol' column (assuming it's the common column)
        final_out = final[0]  # Start with the first DataFrame
        for df in final[1:]:
            final_out = final_out.merge(df, on='metric', how='left')

        selected_metrics = ['title', 'description', 'snippet', 'url']
        extracted_data = final_out[final_out['metric'].isin(selected_metrics)]
        del extracted_data[extracted_data.columns[0]]
        extracted_data.columns =['News Article 1', 'News Article 2', 'News Article 3']
        extracted_data_dict = {col: extracted_data[col].tolist() for col in extracted_data.columns}

        #extracted_string = ""

        #for column in extracted_data.columns:
         #   extracted_string += f"{column.capitalize()}: \n"
          #  extracted_string += '\n'.join([f"{value}" for value in extracted_data[column]])
           # extracted_string += "\n\n"

        # Save prediction data to the database
        new_prediction = Prediction(
            ticker=ticker,
            name=last_row['Name'] if 'Name' in last_row else None,
            recent_date=last_row['timestamp'] if 'timestamp' in last_row else None,
            last_close_price=last_row['close'] if 'close' in last_row else None,
            open_price=last_row['open'] if 'open' in last_row else None,
            high_price=last_row['high'] if 'high' in last_row else None,
            low_price=last_row['low'] if 'low' in last_row else None,
            country=last_row['Country'] if 'Country' in last_row else None,
            sector=last_row['Sector'] if 'Sector' in last_row else None,
            industry=last_row['Industry'] if 'Industry' in last_row else None,
            ten_day_ma=last_row['10_day_MA'] if '10_day_MA' in last_row else None
            # Add other attributes as needed
        )
        db.session.add(new_prediction)
        db.session.commit()

        return render_template('stock_prediction.html', prediction=prediction, ticker=ticker, plot_url=plot_url,news_data=extracted_data_dict)

    except Exception as e:
        print(e)  # Print the actual exception for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        email = request.form['email']
        
        # Retrieve the prediction data from the database (replace this with your logic)
        prediction = Prediction.query.order_by(Prediction.id.desc()).first()

        # Extract all attributes from the prediction instance dynamically
        prediction_details = ''
        for column in Prediction.__table__.columns:
            column_name = column.name
            column_value = getattr(prediction, column_name)
            prediction_details += f"{column_name.capitalize()}: {column_value}\n"

        # Your email sending logic using the retrieved prediction data
        msg = Message('Stock Prediction', sender='your_email@gmail.com', recipients=[email])
        msg.body = 'Your stock prediction details...\n\n' + prediction_details
        mail.send(msg)  # Send the email

        # After sending the email, redirect to the success page
        return redirect(url_for('email_sent'))  # Assumes 'email_sent' is the endpoint for the success page
    
    except Exception as e:
        print(e)  # Print the actual exception for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/email_sent')
def email_sent():
    # Render the success page template after the email is sent
    return render_template('email_sent.html')

if __name__ == '__main__':
    app.run(debug=True)