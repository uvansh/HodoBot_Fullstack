from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from config.prompts import contextual_prompt, qa_prompt
from utils.vector_store import load_vectorstore
class RAGEngine:
    def __init__(self, vectorstore,llm):
        self.vectorestore = vectorstore
        self.llm = llm
        self.retrieval_chain = self._create_chain()
        
    def _create_chain(self):
        # Create retriever
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k":20, # Fetch more documents to allow MMR to select the best ones.
                "lambda_mult":0.7, # Balance between relevance and diversity.
                }
        ) # Retrieve top 3 similar chunks for context and use them to answer the question.
        
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            retriever, 
            contextual_prompt
        )
        
        qa_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        conversational_rag_chain = create_retrieval_chain(
            history_aware_retriever,
            qa_chain
        )
        return conversational_rag_chain
    
    def query(self, question, chat_history):
        return self.retrieval_chain.invoke({
            "input":question,
            "chat_history":chat_history
        })