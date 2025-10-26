from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter


def load_document_from_directory(directory_path):
    # Load documents from the 'documents' directory
        text_loader = DirectoryLoader(
        path=directory_path,
            glob="**/*.txt",
            loader_cls = TextLoader,
            loader_kwargs = {"encoding":"utf-8"}
        )
        
        pdf_loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        
        text_docs = text_loader.load()
        pdf_docs = pdf_loader.load()
        documents = text_docs + pdf_docs
        print(f"Loaded {len(documents)} documents.")
        
        return documents

def split_documents(documents):
    # Create Chunks of text and embeddings.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n","\n",". ",", "," ",""]
        )
        
        # Chunk the loaded documents.
        chunks = text_splitter.split_documents(documents)
        
        print(f"Split into {len(chunks)} chunks.")
        print(f"First chunk preview: {chunks[0].page_content[:150]}")
        
        return chunks