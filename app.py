from flask import Flask, send_from_directory,jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate   
from dotenv import load_dotenv
from src.prompt import *
import os

load_dotenv()

app = Flask(__name__, static_folder='static')

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_embeddings()

index_name = "medical-assistant"
#embed each chunk and upsert the embeddings into the Pinecone index

docseach = PineconeVectorStore.from_existing_index(
    index_name=index_name,  # Name of the Pinecone index
    embedding=embeddings,  # HuggingFaceBgeEmbeddings instance
)

retriever = docseach.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 3  # Number of similar documents to retrieve
    }
)  

chatModel = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answering_chain = create_stuff_documents_chain(
   chatModel,
    prompt)

rag_chain = create_retrieval_chain(
    retriever,
    question_answering_chain
    )

@app.route('/api', methods=['POST'])
def chat():
    data= request.get_json()
    msg = data["msg"]

    response = rag_chain.invoke({"input":msg})
    answer = response['answer']
    print("Response:", answer)
    return answer

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # if the requested resource exists, serve it
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # otherwise, serve React's index.html
    return send_from_directory(app.static_folder, 'index.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)