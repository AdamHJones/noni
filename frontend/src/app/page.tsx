'use client'

import { useState, useEffect } from 'react'
import ChatInterface from '@/components/ChatInterface'
import VoiceButton from '@/components/VoiceButton'
import QuickActions from '@/components/QuickActions'
import InstallPrompt from '@/components/InstallPrompt'
import CameraCapture from '@/components/CameraCapture'
import PhotoAnalysis from '@/components/PhotoAnalysis'
import LocationTracker from '@/components/LocationTracker'
import { Camera, MapPin } from 'lucide-react'
import { analyzeImage } from '@/lib/api'

export default function Home() {
  const [mode, setMode] = useState<'voice' | 'chat'>('voice')
  const [showInstallPrompt, setShowInstallPrompt] = useState(false)
  const [showCamera, setShowCamera] = useState(false)
  const [showLocation, setShowLocation] = useState(false)
  const [photoResult, setPhotoResult] = useState<any>(null)
  const [analyzing, setAnalyzing] = useState(false)

  useEffect(() => {
    // Check if running as installed PWA
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches
    const isIOSStandalone = (window.navigator as any).standalone === true

    // Show install prompt if not installed
    if (!isStandalone && !isIOSStandalone) {
      // Wait 5 seconds before showing prompt
      const timer = setTimeout(() => setShowInstallPrompt(true), 5000)
      return () => clearTimeout(timer)
    }
  }, [])

  const handlePhotoCapture = async (imageData: string, analysisType: string) => {
    setShowCamera(false)
    setAnalyzing(true)

    try {
      const result = await analyzeImage(imageData, analysisType)
      setPhotoResult({
        imageData,
        analysisType,
        result,
      })
    } catch (error) {
      console.error('Error analyzing photo:', error)
      alert('Failed to analyze photo. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-500 to-indigo-600 safe-area-inset">
      <div className="h-screen flex flex-col">
        {/* Header - Fixed at top */}
        <div className="flex-shrink-0 text-center pt-safe px-4 py-6 bg-gradient-to-br from-purple-500 to-indigo-600">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-1">
            Care Companion
          </h1>
          <p className="text-lg md:text-xl text-purple-100">
            I'm here to help
          </p>
        </div>

        {/* Mode Toggle - Fixed below header */}
        <div className="flex-shrink-0 flex justify-center gap-3 px-4 pb-4 bg-gradient-to-br from-purple-500 to-indigo-600">
          <button
            onClick={() => setMode('voice')}
            className={`flex-1 max-w-[160px] px-6 py-4 rounded-2xl text-lg font-semibold transition-all active:scale-95 ${
              mode === 'voice'
                ? 'bg-white text-purple-600 shadow-lg'
                : 'bg-purple-400 text-white'
            }`}
          >
            🎤 Voice
          </button>
          <button
            onClick={() => setMode('chat')}
            className={`flex-1 max-w-[160px] px-6 py-4 rounded-2xl text-lg font-semibold transition-all active:scale-95 ${
              mode === 'chat'
                ? 'bg-white text-purple-600 shadow-lg'
                : 'bg-purple-400 text-white'
            }`}
          >
            💬 Type
          </button>
        </div>

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto px-4 pb-safe">
          <div className="bg-white rounded-3xl shadow-2xl p-4 md:p-6 mb-4">
            {mode === 'voice' ? (
              <div className="space-y-6">
                <VoiceButton />
                <QuickActions />
              </div>
            ) : (
              <ChatInterface />
            )}
          </div>

          {/* Camera & Location Buttons */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <button
              onClick={() => setShowCamera(true)}
              className="bg-white text-purple-600 px-6 py-5 rounded-2xl flex flex-col items-center gap-2 shadow-lg active:scale-95 transition-transform"
            >
              <Camera size={32} />
              <span className="text-base font-semibold">Scan Photo</span>
            </button>
            <button
              onClick={() => setShowLocation(!showLocation)}
              className={`px-6 py-5 rounded-2xl flex flex-col items-center gap-2 shadow-lg active:scale-95 transition-transform ${
                showLocation
                  ? 'bg-green-500 text-white'
                  : 'bg-white text-purple-600'
              }`}
            >
              <MapPin size={32} />
              <span className="text-base font-semibold">
                {showLocation ? 'Tracking On' : 'Share Location'}
              </span>
            </button>
          </div>

          {/* Location Tracker */}
          {showLocation && (
            <div className="mb-4">
              <LocationTracker userId={1} />
            </div>
          )}

          {/* Emergency Button */}
          <div className="text-center pb-4">
            <button
              className="w-full max-w-md bg-red-500 active:bg-red-600 text-white px-8 py-6 rounded-full text-xl font-bold shadow-lg active:scale-95 transition-transform"
              onClick={() => {
                // TODO: Implement emergency call
                if (confirm('Call emergency contact?')) {
                  alert('Calling caregiver...')
                }
              }}
            >
              🚨 Emergency Help
            </button>
          </div>
        </div>
      </div>

      {/* Install Prompt */}
      {showInstallPrompt && (
        <InstallPrompt onClose={() => setShowInstallPrompt(false)} />
      )}

      {/* Camera Interface */}
      {showCamera && (
        <CameraCapture
          onCapture={handlePhotoCapture}
          onClose={() => setShowCamera(false)}
        />
      )}

      {/* Photo Analysis Result */}
      {photoResult && (
        <PhotoAnalysis
          imageData={photoResult.imageData}
          analysisType={photoResult.analysisType}
          result={photoResult.result}
          onClose={() => setPhotoResult(null)}
        />
      )}

      {/* Analyzing Overlay */}
      {analyzing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
          <div className="bg-white rounded-3xl p-8 text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
            <p className="text-xl font-semibold text-gray-900">Analyzing photo...</p>
            <p className="text-gray-600 mt-2">This may take a moment</p>
          </div>
        </div>
      )}
    </main>
  )
}
