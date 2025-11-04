'use client'

import { useState } from 'react'
import { Mic, MicOff } from 'lucide-react'
import { sendMessage } from '@/lib/api'

export default function VoiceButton() {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [response, setResponse] = useState('')
  const [error, setError] = useState('')

  const startListening = () => {
    setError('')
    setTranscript('')
    setResponse('')

    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Voice recognition is not supported in your browser. Please try Safari on iOS.')
      return
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'en-US'

    recognition.onstart = () => {
      setIsListening(true)
      setTranscript('Listening...')
      // Vibrate on start (if supported)
      if ('vibrate' in navigator) {
        navigator.vibrate(50)
      }
    }

    recognition.onresult = async (event: any) => {
      const transcript = event.results[0][0].transcript
      setTranscript(transcript)
      setIsListening(false)

      // Vibrate on recognition
      if ('vibrate' in navigator) {
        navigator.vibrate([50, 100, 50])
      }

      try {
        // Send to AI
        const result = await sendMessage(transcript, [])
        setResponse(result.response)

        // Speak the response
        if ('speechSynthesis' in window) {
          // Cancel any ongoing speech
          window.speechSynthesis.cancel()

          const utterance = new SpeechSynthesisUtterance(result.response)
          utterance.rate = 0.85 // Slower for elderly users
          utterance.pitch = 1.0
          utterance.volume = 1.0
          utterance.lang = 'en-US'

          // Use more natural voice if available
          const voices = window.speechSynthesis.getVoices()
          const preferredVoice = voices.find(voice =>
            voice.lang === 'en-US' && voice.name.includes('Samantha')
          ) || voices.find(voice => voice.lang === 'en-US')

          if (preferredVoice) {
            utterance.voice = preferredVoice
          }

          window.speechSynthesis.speak(utterance)
        }
      } catch (error) {
        console.error('Error:', error)
        setError('Sorry, I had trouble with that. Can you try again?')
        if ('vibrate' in navigator) {
          navigator.vibrate([100, 100, 100]) // Error vibration
        }
      }
    }

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error)
      setIsListening(false)

      if (event.error === 'no-speech') {
        setError('I didn\'t hear anything. Please try again.')
      } else if (event.error === 'not-allowed') {
        setError('Please allow microphone access in your browser settings.')
      } else {
        setError('I had trouble hearing you. Please try again.')
      }

      if ('vibrate' in navigator) {
        navigator.vibrate([100, 100, 100])
      }
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognition.start()
  }

  return (
    <div className="flex flex-col items-center space-y-4 md:space-y-6">
      {/* Voice Button - Extra large for easy tapping */}
      <button
        onClick={startListening}
        disabled={isListening}
        className={`w-36 h-36 md:w-40 md:h-40 rounded-full flex items-center justify-center text-white text-5xl md:text-6xl transition-all shadow-2xl active:scale-95 ${
          isListening
            ? 'bg-red-500 animate-pulse'
            : 'bg-gradient-to-br from-purple-600 to-indigo-600'
        }`}
        style={{ touchAction: 'manipulation' }}
      >
        {isListening ? <MicOff size={64} /> : <Mic size={64} />}
      </button>

      {/* Instructions - Large text */}
      <div className="text-center">
        <p className="text-2xl md:text-3xl font-semibold text-gray-700">
          {isListening ? 'Listening...' : 'Tap to speak'}
        </p>
        <p className="text-lg md:text-xl text-gray-500 mt-2">
          {isListening ? 'Say your question' : 'Ask me anything!'}
        </p>
      </div>

      {/* Transcript - Large text for readability */}
      {transcript && transcript !== 'Listening...' && (
        <div className="w-full bg-purple-50 rounded-2xl p-4 md:p-6">
          <p className="text-base md:text-lg text-gray-600 mb-2 font-semibold">You said:</p>
          <p className="text-xl md:text-2xl text-gray-900 leading-relaxed">{transcript}</p>
        </div>
      )}

      {/* Response - Large text with high contrast */}
      {response && (
        <div className="w-full bg-green-50 border-2 border-green-200 rounded-2xl p-4 md:p-6">
          <p className="text-base md:text-lg text-gray-600 mb-2 font-semibold">My response:</p>
          <p className="text-xl md:text-2xl text-gray-900 leading-relaxed">{response}</p>
        </div>
      )}

      {/* Error - High contrast, large text */}
      {error && (
        <div className="w-full bg-red-50 border-2 border-red-200 rounded-2xl p-4 md:p-6">
          <p className="text-lg md:text-xl text-red-700 leading-relaxed">{error}</p>
        </div>
      )}
    </div>
  )
}
