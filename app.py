import csv
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use your actual database URI
db = SQLAlchemy(app)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
        return 'No file part', 400

    file1_id = request.files['file1']
    file2_id = request.files['file2']
    file3_id = request.files['file3']

    if file1_id == '' or file2_id == '' or file3_id == '':
        return 'No selected file', 400

    # Download files from Google Drive
    file1_url = f"https://drive.google.com/uc?id={file1_id}"
    file2_url = f"https://drive.google.com/uc?id={file2_id}"
    file3_url = f"https://drive.google.com/uc?id={file3_id}"

    file1 = requests.get(file1_url)
    file2 = requests.get(file2_url)
    file3 = requests.get(file3_url)

    # Process the downloaded files
    dfs = []
    for file in [file1, file2, file3]:
        data = pd.read_csv(file.content)
        dfs.append(data)

    for i, df in enumerate(dfs):
        df.to_sql('table' + str(i+1), con=db.engine, if_exists='replace')

    return 'Files uploaded and data inserted into DB', 200