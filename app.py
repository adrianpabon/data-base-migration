import csv
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use your actual database URI
db = SQLAlchemy(app)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
        return 'No file part', 400
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']

    if file1.filename == '' or file2.filename == '' or file3.filename == '':
        return 'No selected file', 400

    dfs = []
    for file in [file1, file2, file3]:
        data = pd.read_csv(file)
        dfs.append(data)

    for i, df in enumerate(dfs):
        df.to_sql('table' + str(i+1), con=db.engine, if_exists='replace')

    return 'Files uploaded and data inserted into DB', 200