from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document], min_length: int = 1000) -> List[Document]:
    
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get('source')
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    'source': src
                }
            )
        )
    return minimal_docs

# Split the documents into smaller chunks

def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    texts_chunks = text_splitter.split_documents(minimal_docs)
    return texts_chunks


def download_embeddings():
    model_name = "sentence-transformers/all-MiniLm-L6-v2"  
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name
    )
    return embeddings

embedding = download_embeddings()

