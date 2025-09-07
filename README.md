# Document Intelligence Agent

A sophisticated RAG (Retrieval-Augmented Generation) system for enterprise document analysis. This agent can process PDF documents, create semantic embeddings, and answer questions based on document content using advanced AI models.

## 🌟 Features

- **🌐 Beautiful Web Interface**: Modern, responsive Streamlit UI with real-time chat
- **📄 PDF Document Processing**: Automatically loads and processes PDF documents from a directory
- **🧠 Intelligent Chunking**: Splits documents into optimal chunks for better processing
- **🆓 Free Embeddings**: Uses HuggingFace sentence transformers for cost-effective semantic search
- **💾 Persistent Storage**: ChromaDB vector store for efficient document retrieval
- **🤖 OpenAI Integration**: GPT-3.5-turbo for intelligent question answering
- **💬 Interactive Chat**: Both web and command-line interfaces
- **📊 Real-time Analytics**: Live statistics and document search
- **⚡ Batch Processing**: Handles large document sets efficiently
- **🏗️ Professional Architecture**: Clean, modular, and well-documented code

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- PDF documents in the `data/` directory

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd document-intelligence-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Add your PDF documents**
   ```bash
   # Place your PDF files in the data/ directory
   mkdir data
   cp your_documents.pdf data/
   ```

### Running the Application

#### Option 1: Web Interface (Recommended) 🌐
```bash
# Easy launch with automatic checks
./start_web_ui.sh

# Or manually
python run_web_app.py

# Or directly with Streamlit
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

#### Option 2: Command Line Interface 💻
```bash
python document_intelligence_agent.py
```

#### Option 3: Programmatic Usage 🐍
```bash
python example_usage.py
```

## 📁 Project Structure

```
document-intelligence-agent/
├── app.py                         # 🌐 Streamlit web interface
├── run_web_app.py                 # Web app launcher
├── start_web_ui.sh               # Easy launch script
├── document_intelligence_agent.py # Main agent implementation
├── demo.py                        # Interactive demo script
├── example_usage.py               # Programmatic usage examples
├── requirements.txt               # Python dependencies
├── setup.py                      # Package installation script
├── README.md                     # This file
├── .env                          # Environment variables (create this)
├── data/                         # PDF documents directory
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
└── chroma_db/                    # Vector database (created automatically)
```

## 🔧 Configuration

The agent can be customized by modifying the initialization parameters:

```python
agent = DocumentIntelligenceAgent(
    data_directory="./data",           # PDF files directory
    vector_store_path="./chroma_db",   # Vector database location
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",  # Embedding model
    chunk_size=1000,                   # Document chunk size
    chunk_overlap=200                  # Overlap between chunks
)
```

## 💡 Usage Examples

### Basic Usage

```python
from document_intelligence_agent import DocumentIntelligenceAgent

# Initialize the agent
agent = DocumentIntelligenceAgent()
agent.initialize()

# Ask questions
answer = agent.ask_question("What is the main topic of the documents?")
print(answer)

# Search for specific information
results = agent.search_documents("climate change", k=5)
for doc in results:
    print(doc.page_content)
```

### Interactive Mode

```bash
python document_intelligence_agent.py
```

This will start an interactive chat session where you can ask questions about your documents.

## 🏗️ Architecture

### Components

1. **Document Loader**: Loads PDF files using PyPDFLoader
2. **Text Splitter**: Splits documents into manageable chunks
3. **Embedding Model**: Creates semantic embeddings using HuggingFace
4. **Vector Store**: Stores and retrieves document chunks using ChromaDB
5. **Retriever**: Finds relevant document chunks for queries
6. **Language Model**: Generates answers using OpenAI GPT
7. **RAG Chain**: Combines retrieval and generation for intelligent responses

### Data Flow

```
PDF Documents → Chunking → Embeddings → Vector Store
                                                      ↓
User Query → Retrieval → Context + Query → LLM → Answer
```

## 🔍 Key Features Explained

### Cost-Effective Design
- Uses free HuggingFace embeddings instead of expensive OpenAI embeddings
- Only uses OpenAI for the final answer generation (minimal cost)
- Processes documents locally without API calls

### Intelligent Chunking
- Recursive character splitting for optimal chunk sizes
- Configurable overlap to maintain context
- Handles various document structures

### Semantic Search
- Vector-based similarity search
- Finds relevant information even with different wording
- Configurable number of results

### Professional Code Quality
- Type hints for better code maintainability
- Comprehensive error handling
- Modular design for easy extension
- Detailed documentation

## 📊 Performance

- **Processing Speed**: ~2-5 minutes for 100+ page documents
- **Memory Usage**: Efficient chunking reduces memory footprint
- **Accuracy**: High-quality semantic search with relevant results
- **Cost**: Minimal API usage (only for final answer generation)

## 🛠️ Dependencies

- `langchain`: Core RAG framework
- `langchain-community`: Community integrations
- `langchain-openai`: OpenAI integration
- `sentence-transformers`: Free embedding models
- `chromadb`: Vector database
- `pypdf`: PDF processing
- `python-dotenv`: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain team for the excellent RAG framework
- HuggingFace for free embedding models
- OpenAI for the powerful language models
- ChromaDB for efficient vector storage

## 📞 Support

For questions or issues, please open an issue on GitHub or contact [your-email].

---

**Built with ❤️ for the AI community**
