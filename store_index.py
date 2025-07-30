import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

extracted_data = load_pdf_files(data="data/")
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)   

embeddings = download_embeddings()

# Initialize Pinecone
pinecone_api_key = PINECONE_API_KEY

pc = Pinecone(api_key=pinecone_api_key)

index_name = "medical-assistant"

# Check if the index exists, if not create it
if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # Dimension of the embeddings
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

index = pc.Index(index_name)

# Store the documents in Pinecone
# Create a PineconeVectorStore instance

docset = PineconeVectorStore.from_documents(
    documents=text_chunks, # List of Document objects
    embedding=embeddings, # HuggingFaceBgeEmbeddings instance
    index_name=index_name # Name of the Pinecone index
)
