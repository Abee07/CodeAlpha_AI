import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, Settings, X, Trash2 } from 'lucide-react';
import './ChatBot.css';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! 👋 I'm your FAQ Chatbot. Ask me anything about our services!",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch suggestions as user types
  const fetchSuggestions = async (query) => {
    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/chat/suggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: query,
          top_n: 3
        })
      });

      if (response.ok) {
        const data = await response.json();
        setSuggestions(data.suggestions || []);
        setShowSuggestions(data.suggestions.length > 0);
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    fetchSuggestions(value);
  };

  const sendMessage = async (messageText = null) => {
    const text = messageText || inputValue.trim();
    
    if (!text) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setShowSuggestions(false);
    setSuggestions([]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text
        })
      });

      if (response.ok) {
        const data = await response.json();
        
        const botMessage = {
          id: messages.length + 2,
          text: data.answer,
          sender: 'bot',
          timestamp: new Date(data.timestamp),
          category: data.category,
          similarity: data.similarity,
          matchedQuestion: data.question
        };

        setMessages(prev => [...prev, botMessage]);
      } else {
        const error = await response.json();
        const botMessage = {
          id: messages.length + 2,
          text: error.answer || 'Sorry, I encountered an error. Please try again.',
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const botMessage = {
        id: messages.length + 2,
        text: 'Sorry, I couldn\'t connect to the chatbot service. Please make sure the server is running.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion.question);
    setShowSuggestions(false);
    setSuggestions([]);
    // Send the message after setting state
    setTimeout(() => sendMessage(suggestion.question), 0);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = async () => {
    try {
      await fetch('http://localhost:5000/api/conversation/clear', {
        method: 'POST'
      });
      setMessages([
        {
          id: 1,
          text: "Hi! 👋 I'm your FAQ Chatbot. Ask me anything about our services!",
          sender: 'bot',
          timestamp: new Date()
        }
      ]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chatbot-container">
      {/* Header */}
      <div className="chatbot-header">
        <div className="header-content">
          <MessageCircle size={24} className="header-icon" />
          <h1>FAQ Chatbot</h1>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="header-btn"
            title="Settings"
          >
            <Settings size={20} />
          </button>
          <button
            onClick={clearChat}
            className="header-btn"
            title="Clear chat"
          >
            <Trash2 size={20} />
          </button>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="settings-panel">
            <div className="settings-header">
              <h3>Settings</h3>
              <button onClick={() => setShowSettings(false)} className="close-btn">
                <X size={18} />
              </button>
            </div>
            <div className="settings-content">
              <p className="setting-info">
                ℹ️ This chatbot uses NLTK and TF-IDF vectorization with cosine similarity matching to find the best FAQ answers.
              </p>
              <p className="setting-info">
                💡 Try asking questions like "What languages do you support?" or "How much does it cost?"
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="chatbot-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message-wrapper ${message.sender}`}>
            <div className={`message ${message.sender}`}>
              <div className="message-text">{message.text}</div>
              {message.matchedQuestion && (
                <div className="message-meta">
                  <small>📎 Matched: "{message.matchedQuestion}"</small>
                  <small>✓ Confidence: {(message.similarity * 100).toFixed(0)}%</small>
                </div>
              )}
              <div className="message-time">{formatTime(message.timestamp)}</div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message-wrapper bot">
            <div className="message bot">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="suggestions-container">
          <div className="suggestions-header">Suggested questions:</div>
          <div className="suggestions-list">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-item"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                <span className="suggestion-text">{suggestion.question}</span>
                <span className="suggestion-confidence">
                  {(suggestion.similarity * 100).toFixed(0)}%
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="chatbot-input-area">
        <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
          <div className="input-wrapper">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything... (Shift+Enter for new line)"
              className="input-field"
              rows="2"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="send-button"
              disabled={!inputValue.trim() || isLoading}
              title="Send message"
            >
              <Send size={20} />
            </button>
          </div>
        </form>
        <div className="input-footer">
          <small>💬 Powered by NLTK & Cosine Similarity Matching</small>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
