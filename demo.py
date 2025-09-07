#!/usr/bin/env python3
"""
Document Intelligence Agent - Demo Script
=========================================

This script demonstrates the capabilities of the Document Intelligence Agent
with sample questions and responses.
"""

from document_intelligence_agent import DocumentIntelligenceAgent
import time

def run_demo():
    """Run a demonstration of the Document Intelligence Agent."""
    
    print("🎬 Document Intelligence Agent - Demo")
    print("=" * 50)
    
    # Sample questions to demonstrate capabilities
    demo_questions = [
        "What is the main topic discussed in the documents?",
        "What are the key findings or conclusions?",
        "Are there any statistics or data mentioned?",
        "What methodologies are discussed?",
        "What are the main challenges or problems addressed?",
        "What recommendations are provided?",
        "Who are the authors or organizations mentioned?",
        "What is the scope or context of the research?"
    ]
    
    try:
        # Initialize the agent
        print("🚀 Initializing Document Intelligence Agent...")
        agent = DocumentIntelligenceAgent()
        agent.initialize()
        
        print("\n📊 Agent Statistics:")
        stats = agent.get_stats()
        for key, value in stats.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print("\n" + "=" * 50)
        print("🎯 Demo Questions and Answers")
        print("=" * 50)
        
        # Ask demo questions
        for i, question in enumerate(demo_questions, 1):
            print(f"\n❓ Question {i}: {question}")
            print("🔍 Searching documents...")
            
            start_time = time.time()
            answer = agent.ask_question(question)
            response_time = time.time() - start_time
            
            print(f"📝 Answer: {answer}")
            print(f"⏱️ Response time: {response_time:.2f} seconds")
            print("-" * 50)
            
            # Add a small delay for readability
            time.sleep(1)
        
        print("\n🎉 Demo completed successfully!")
        print("The agent is ready for interactive use.")
        print("Run 'python document_intelligence_agent.py' to start chatting!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have:")
        print("1. PDF files in the 'data/' directory")
        print("2. Valid OPENAI_API_KEY in .env file")
        print("3. All dependencies installed")

if __name__ == "__main__":
    run_demo()
