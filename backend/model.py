from langchain import PromptTemplate
# from langchain_community import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
# from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
import chainlit as cl

DB_FAISS_PATH = "vectorstores/db_faiss"

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, please just say that you don't know the answer, don't try to make up
an answer.

Context: {context}
Question: {question}

Only returns the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context','question'])
    return prompt
    

def load_llm():
    # """Loads the Llama-2 LLM model."""
    model_name = "llama-2-7b-chat.ggmlv3.q8_0.bin" #llama-2-7b-chat.ggmlv3.q8_0.bin
    model_type = "llama"
    max_new_tokens = 30
    temperature = 0.5
    llm = CTransformers(model=model_name, model_type=model_type, max_new_tokens=max_new_tokens, temperature=temperature)
    return llm

def retrieval_qa_chain(llm, prompt, db):
    # """Creates a retrieval-QA chain for question answering."""
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True,
        chain_type_kwargs = {'prompt': prompt})
    return qa_chain

def qa_bot():
    # """Sets up the question-answering bot."""
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs = {'device':'cuda'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

def result(query):
    qa_result = qa_bot()
    response = qa_result({'query':query})
    return response