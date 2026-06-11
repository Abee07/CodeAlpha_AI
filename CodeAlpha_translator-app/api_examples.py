"""
FAQ Chatbot - API Usage Examples
This file shows how to use the chatbot API endpoints
"""

import requests
import json
from typing import Dict, List, Optional

BASE_URL = "http://localhost:5000"

class ChatbotAPIClient:
    """Client for interacting with FAQ Chatbot API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def chat(self, message: str) -> Dict:
        """
        Send a message to the chatbot
        
        Args:
            message: User's question
            
        Returns:
            Response dict with answer, confidence, etc.
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"message": message}
        )
        return response.json()
    
    def get_suggestions(self, message: str, top_n: int = 3) -> List[Dict]:
        """
        Get top matching FAQs for a message
        
        Args:
            message: Query text
            top_n: Number of suggestions to return
            
        Returns:
            List of suggestion dicts
        """
        response = requests.post(
            f"{self.base_url}/api/chat/suggestions",
            json={"message": message, "top_n": top_n}
        )
        return response.json().get('suggestions', [])
    
    def get_all_faqs(self) -> List[Dict]:
        """Get all FAQs"""
        response = requests.get(f"{self.base_url}/api/faqs")
        return response.json().get('faqs', [])
    
    def get_faq_by_category(self, category: str) -> List[Dict]:
        """Get FAQs filtered by category"""
        response = requests.get(f"{self.base_url}/api/faqs/category/{category}")
        return response.json().get('faqs', [])
    
    def add_faq(self, question: str, answer: str, category: str = "general") -> Dict:
        """Add a new FAQ"""
        response = requests.post(
            f"{self.base_url}/api/faq/add",
            json={
                "question": question,
                "answer": answer,
                "category": category
            }
        )
        return response.json()
    
    def export_faqs(self) -> List[Dict]:
        """Export all FAQs"""
        response = requests.get(f"{self.base_url}/api/faqs/export")
        return response.json().get('faqs', [])
    
    def get_conversation(self) -> List[Dict]:
        """Get conversation history"""
        response = requests.get(f"{self.base_url}/api/conversation")
        return response.json().get('conversation', [])
    
    def clear_conversation(self) -> Dict:
        """Clear conversation history"""
        response = requests.post(f"{self.base_url}/api/conversation/clear")
        return response.json()
    
    def health_check(self) -> Dict:
        """Check if server is running"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_basic_chat():
    """Example: Basic chat interaction"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Chat")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    questions = [
        "What languages do you support?",
        "How much does it cost?",
        "Is my data secure?"
    ]
    
    for question in questions:
        print(f"\n👤 User: {question}")
        response = client.chat(question)
        print(f"🤖 Bot: {response['answer']}")
        print(f"📊 Confidence: {response['similarity']*100:.1f}%")
        if response['question']:
            print(f"📎 Matched FAQ: {response['question']}")


def example_get_suggestions():
    """Example: Get suggestions for partial query"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Get Suggestions")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    queries = ["pricing", "languages", "support"]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        suggestions = client.get_suggestions(query, top_n=3)
        for i, sugg in enumerate(suggestions, 1):
            print(f"  {i}. {sugg['question']} ({sugg['similarity']*100:.0f}%)")


def example_manage_faqs():
    """Example: List FAQs and add new one"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Manage FAQs")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    # Get all FAQs
    faqs = client.get_all_faqs()
    print(f"\nTotal FAQs: {len(faqs)}")
    
    # Show by category
    print("\nFAQs by category:")
    categories = {}
    for faq in faqs:
        cat = faq['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"  • {cat}: {count}")
    
    # Add new FAQ
    print("\nAdding new FAQ...")
    result = client.add_faq(
        question="Do you support video translation?",
        answer="Yes, we translate video subtitles and audio.",
        category="features"
    )
    print(f"✓ Added: {result.get('message', 'Success')}")
    
    # Verify it works
    print("\nTesting new FAQ...")
    response = client.chat("Can you translate videos?")
    print(f"Match confidence: {response['similarity']*100:.1f}%")


def example_category_filter():
    """Example: Filter FAQs by category"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Filter by Category")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    categories = ["pricing", "translation", "security"]
    
    for category in categories:
        faqs = client.get_faq_by_category(category)
        print(f"\n📁 {category.upper()} ({len(faqs)} FAQs):")
        for faq in faqs:
            print(f"  • {faq['question']}")


def example_conversation_history():
    """Example: View and clear conversation"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Conversation History")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    # Send some messages
    print("\nSending messages...")
    client.chat("What languages are supported?")
    client.chat("How much does it cost?")
    client.chat("How do I contact support?")
    
    # Get history
    history = client.get_conversation()
    print(f"\nConversation history ({len(history)} messages):")
    for i, item in enumerate(history[-3:], 1):
        print(f"\n{i}. User: {item['user_message']}")
        print(f"   Bot: {item['bot_response']['answer'][:60]}...")
    
    # Clear
    print("\nClearing conversation...")
    client.clear_conversation()
    history = client.get_conversation()
    print(f"✓ Cleared. History now has {len(history)} messages")


def example_export_data():
    """Example: Export FAQ data"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Export FAQs")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    faqs = client.export_faqs()
    print(f"\nExported {len(faqs)} FAQs")
    
    # Save to file
    with open('exported_faqs.json', 'w') as f:
        json.dump(faqs, f, indent=2)
    print("✓ Saved to exported_faqs.json")
    
    # Show structure
    if faqs:
        print(f"\nExample FAQ structure:")
        print(json.dumps(faqs[0], indent=2))


def example_health_check():
    """Example: Health check"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Health Check")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    try:
        health = client.health_check()
        print(f"\n✓ Server is running!")
        print(f"  Status: {health['status']}")
        print(f"  FAQ count: {health['faq_count']}")
        print(f"  Timestamp: {health['timestamp']}")
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to server!")
        print("  Make sure Flask is running: python server.py")


def example_error_handling():
    """Example: Error handling"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Error Handling")
    print("="*70)
    
    client = ChatbotAPIClient()
    
    # Test empty message
    print("\n1. Empty message:")
    response = client.chat("")
    if 'error' in response:
        print(f"   ✓ Error handled: {response['error']}")
    
    # Test adding FAQ with missing fields
    print("\n2. Add FAQ with missing answer:")
    response = client.add_faq("Question?", "", "test")
    if 'error' in response:
        print(f"   ✓ Error handled: {response['error']}")
    
    # Test non-existent category
    print("\n3. Filter non-existent category:")
    faqs = client.get_faq_by_category("nonexistent")
    print(f"   ✓ Returns empty list: {len(faqs)} FAQs")


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█  FAQ CHATBOT - API USAGE EXAMPLES" + " " * 33 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    print("\nMake sure the Flask server is running:")
    print("  python server.py\n")
    
    try:
        # Run examples
        example_health_check()
        example_basic_chat()
        example_get_suggestions()
        example_manage_faqs()
        example_category_filter()
        example_conversation_history()
        example_export_data()
        example_error_handling()
        
        print("\n" + "="*70)
        print("✅ All examples completed!")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Please make sure the Flask server is running:")
        print("  python server.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
