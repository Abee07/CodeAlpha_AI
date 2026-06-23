import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

# 🔥 CRITICAL FIX: Force the sidebar to always appear expanded on load!
st.set_page_config(initial_sidebar_state="expanded", layout="wide")

# 1. Setup Technical AI FAQ Data
faq_data = {
    "What is the difference between AI, Machine Learning, and Deep Learning?": 
        "AI is the broad concept of machines acting smartly. Machine Learning (ML) is a subset of AI where machines learn from data without strict rules. Deep Learning (DL) is a subset of ML that uses deep multi-layer neural networks inspired by the human brain.",
    
    "What is the role of an Activation Function in neural networks?": 
        "Activation functions (like ReLU or Sigmoid) add non-linearity to a network. Without them, the network would just act like a simple linear regression model, making it unable to learn complex patterns.",
    
    "What is Overfitting and how do you prevent it?": 
        "Overfitting happens when a model learns the training data and noise too well, causing it to perform poorly on new test data. You can prevent it using Dropout layers, L1/L2 Regularization, or Early Stopping.",
    
    "What is the difference between Supervised and Unsupervised Learning?": 
        "Supervised Learning uses labeled data where the correct answer is known (e.g., house price prediction). Unsupervised Learning works on unlabeled data to find hidden clusters (e.g., customer segmentation).",

    "What is AI?":
        "Artificial Intelligence (AI) is computer technology designed to simulate human intelligence. It enables machines to learn from data, reason, recognize patterns, understand language, and make decisions to solve complex problems.",

    "What is Agent in AI?":
        "An AI agent is a software program that autonomously perceives its environment, makes decisions, and takes actions to achieve a specific goal."
}
questions = list(faq_data.keys())

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# 2. Create the Sidebar Elements
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebarContent"] {
        padding-top: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("🗨️ Chat")

# 🔥 CHANGED: Set both top and bottom margins to 15px to create equal gaps on both sides
st.sidebar.markdown("<hr style='margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)

st.sidebar.subheader("💡 Interactive Sample Questions")
st.sidebar.write("Click any question below to instantly see the answer:")



# Interactive sidebar buttons
for q in questions:
    if st.sidebar.button(q, key=q):
        st.session_state.pending_query = q

# Clear conversation button
if st.sidebar.button("🔄 Clear Chat", key="clear_chat"):
    st.session_state.messages = []
    st.session_state.pending_query = None
    st.rerun()

# 3. Main Chatbot Interface Layout
st.title("🤖 ChatAI")

# Custom Large Font Greeting
st.markdown("<h2 style='font-size:28px;'>Hello! How can I help you today?</h2>", unsafe_allow_html=True)
st.write("Ask me foundational Artificial Intelligence and Machine Learning concepts to test your coding round knowledge.")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Type your question here or click an option from the sidebar:")

# Use pending query from sidebar button if available, otherwise use chat input
if st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

# 4. Math Logic Matching System (scikit-learn)
if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Find best match and generate response
    vectorizer = TfidfVectorizer()
    all_text = questions + [user_query]
    tfidf_matrix = vectorizer.fit_transform(all_text)
    
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    best_match_idx = np.argmax(scores)
    
    # Display assistant response with typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if scores[best_match_idx] > 0.2:
            matched_question = questions[best_match_idx]
            answer = faq_data[matched_question]
        else:
            answer = "I am sorry, I couldn't find a close answer to that in my technical database. Try asking about Overfitting, Activation Functions, or ML vs DL!"
        
        # Simulate streaming effect by displaying text character by character
        displayed_text = ""
        for char in answer:
            displayed_text += char
            message_placeholder.markdown(displayed_text + "▌")
            time.sleep(0.01)
        
        # Final display without cursor
        message_placeholder.markdown(answer)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    st.rerun()
