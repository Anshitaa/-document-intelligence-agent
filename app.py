#!/usr/bin/env python3
"""
Document Intelligence Agent - Web Interface
==========================================

A beautiful Streamlit web interface for the Document Intelligence Agent.
Features interactive chat, document analysis, and real-time statistics.
"""

import streamlit as st
import os
import time
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

# Import our agent
from document_intelligence_agent import DocumentIntelligenceAgent

# Page configuration
st.set_page_config(
    page_title="Document Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        margin-right: 20%;
        border-left: 4px solid #667eea;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'stats' not in st.session_state:
    st.session_state.stats = {}

def initialize_agent():
    """Initialize the Document Intelligence Agent."""
    try:
        with st.spinner("🚀 Initializing Document Intelligence Agent..."):
            agent = DocumentIntelligenceAgent()
            agent.initialize()
            st.session_state.agent = agent
            st.session_state.initialized = True
            st.session_state.stats = agent.get_stats()
        return True
    except Exception as e:
        st.error(f"❌ Error initializing agent: {e}")
        return False

def display_chat_message(message: str, is_user: bool = True):
    """Display a chat message with appropriate styling."""
    if is_user:
        st.markdown(f'<div class="chat-message user-message">👤 {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message">🤖 {message}</div>', unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Document Intelligence Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Agent Status")
        
        if st.session_state.initialized:
            st.markdown('<p class="status-success">✅ Agent Ready</p>', unsafe_allow_html=True)
            
            # Display statistics
            st.markdown("### 📈 Statistics")
            stats = st.session_state.stats
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Documents", stats.get('documents_loaded', 0))
                st.metric("Chunks", stats.get('chunks_created', 0))
            
            with col2:
                st.metric("Processing Time", f"{stats.get('processing_time', 0):.1f}s")
            
            # Agent configuration
            st.markdown("### ⚙️ Configuration")
            st.info(f"**Embedding Model:** sentence-transformers/all-MiniLM-L6-v2")
            st.info(f"**Vector Store:** ChromaDB")
            st.info(f"**Language Model:** GPT-3.5-turbo")
            
        else:
            st.markdown('<p class="status-error">❌ Agent Not Initialized</p>', unsafe_allow_html=True)
            st.markdown("Click 'Initialize Agent' to start")
        
        st.markdown("---")
        
        # Initialize button
        if not st.session_state.initialized:
            if st.button("🚀 Initialize Agent", type="primary", use_container_width=True):
                initialize_agent()
                st.rerun()
        
        # Clear chat button
        if st.session_state.initialized:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Document upload section
        st.markdown("### 📄 Document Management")
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload PDF files to analyze"
        )
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} files uploaded")
            # Note: In a real implementation, you'd save these files to the data directory
    
    # Main content area
    if not st.session_state.initialized:
        # Welcome screen
        st.markdown("## 🎯 Welcome to Document Intelligence Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### What is this?
            The Document Intelligence Agent is a sophisticated RAG (Retrieval-Augmented Generation) 
            system that can analyze your PDF documents and answer questions about their content.
            
            ### Features:
            - 📄 **PDF Processing**: Automatically loads and processes PDF documents
            - 🧠 **AI-Powered**: Uses advanced AI models for intelligent analysis
            - 💬 **Interactive Chat**: Ask questions and get intelligent answers
            - 🔍 **Semantic Search**: Find relevant information using vector similarity
            - 💰 **Cost-Effective**: Uses free HuggingFace embeddings
            - 📊 **Real-time Stats**: Monitor processing and performance metrics
            
            ### How to get started:
            1. Place your PDF files in the `data/` directory
            2. Click "Initialize Agent" in the sidebar
            3. Start asking questions about your documents!
            """)
        
        with col2:
            st.markdown("### 🚀 Quick Start")
            st.info("""
            **Prerequisites:**
            - PDF files in `data/` folder
            - OpenAI API key in `.env` file
            - All dependencies installed
            """)
            
            if st.button("📖 View Documentation", use_container_width=True):
                st.info("Check the README.md file for detailed instructions")
    
    else:
        # Main chat interface
        st.markdown("## 💬 Chat with Your Documents")
        
        # Chat input
        user_input = st.chat_input("Ask a question about your documents...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get response from agent
            with st.spinner("🔍 Analyzing documents..."):
                try:
                    response = st.session_state.agent.ask_question(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {e}"
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                display_chat_message(message["content"], is_user=True)
            else:
                display_chat_message(message["content"], is_user=False)
        
        # Quick action buttons
        st.markdown("### 🎯 Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Main Topic"):
                if st.session_state.agent:
                    response = st.session_state.agent.ask_question("What is the main topic of the documents?")
                    st.session_state.chat_history.append({"role": "user", "content": "What is the main topic of the documents?"})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
        
        with col2:
            if st.button("🔍 Key Findings"):
                if st.session_state.agent:
                    response = st.session_state.agent.ask_question("What are the key findings in the documents?")
                    st.session_state.chat_history.append({"role": "user", "content": "What are the key findings in the documents?"})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
        
        with col3:
            if st.button("📈 Statistics"):
                if st.session_state.agent:
                    response = st.session_state.agent.ask_question("What statistics or data are mentioned in the documents?")
                    st.session_state.chat_history.append({"role": "user", "content": "What statistics or data are mentioned in the documents?"})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
        
        with col4:
            if st.button("💡 Recommendations"):
                if st.session_state.agent:
                    response = st.session_state.agent.ask_question("What recommendations are provided in the documents?")
                    st.session_state.chat_history.append({"role": "user", "content": "What recommendations are provided in the documents?"})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
        
        # Analytics section
        st.markdown("---")
        st.markdown("## 📊 Document Analytics")
        
        if st.session_state.agent:
            # Document search functionality
            search_query = st.text_input("🔍 Search documents for specific information:")
            if search_query:
                try:
                    results = st.session_state.agent.search_documents(search_query, k=3)
                    st.markdown(f"**Found {len(results)} relevant chunks:**")
                    
                    for i, doc in enumerate(results, 1):
                        with st.expander(f"Result {i}"):
                            st.text(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                except Exception as e:
                    st.error(f"Search error: {e}")
            
            # Performance metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Documents Processed",
                    st.session_state.stats.get('documents_loaded', 0),
                    help="Total number of PDF documents loaded"
                )
            
            with col2:
                st.metric(
                    "Chunks Created",
                    st.session_state.stats.get('chunks_created', 0),
                    help="Total number of document chunks created"
                )
            
            with col3:
                st.metric(
                    "Processing Time",
                    f"{st.session_state.stats.get('processing_time', 0):.1f}s",
                    help="Time taken to process all documents"
                )

if __name__ == "__main__":
    main()
