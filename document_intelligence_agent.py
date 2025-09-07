#!/usr/bin/env python3
"""
Document Intelligence Agent
==========================

A sophisticated RAG (Retrieval-Augmented Generation) system for enterprise document analysis.
This agent can process PDF documents, create semantic embeddings, and answer questions
based on document content using advanced AI models.

Features:
- PDF document processing and chunking
- Free HuggingFace embeddings for cost efficiency
- OpenAI GPT integration for intelligent responses
- Persistent vector storage with ChromaDB
- Interactive chat interface
- Batch processing for large document sets

Author: [Your Name]
Date: 2024
"""

import os
import sys
import time
from typing import List, Dict, Any
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import Document

class DocumentIntelligenceAgent:
    """
    A sophisticated RAG-based document intelligence agent.
    
    This class provides functionality to:
    - Load and process PDF documents
    - Create semantic embeddings using HuggingFace models
    - Store and retrieve document chunks efficiently
    - Answer questions based on document content
    """
    
    def __init__(self, 
                 data_directory: str = "./data",
                 vector_store_path: str = "./chroma_db",
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize the Document Intelligence Agent.
        
        Args:
            data_directory: Path to directory containing PDF files
            vector_store_path: Path to store the vector database
            embedding_model: HuggingFace model name for embeddings
            chunk_size: Size of document chunks for processing
            chunk_overlap: Overlap between consecutive chunks
        """
        self.data_directory = Path(data_directory)
        self.vector_store_path = vector_store_path
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize components
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.llm = None
        self.rag_chain = None
        
        # Statistics
        self.stats = {
            'documents_loaded': 0,
            'chunks_created': 0,
            'processing_time': 0
        }
    
    def setup_embeddings(self) -> None:
        """Initialize the embedding model."""
        print("🔄 Initializing embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Embedding model ready")
    
    def load_documents(self) -> List[Document]:
        """
        Load all PDF documents from the data directory.
        
        Returns:
            List of loaded documents
        """
        print(f"📄 Loading documents from {self.data_directory}...")
        documents = []
        
        if not self.data_directory.exists():
            raise FileNotFoundError(f"Data directory {self.data_directory} not found")
        
        pdf_files = list(self.data_directory.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.data_directory}")
        
        for pdf_file in pdf_files:
            print(f"  📖 Loading {pdf_file.name}...")
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            documents.extend(docs)
        
        self.stats['documents_loaded'] = len(documents)
        print(f"✅ Loaded {len(documents)} documents from {len(pdf_files)} files")
        return documents
    
    def create_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better processing.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of document chunks
        """
        print("✂️ Creating document chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        self.stats['chunks_created'] = len(chunks)
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, chunks: List[Document]) -> None:
        """
        Create or load the vector store with document embeddings.
        
        Args:
            chunks: List of document chunks to embed and store
        """
        if not self.embeddings:
            self.setup_embeddings()
        
        print("🗄️ Creating vector store...")
        start_time = time.time()
        
        # Check if vector store already exists
        if os.path.exists(f"{self.vector_store_path}/chroma.sqlite3"):
            print("📂 Loading existing vector store...")
            self.vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
            print("✅ Vector store loaded from existing data")
        else:
            print("🆕 Creating new vector store...")
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.vector_store_path
            )
            print("✅ Vector store created and saved")
        
        self.stats['processing_time'] = time.time() - start_time
    
    def setup_retriever(self, k: int = 3) -> None:
        """
        Setup the document retriever.
        
        Args:
            k: Number of most relevant chunks to retrieve
        """
        print("🔍 Setting up document retriever...")
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        print("✅ Retriever ready")
    
    def setup_llm(self) -> None:
        """Initialize the language model for generating responses."""
        print("🤖 Initializing language model...")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key
        )
        print("✅ Language model ready")
    
    def create_rag_chain(self) -> None:
        """Create the RAG (Retrieval-Augmented Generation) chain."""
        print("⚙️ Building RAG chain...")
        
        # Create prompt template
        prompt_template = ChatPromptTemplate.from_template("""
        You are an intelligent document analysis assistant. Your task is to answer questions 
        based on the provided context from enterprise documents.
        
        Guidelines:
        - Use ONLY the information provided in the context
        - Be accurate and specific in your responses
        - If the answer cannot be found in the context, clearly state this
        - Provide relevant details and examples when available
        - Maintain a professional tone
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """)
        
        # Format retrieved documents
        def format_docs(docs):
            return "\n\n".join(f"Document: {doc.page_content}" for doc in docs)
        
        # Create the RAG chain
        self.rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | self.llm
            | StrOutputParser()
        )
        print("✅ RAG chain ready")
    
    def initialize(self) -> None:
        """Initialize the complete document intelligence system."""
        print("🚀 Initializing Document Intelligence Agent...")
        print("=" * 60)
        
        try:
            # Load and process documents
            documents = self.load_documents()
            chunks = self.create_chunks(documents)
            
            # Setup AI components
            self.setup_embeddings()
            self.create_vector_store(chunks)
            self.setup_retriever()
            self.setup_llm()
            self.create_rag_chain()
            
            print("=" * 60)
            print("🎉 Document Intelligence Agent Ready!")
            print(f"📊 Statistics:")
            print(f"   • Documents processed: {self.stats['documents_loaded']}")
            print(f"   • Chunks created: {self.stats['chunks_created']}")
            print(f"   • Processing time: {self.stats['processing_time']:.2f}s")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            raise
    
    def ask_question(self, question: str) -> str:
        """
        Ask a question about the documents.
        
        Args:
            question: The question to ask
            
        Returns:
            The answer based on document content
        """
        if not self.rag_chain:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            return f"Error processing question: {e}"
    
    def search_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        Search for relevant document chunks.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant document chunks
        """
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")
        
        return self.vector_store.similarity_search(query, k=k)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.stats.copy()
    
    def interactive_chat(self) -> None:
        """Start an interactive chat session."""
        print("\n💬 Interactive Chat Mode")
        print("Ask questions about your documents. Type 'quit' to exit.")
        print("-" * 60)
        
        while True:
            try:
                question = input("\n❓ Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using Document Intelligence Agent.")
                    break
                
                if not question:
                    print("Please enter a question.")
                    continue
                
                print("\n🔍 Analyzing documents...")
                response = self.ask_question(question)
                print(f"\n📝 Answer: {response}")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    """Main function to run the Document Intelligence Agent."""
    try:
        # Initialize the agent
        agent = DocumentIntelligenceAgent()
        agent.initialize()
        
        # Start interactive chat
        agent.interactive_chat()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
