from flask import Flask, render_template, request, redirect, url_for, flash , send_from_directory
import pandas as pd
import os
from model.model import predict_spending

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flash messages

data = []  # This will hold the financial data

# Define the upload folder for the CSV file
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        income = float(request.form['income'])
        expense = float(request.form['expense'])
        category = request.form['category']

        # Append new data to the list
        data.append({'income': income, 'expense': expense, 'category': category})

        flash('Data submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    except ValueError:
        flash('Invalid input. Please enter numeric values for income and expense.', 'error')
        return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('upload.html')

def provide_recommendations(data):
    df = pd.DataFrame(data)
    average_expense = df['expense'].mean()
    
    if df['expense'].iloc[-1] > average_expense:
        return "Consider reducing discretionary spending."
    elif df['expense'].iloc[-1] < average_expense:
        return "Great job! Keep up the good spending habits."
    return "Maintain your current financial habits."

@app.route('/dashboard')
def dashboard():
    if not data:
        return render_template('dashboard.html', prediction=None, recommendations=None)

    prediction = predict_spending(data)
    recommendations = provide_recommendations(data)
    return render_template('dashboard.html', prediction=prediction, recommendations=recommendations, data=data)

@app.route('/download')
def download_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)