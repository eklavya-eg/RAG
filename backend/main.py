from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from ingest import create_vector_db
from model import result
import os
import shutil

app = Flask(__name__)
CORS(app)

def delete_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path):
            os.remove(item_path)
        
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        question = request.form.get('question')
        file = request.files.get('file')

        if not file or not question:
            return jsonify({'error': 'File and question are required'}), 400
        
        file.save('data/' + file.filename)
        db = create_vector_db("data/")
        ans = result(query=question)

        ans['source_documents'] = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in ans['source_documents']]
        delete_contents("RAG\\backend\\data")
        delete_contents("RAG\\backend\\vectorstores\\db_faiss")
        print(ans)
        return jsonify({'result': ans})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)