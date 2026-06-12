# 🤖 AI FAQs Chatbot

An interactive, web-based AI Chatbot designed to help engineering students master fundamental Artificial Intelligence and Machine Learning interview questions. Built as part of the **CodeAlpha Virtual Internship** program.

This application transitions away from static interfaces to offer a dynamic, real-time **vibe-coding** user experience featuring a conversational chat log layout, automatic response streaming, and interactive sample queries.

---

## 🌟 Key Features

*   **💬 Conversational Chat UI:** Simulates a modern chat application interface that securely maintains session history.
*   **💡 Interactive Sample Questions:** A sidebar populated with common technical questions. Clicking any question instantly populates the chat and pulls the answer.
*   **⚡ Real-Time Streaming Effect:** Uses automated delays to stream responses letter-by-letter for an organic conversational flow.
*   **🔄 History Management:** Includes a dedicated "Clear Chat" button to flush short-term session state memory and reset the context instantly.
*   **🖥️ Wide Screen Optimization:** Features a clean, dual-column responsive web layout.

---

## 🧠 The AI Aspect Explained

Even though this tool operates without heavy, resource-intensive deep learning servers, it utilizes advanced mathematical algorithms from the field of **Natural Language Processing (NLP)**:

1.  **Text Vectorization (`TfidfVectorizer`):** Computers cannot read English words directly. The system converts text strings into mathematical structures called vectors by calculating word frequencies and importance rankings.
2.  **Semantic Similarity Matching (`cosine_similarity`):** When a user types a prompt, the algorithm treats it as a vector and calculates the geometric angle between the user's string and the stored database questions. 
3.  **Confidence Thresholding:** If the closest calculated matching score is too low (below 0.2), the system dynamically routes to a helpful fall-back safety response instead of failing.

---

## 🛠️ Tech Stack Used

*   **Language:** Python
*   **UI Framework:** Streamlit (Web App Engine)
*   **Mathematical Operations:** NumPy
*   **Machine Learning Engine:** Scikit-Learn (Simple NLP Models)

---

## 💻 Local Setup Instructions

Follow these quick steps to get the chatbot up and running on your personal computer:

### 1. Clone or Download the Project
Ensure you have downloaded the code files into a dedicated folder on your machine.

### 2. Install Dependencies
Open your system terminal or code editor panel and install the required external libraries using the provided text requirements file:
```bash
pip install streamlit scikit-learn numpy
```

### 3. Launch the Web Server
Because Streamlit boots up a local web server to display your graphical layout, bypass standard execution constraints by running the module shortcut command:
```bash
python -m streamlit run faq_chatbot.py
```

After running the command, your terminal will generate a local network loopback address (`http://localhost:8501`), and your web browser will automatically open up your application!

---

## 📂 Project Structure

```text
├── faq_chatbot.py     # Core application script containing UI logic and matching math
├── README.md          # Project documentation and guide sheet
```
