from flask import Flask, request, jsonify
import pandas as pd
import io
import base64

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Try reading as raw binary first
        file_bytes = request.data
        if not file_bytes:
            # Try reading from JSON body as base64
            data = request.get_json()
            file_bytes = base64.b64decode(data['fileBase64'])
        
        df = pd.read_parquet(io.BytesIO(file_bytes))
        df = df.where(pd.notnull(df), None)
        df = df.fillna("")
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
