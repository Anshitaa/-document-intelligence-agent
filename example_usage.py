#!/usr/bin/env python3
"""
Example Usage of Document Intelligence Agent
===========================================

This script shows how to use the Document Intelligence Agent
programmatically in your own applications.
"""

from document_intelligence_agent import DocumentIntelligenceAgent

def main():
    """Example of using the Document Intelligence Agent."""
    
    print("📚 Document Intelligence Agent - Example Usage")
    print("=" * 50)
    
    try:
        # Initialize the agent
        print("1. Initializing agent...")
        agent = DocumentIntelligenceAgent(
            data_directory="./data",
            vector_store_path="./chroma_db",
            chunk_size=1000,
            chunk_overlap=200
        )
        agent.initialize()
        
        # Example 1: Ask a simple question
        print("\n2. Asking a simple question...")
        question1 = "What is the main topic of the documents?"
        answer1 = agent.ask_question(question1)
        print(f"Q: {question1}")
        print(f"A: {answer1}")
        
        # Example 2: Search for specific information
        print("\n3. Searching for specific information...")
        search_query = "climate change"
        results = agent.search_documents(search_query, k=3)
        print(f"Search results for '{search_query}':")
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc.page_content[:100]}...")
        
        # Example 3: Ask a complex question
        print("\n4. Asking a complex question...")
        question2 = "What are the key findings and recommendations?"
        answer2 = agent.ask_question(question2)
        print(f"Q: {question2}")
        print(f"A: {answer2}")
        
        # Example 4: Get statistics
        print("\n5. Agent statistics:")
        stats = agent.get_stats()
        for key, value in stats.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have PDF files in the 'data/' directory")

if __name__ == "__main__":
    main()
