# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:48:07 2023

@author: vkedu
"""
from flask import Flask, render_template, request
import numpy as np
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint
import random
from datetime import datetime
from keras.models import load_model

app = Flask('_name_',template_folder='templates')
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/result', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        # Retrieve form data
        hours = request.form['hours']
        minutes = request.form['minutes']
        seconds = request.form['seconds']
        
        # Print form data
        print(f"Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")
        
        # Load data
        data = pd.read_csv('MO.csv')

        # Drop unwanted columns
        data.drop(['Sender Address', 'Receiver Address', 'Protocol', 'Frame Size', 'Time Stamp', 'IP Version', 'Date'], axis=1, inplace=True)

        # Drop rows with empty or inf values in Bandwidth column
        data = data.replace([np.inf, -np.inf], np.nan).dropna(subset=['Bandwidth'])

        # Combine Time and Milliseconds columns
        data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S')
        data['Time'] += pd.to_timedelta(data['Milliseconds'], unit='ms')
        data.drop('Milliseconds', axis=1, inplace=True)

        # Convert time to numerical representation
        data['Time'] = data['Time'].apply(lambda x: x.timestamp())

        # Define features and target
        X = data[['Time', 'Time Diff']].values
        y = data['Bandwidth'].values

        # Normalize features
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Load LSTM model
        m = load_model('model.h5')
        
        # Generate random time
        time_str = f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}"
        random_time = datetime.strptime(time_str, '%H:%M:%S')
        
        # Example time difference
        random_time_diff = random.uniform(0, 1)
        
        # Create timestamp manually
        random_timestamp = (random_time - datetime(1970, 1, 1)).total_seconds()
        
        # Prepare input for prediction
        random_input = np.array([[random_timestamp, random_time_diff]])
        
        # Scale input
        random_input_scaled = scaler.transform(random_input)
        
        # Reshape input for LSTM
        random_input_reshaped = random_input_scaled.reshape((random_input_scaled.shape[0], 1, random_input_scaled.shape[1]))
        
        # Predict bandwidth for random time
        predicted_bandwidth = m.predict(random_input_reshaped)
        
        # Print predicted bandwidth
        print("Predicted Bandwidth:", predicted_bandwidth[0][0])
        
        # Return response
        return render_template("preview.html",v=predicted_bandwidth[0][0])

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port,debug=True)
