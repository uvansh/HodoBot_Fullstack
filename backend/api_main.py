from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from langchain_groq import ChatGroq
from config.tools_schema import tools
from dotenv import load_dotenv
from core.rag_engine import RAGEngine
from core.tool_handler import ToolHandler
from core.router import route_query
from utils.vector_store import create_vectorstore, load_vectorstore
from langchain_classic.schema import HumanMessage, AIMessage
import os
from utils.document_loader import split_documents, load_document_from_directory
from contextlib import asynccontextmanager
from config.tools_schema import available_functions

load_dotenv()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    chat_history: List[Message] = []

class Source(BaseModel):
    file: str
    content: str
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    confidence: Optional[float] = None

def initialize_llm():
    llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=os.environ.get("GROQ_API_KEY"),
        )
    return llm

rag_engine = None
tool_handler = None
vectorstore = None
llm = None

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Initialize HodoBot components on server startup
    global rag_engine, tool_handler, vectorstore,llm
    
    print("Initializing HodoBot...")
    
    doc = load_document_from_directory(directory_path="./documents")
    vectorstore = create_vectorstore(chunks=split_documents(doc))
    print("Vectorstore ready.")
    
    # Load documents
    load_vectorstore()
    
    # Initialize LLM
    llm = initialize_llm()
    print("LLM initialized.")
    
    # Initialize RAG Engine
    rag_engine = RAGEngine(vectorstore, llm)
    print("RAG Engine initialized.")
    
    # Initialize Tool Handler
    tool_handler = ToolHandler(llm, tools,available_functions=available_functions)
    print("Tool Handler initialized.")
    
    print("HodoBot ready!")
    
    yield
    
    print("Shutting down HodoBot...")
    
app = FastAPI(title="HodoBot API",description="AI Travel Assistant.",lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "HodoBot API",
    }

@app.get("/health")
async def health():
    return {
        "status":"ok",
        "rag_engine": rag_engine is not None,
        "tool_handler": tool_handler is not None,
        "vectorstore": vectorstore is not None
    }

@app.post("/chat",response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chat_history = []
        for msg in request.chat_history:
            if msg.role == "user":
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                chat_history.append(AIMessage(content=msg.content))
        
        result = route_query(
            question=request.message,
            chat_history=chat_history,
            rag_engine=rag_engine,
            tool_handler=tool_handler
            )
        
        sources = []
        if 'context' in result:
            for doc in result['context']:
                sources.append(Source(
                    file=doc.metadata.get('source','unknown'),
                    content=doc.page_content[:150]
                ))

        return ChatResponse(
            answer=result['answer'],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/documents")
async def list_documents():
    return {
        "documents": [],
        "total": 0
    }
    
if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)