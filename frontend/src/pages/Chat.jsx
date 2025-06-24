import { useState, useEffect, useRef, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import './Chat.css';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [availableTools, setAvailableTools] = useState([]);
  const [toolsUsed, setToolsUsed] = useState([]);
  const messagesEndRef = useRef(null);
  const { token } = useContext(AuthContext);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (token) {
      checkConnection();
      loadAvailableTools();
    }
  }, [token]);

  const checkConnection = async () => {
    try {
      const response = await axios.get('http://localhost:5000/ai-chat/health', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setIsConnected(response.data.ollama_connected && response.data.agent_initialized);
      setError(null);
    } catch (err) {
      setIsConnected(false);
      setError('Cannot connect to AI service. Please make sure the backend and Ollama are running.');
    }
  };

  const loadAvailableTools = async () => {
    try {
      const response = await axios.get('http://localhost:5000/ai-chat/tools', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAvailableTools(response.data.tools || []);
    } catch (err) {
      console.error('Failed to load tools:', err);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading || !token) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);
    setToolsUsed([]);

    try {
      // Prepare chat history for the agent
      const chatHistory = messages
        .filter(msg => msg.sender === 'user' || msg.sender === 'ai')
        .map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        }));

      const response = await axios.post('http://localhost:5000/ai-chat/chat', {
        message: inputMessage,
        chat_history: chatHistory
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const aiMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString(),
        model: response.data.model,
        toolsUsed: response.data.tools_used,
        toolDetails: response.data.tool_details
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Update tools used if any
      if (response.data.tools_used) {
        setToolsUsed(response.data.tool_details || []);
      }
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        text: err.response?.data?.error || 'Failed to get response from AI',
        sender: 'error',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
      setError(err.response?.data?.error || 'An error occurred while communicating with the AI');
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
    setToolsUsed([]);
  };

  const renderToolUsage = (toolDetails) => {
    if (!toolDetails || toolDetails.length === 0) return null;
    
    return (
      <div className="tool-usage">
        <div className="tool-indicator">
          <span className="tool-icon">🔧</span>
          <span className="tool-text">Tools used: {toolDetails.length}</span>
        </div>
        {toolDetails.map((step, index) => (
          <div key={index} className="tool-step">
            <div className="tool-name">{step[0].tool}</div>
            <div className="tool-input">{step[0].tool_input}</div>
            <div className="tool-output">{step[1]}</div>
          </div>
        ))}
      </div>
    );
  };

  if (!token) {
    return (
      <div className="chat-container">
        <div className="auth-required">
          <h2>Authentication Required</h2>
          <p>Please log in to use the AI chat assistant.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>AI Chat Assistant with Tools</h1>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '●' : '○'}
          </span>
          <span className="status-text">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        <button onClick={clearChat} className="clear-button">
          Clear Chat
        </button>
      </div>

      {availableTools.length > 0 && (
        <div className="tools-info">
          <h3>Available Tools ({availableTools.length})</h3>
          <div className="tools-list">
            {availableTools.map((tool, index) => (
              <div key={index} className="tool-item">
                <strong>{tool.name}:</strong> {tool.description}
              </div>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={checkConnection} className="retry-button">
            Retry Connection
          </button>
        </div>
      )}

      <div className="messages-container">
        {messages.length === 0 && !isLoading && (
          <div className="welcome-message">
            <h3>Welcome to AI Chat with Tools!</h3>
            <p>This AI assistant can use tools to provide better responses.</p>
            <p>Try asking about your message history or communication patterns!</p>
            <div className="example-prompts">
              <p><strong>Example prompts:</strong></p>
              <ul>
                <li>"Can you summarize my recent messages?"</li>
                <li>"What have I been talking about this week?"</li>
                <li>"Show me my message patterns from the last month"</li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'} ${message.sender === 'error' ? 'error-message' : ''}`}
          >
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              {message.toolsUsed && renderToolUsage(message.toolDetails)}
              <div className="message-meta">
                <span className="message-time">{message.timestamp}</span>
                {message.model && (
                  <span className="model-info">via {message.model}</span>
                )}
                {message.toolsUsed && (
                  <span className="tools-used">🔧 Tools used</span>
                )}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <div className="loading-indicator">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="loading-text">AI is thinking and may use tools...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here... (Try asking about your message history!)"
            disabled={isLoading || !isConnected}
            className="message-input"
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim() || !isConnected}
            className="send-button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22,2 15,22 11,13 2,9"></polygon>
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
}