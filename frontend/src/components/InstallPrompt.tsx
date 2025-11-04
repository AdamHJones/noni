'use client'

import { X, Share, Plus } from 'lucide-react'

interface InstallPromptProps {
  onClose: () => void
}

export default function InstallPrompt({ onClose }: InstallPromptProps) {
  const isIOS = () => {
    if (typeof window === 'undefined') return false
    return /iPad|iPhone|iPod/.test(navigator.userAgent)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-end justify-center z-50 p-4">
      <div className="bg-white rounded-t-3xl max-w-lg w-full p-6 shadow-2xl animate-slide-up">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X size={24} />
        </button>

        <div className="text-center mb-6">
          <div className="text-5xl mb-4">📱</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Install Care Companion
          </h2>
          <p className="text-lg text-gray-600">
            Add this app to your home screen for easy access
          </p>
        </div>

        {isIOS() ? (
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <p className="text-base text-gray-900">
                    Tap the <strong>Share button</strong> <Share size={16} className="inline" /> at the bottom of Safari
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <div>
                  <p className="text-base text-gray-900">
                    Scroll down and tap <strong>"Add to Home Screen"</strong> <Plus size={16} className="inline" />
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <div>
                  <p className="text-base text-gray-900">
                    Tap <strong>"Add"</strong> in the top right
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-purple-50 rounded-2xl">
              <p className="text-sm text-gray-700 text-center">
                The app icon will appear on your home screen. Tap it to open Care Companion anytime!
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-base text-gray-600">
              To install this app, open it in Safari on your iPhone.
            </p>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full mt-6 bg-gray-200 text-gray-700 py-4 rounded-2xl text-lg font-semibold hover:bg-gray-300 transition-colors"
        >
          Maybe Later
        </button>
      </div>
    </div>
  )
}
