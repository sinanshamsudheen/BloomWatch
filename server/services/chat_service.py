import os
import logging
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from config import settings

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize the RAG chat service with the PDF document"""
        try:
            # Check if OpenAI API key is available
            if not settings.OPENAI_API_KEY:
                logger.warning("OpenAI API key not found. RAG chat service will not be available.")
                return False
                
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
            
            # Load and process the PDF document
            pdf_path = os.path.join(os.path.dirname(__file__), "..", "bloom.pdf")
            if not os.path.exists(pdf_path):
                logger.error(f"PDF file not found at {pdf_path}")
                return False
                
            # Load PDF document
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            # Initialize QA chain
            llm = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever()
            )
            
            self.is_initialized = True
            logger.info("RAG chat service initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG chat service: {str(e)}")
            return False
    
    def get_response(self, query: str) -> str:
        """Get a response to a user query using RAG"""
        if not self.is_initialized:
            return "The chat service is not available. Please check the server configuration."
            
        try:
            # Use the QA chain to get a response
            response = self.qa_chain.invoke({"query": query})
            return response["result"]
        except Exception as e:
            logger.error(f"Error getting chat response: {str(e)}")
            return "Sorry, I encountered an error while processing your question."

# Global instance
chat_service = ChatService()