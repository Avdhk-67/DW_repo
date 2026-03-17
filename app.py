from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    file_bytes = request.data
    df = pd.read_parquet(io.BytesIO(file_bytes))
    df = df.where(pd.notnull(df), None)
    df = df.fillna("")
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run()