
from flask import Flask, render_template,send_from_directory, request, redirect, url_for, session, flash, jsonify
import numpy as np
import cv2
import base64
import os
from werkzeug.utils import secure_filename
import pandas as pd

from utils.chart_generator import generate_charts
from utils.insights import generate_insights

app = Flask(__name__)
app.secret_key = 'manjal'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard.html', methods=['GET', 'POST'])
def serve_page2():

    dataset_name = None
    features = []
    charts = []
    insights = []
    
    if request.method == 'POST':
        if 'dataset' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['dataset']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read dataset
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                dataset_name = filename
                features = list(df.columns)
                
                charts = generate_charts(df)
                insights = generate_insights(df)
                
            except Exception as e:
                flash(f'Error reading dataset: {str(e)}', 'error')
        else:
            flash('Allowed file types: csv, xlsx', 'error')
    
    return render_template('dashboard.html',  
                           dataset_name=dataset_name,
                           features=features,
                           charts=charts,
                           insights=insights,)



if __name__ == "__main__":
    app.run(debug=True)
