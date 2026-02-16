import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { SearchRequest } from "@/util/types";
import '@/styles/qna.css';

interface SourceDocument {
  document_name: string;
  document_id: number;
  score: number;
}

interface ChatMessage {
  id: number;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  sources?: SourceDocument[];
}

interface LLMResponse {
  response: string;
  sources?: SourceDocument[];
}

export default function QnAPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {

      const search_request: SearchRequest = {
        query: inputText,
        category_ids: undefined
      }
      const response = await fetch('http://127.0.0.1:8000/rag/qna', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(search_request),
      });

      if (!response.ok) {
        throw new Error(`Error Status: ${response.status}`);
      }
      const data : LLMResponse = await response.json();

      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        text: data.response || 'Sorry, I could not find an answer to your question in the knowledge base.',
        sender: 'assistant',
        timestamp: new Date(),
        sources: data.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);

    } catch {

      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error retrieving information from the knowledge base. Please try again.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);

    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    if (messages.length > 0 && confirm('Are you sure you want to clear the chat history?')) {
      setMessages([]);
    }
  };

  return (
    <div className="qna-page">
      <div className="qna-container">

        {/* Header */}
        <div className="qna-header">
          <div className="header-content">
            <h1 className="qna-title">Knowledge Base Q&A</h1>
            <p className="qna-subtitle">Search and retrieve information from your documents</p>
          </div>
          {messages.length > 0 && (
            <button className="clear-chat-button" onClick={handleClearChat}>
              Clear History
            </button>
          )}
        </div>

        {/* Chat Messages */}
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📚</div>
              <h2>Query Your Knowledge Base</h2>
              <p>Ask questions and get answers with cited sources from your documents</p>
              <div className="suggestion-chips">
                <button
                  className="suggestion-chip"
                  onClick={() => setInputText('What information is available about ')}
                >
                  What information is available about ...
                </button>
                <button
                  className="suggestion-chip"
                  onClick={() => setInputText('Create a summary on ')}
                >
                  Create a summary on ...
                </button>
                <button
                  className="suggestion-chip"
                  onClick={() => setInputText('What are the specific requirements for')}
                >
                  What are the specific requirements for ...
                </button>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  <div className="message-avatar">
                    {message.sender === 'user' ? '👤' : '📖'}
                  </div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-label">
                        {message.sender === 'user' ? 'Query' : 'Retrieved Answer'}
                      </span>
                    </div>
                    <div className="message-text">{message.text}</div>
                    
                    {/* Source Citations */}
                    {message.sender === 'assistant' && message.sources && message.sources.length > 0 && (
                      <div className="sources-section">
                        <div className="sources-header">
                          <span className="sources-icon">🔗</span>
                          <span className="sources-title">Source Documents ({message.sources.length})</span>
                        </div>
                        <div className="sources-list">
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="source-item">
                              <div className="source-info">
                                <span className="source-number">{idx + 1}</span>
                                <div className="source-details">
                                  <Link 
                                    to={`/document/${source.document_id}`}
                                    className="source-name"
                                  >
                                    {source.document_name}
                                  </Link>
                                  <div className="source-meta">
                                    <span className="relevance-badge">
                                      Relevance: {(source.score * 100).toFixed(0)}%
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="message-timestamp">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message assistant-message">
                  <div className="message-avatar">📖</div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-label">Searching Knowledge Base</span>
                    </div>
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <textarea
              className="chat-input"
              placeholder="Ask a question about your documents..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              rows={1}
              disabled={isLoading}
            />
            <button
              className="send-button"
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
            >
              <span className="send-icon">🔍</span>
            </button>
          </div>
          <p className="input-hint">Press Enter to search • Shift + Enter for new line</p>
        </div>
      </div>
    </div>
  );
}