'use client'

import { useState, useRef, useEffect } from 'react'
import { sendMessage } from '@/lib/api'
import { Send } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! How can I help you today?',
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')

    // Add user message
    const newMessages = [...messages, { role: 'user' as const, content: userMessage }]
    setMessages(newMessages)
    setLoading(true)

    try {
      // Call backend API
      const response = await sendMessage(userMessage, newMessages)

      // Add assistant response
      setMessages([
        ...newMessages,
        { role: 'assistant', content: response.response },
      ])

      // Text-to-speech (optional)
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(response.response)
        utterance.rate = 0.9 // Slightly slower for clarity
        utterance.pitch = 1.0
        window.speechSynthesis.speak(utterance)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: "I'm sorry, I'm having trouble right now. Can you try again?",
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-280px)] md:h-[600px]">
      {/* Messages - Scrollable */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-4 px-2 hide-scrollbar">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[85%] rounded-3xl px-5 py-4 text-lg md:text-xl ${
                message.role === 'user'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
              style={{ wordBreak: 'break-word' }}
            >
              {message.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-3xl px-5 py-4">
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input - Fixed at bottom */}
      <div className="flex gap-2 items-end">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          rows={1}
          className="flex-1 px-5 py-4 text-lg md:text-xl border-2 border-gray-300 rounded-2xl focus:outline-none focus:border-purple-500 resize-none"
          style={{ fontSize: '16px' }} // Prevents iOS zoom
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="flex-shrink-0 w-14 h-14 bg-purple-600 text-white rounded-2xl flex items-center justify-center hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors active:scale-95"
          style={{ touchAction: 'manipulation' }}
        >
          <Send size={24} />
        </button>
      </div>
    </div>
  )
}
