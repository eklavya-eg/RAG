I am using RAG to create the project which is Retrieval Augmented Generation.

First of all taking data file and query from user from frontend to backend then
using ingest.py to create vectorstores of data and the saving it.

Then using llama2-7b quantized model by TheBloke to provide context retrieved from vvector stores and query by user,
to the model, which will answer to the query.

Then this answer will be sent to frontend by backend.

backend running on port 5000
frontend running on port 3000