'use client'

import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from "react-markdown";

interface Message {
    role: 'user' | 'assistant'
    content: string
    sources?: Array<{ file: string; content: string}>
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null);
  
    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);
  
    const sendMessage = async () => {
        if (!input.trim()) return
        
        const userMessage: Message = { role: 'user', content: input }
        setMessages(prev => [...prev, userMessage])
        setInput("")
        setLoading(true)

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: input,
                    chat_history: messages.map(m => ({
                        role: m.role,
                        content: m.content
                    }))
                })
            })
          
            if (!response.ok) throw new Error('Failed to get response')
          
            const data = await response.json()

            const botMessage: Message = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources
            }
            setMessages(prev => [...prev, botMessage])
        } catch (error) {
            console.error('Error:', error)
            // TODO 3: Add error message
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: "❌ Sorry, something went wrong. Please try again.",
              },
            ]);
        } finally {
            setLoading(false)
        }
  }
  
  const clearChat = () => {
    if (confirm("Clear all messages?")) {
      setMessages([]);
    }
  };

  const exampleQuestions = [
    "🇹🇭 Tell me about Thailand",
    "🌤️ What's the weather in Tokyo?",
    "💱 Convert 1000 USD to EUR",
    "🎒 What should I pack for Southeast Asia?",
  ];

    return (
      <div className="flex flex-col h-screen max-w-5xl mx-auto">
        {/* Header */}
        <header className="border-b border-gray-700 p-4 bg-gray-900">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-linear-to-r from-accent-blue to-accent-purple bg-clip-text text-transparent">
                🌍 HodoBot
              </h1>
              <p className="text-sm text-gray-400 mt-1">
                Your intelligent travel companion
              </p>
            </div>
            <button
              onClick={clearChat}
              disabled={messages.length === 0}
              className="px-4 py-2 rounded-lg text-sm bg-gray-800 hover:bg-dark-border transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Clear Chat
            </button>
          </div>
        </header>

        {/* Messages Area */}
        <main className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
              <div className="space-y-2">
                <h2 className="text-2xl font-semibold">
                  👋 Welcome to HodoBot!
                </h2>
                <p className="text-gray-400 max-w-md">
                  I can help you with travel planning, real-time weather,
                  currency conversion, and more.
                </p>
              </div>

              <div className="w-full max-w-md space-y-2">
                <p className="text-sm text-gray-400 font-medium">
                  Try asking:
                </p>
                {exampleQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() =>
                      setInput(question.split(" ").slice(1).join(" "))
                    }
                    className="w-full text-left p-3 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-700 transition-all hover:border-accent-blue/50 text-sm"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 ${
                  msg.role === "user"
                    ? "bg-accent-blue text-white"
                    : "bg-gray-900 border border-gray-700"
                }`}
              >
                {/* Avatar */}
                <div className="flex items-start gap-3">
                  <div
                    className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-lg ${
                      msg.role === "user"
                        ? "bg-white/20"
                        : "bg-accent-purple/20"
                    }`}
                  >
                    {msg.role === "user" ? "👤" : "🤖"}
                  </div>

                  <div className="flex-1 min-w-0">
                    {/* Message Content with Markdown */}
                    <ReactMarkdown>
                      {msg.content}
                    </ReactMarkdown>

                    {/* Sources */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-700 space-y-1">
                        <p className="text-xs font-semibold text-gray-400 flex items-center gap-1">
                          📚 Sources
                        </p>
                        <div className="space-y-1">
                          {msg.sources.map((source, i) => (
                            <div
                              key={i}
                              className="text-xs bg-gray-800 p-2 rounded border border-gray-700"
                            >
                              <span className="text-accent-blue font-mono">
                                {source.file}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-900 border border-gray-700 rounded-2xl p-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-accent-purple/20 flex items-center justify-center">
                    🤖
                  </div>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-accent-blue rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-accent-blue rounded-full animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 bg-accent-blue rounded-full animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </main>

        {/* Input Area */}
        <footer className="border-t border-gray-700 p-4 bg-gray-900">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) =>
                  e.key === "Enter" && !e.shiftKey && sendMessage()
                }
                placeholder="Ask me anything about travel..."
                className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent placeholder:text-gray-400 transition-all"
                disabled={loading}
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="bg-accent-blue hover:bg-accent-blue-dark text-white px-6 py-3 rounded-xl font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-accent-blue flex items-center gap-2"
              >
                <span>Send</span>
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </button>
            </div>
            <p className="text-xs text-gray-400 text-center mt-2">
              Press Enter to send • Shift + Enter for new line
            </p>
          </div>
        </footer>
      </div>
    );
}