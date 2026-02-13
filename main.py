from flask import Flask, request, jsonify
import tabula
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = "temp.pdf"
    file.save(file_path)
    
    try:
        # PDF se table extract karna
        df = tabula.read_pdf(file_path, pages='all', multiple_tables=True, output_format="json")
        os.remove(file_path) # File delete karein processing ke baad
        return jsonify(df)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)