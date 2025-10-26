from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Loading Document and Creating Vectorstore
def create_vectorstore(chunks,persist_directory="./chroma_db"):
    
    # Create Embeddings and Vectorstore
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print("Vector store created.")
    return vectorstore

def load_vectorstore(persist_directory="./chroma_db"):
    # Load existing vectorstore
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    print("Vector store loaded.")
    return vectorstore