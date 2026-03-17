from flask import Flask, request, jsonify
import pandas as pd
import io
import base64

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Get raw bytes from request
        file_bytes = request.get_data()
        
        # If data comes as base64 encoded string
        if file_bytes[:3] != b'PAR':
            try:
                file_bytes = base64.b64decode(file_bytes)
            except Exception:
                pass
        
        buf = io.BytesIO(file_bytes)
        buf.seek(0)
        df = pd.read_parquet(buf)
        df = df.where(pd.notnull(df), None)
        df = df.fillna("")
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
