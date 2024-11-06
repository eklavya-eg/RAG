from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ingest import create_vector_db
from model import result
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def delete_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path):
            os.remove(item_path)
        
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

@app.post("/predict")
async def predict(question: str = Form(...), file: UploadFile = File(...)):
    try:
        if not file or not question:
            raise HTTPException(status_code=400, detail="File and question are required")

        file_path = os.path.join('data', file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        db = create_vector_db("data/")
        ans = result(query=question)

        ans['source_documents'] = [
            {'page_content': doc.page_content, 'metadata': doc.metadata} for doc in ans['source_documents']
        ]
        
        delete_contents("RAG\\backend\\data")
        delete_contents("RAG\\backend\\vectorstores\\db_faiss")
        
        return JSONResponse(content={'result': ans})
        
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
