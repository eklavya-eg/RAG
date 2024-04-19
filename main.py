
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from UniversalSentenceEncoder import TensorflowHubEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
from langchain_community.vectorstores import Typesense
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
import chainlit as cl

LLAMA2_PATH = "W:/Models/TheBloke/llama-2-7b-chat.ggmlv3.q8_0.bin"
DATA_PATH = "Docs/"
# USE_PATH = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
USE_PATH = "W:/Models/Sentence Embeddings/universal sentence encoder"

embedding = TensorflowHubEmbeddings(model_url=USE_PATH)
embedding.model_url = USE_PATH
embedding.load()
loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
pages = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap=30)
docs = splitter.split_documents(pages)

# TYPESENSE self-hosting api-key="xyz"
# %docker run -p 8108:8108 -v %cd%/typesense-data:/data typesense/typesense:26.0 --data-dir /data --api-key="xyz" --enable-cors
docsearch = Typesense.from_documents(
    docs,
    embedding,
    typesense_client_params={
        "host": "localhost",
        "port": "8108",
        "protocol": "http",
        "typesense_api_key": "xyz",
        "typesense_collection_name": "lang-chain",
    },
)

# Setting Up CHAIN
custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, please just say that you don't know the answer, don't try to make up
an answer.

Context: {context}
Question: {question}

Only returns the helpful answer below and nothing else.
Helpful answer:
"""

prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context','question'])

model = CTransformers(model=LLAMA2_PATH, model_type="llama", max_new_tokens=100, temperature=0.3)

chain = RetrievalQA.from_chain_type(llm=model,
                                    chain_type='stuff',
                                    retriever=docsearch.as_retriever(search_kwargs={'k': 3}),
                                    return_source_documents=True,
                                    chain_type_kwargs={'prompt': prompt})
def response(query):
    result = chain
    result = result({'query': query})
    return result

@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting...")
    await msg.send()
    msg.content = "Hi, What is your query?"
    await msg.update()
    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        print(answer, "\n", str(sources))
    else:
        answer += "\nNo sources found"

    # if sources:
    #     answer += f"\nSources:" + str(sources)
    # else:
    #     answer += "\nNo sources found"

    await cl.Message(content=answer).send()