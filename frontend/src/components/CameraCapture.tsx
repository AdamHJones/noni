'use client'

import { useState, useRef } from 'react'
import { Camera, X, Image as ImageIcon } from 'lucide-react'

interface CameraCaptureProps {
  onCapture: (imageData: string, analysisType: string) => void
  onClose: () => void
}

export default function CameraCapture({ onCapture, onClose }: CameraCaptureProps) {
  const [selectedType, setSelectedType] = useState<string>('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const analysisTypes = [
    { id: 'prescription', label: 'Prescription', icon: '💊', color: 'bg-blue-500' },
    { id: 'medication', label: 'Medication Label', icon: '🏷️', color: 'bg-green-500' },
    { id: 'doctor_note', label: 'Doctor Note', icon: '📋', color: 'bg-purple-500' },
    { id: 'recipe', label: 'Recipe', icon: '🍳', color: 'bg-orange-500' },
    { id: 'food_label', label: 'Food Label', icon: '🥫', color: 'bg-red-500' },
    { id: 'nutrition', label: 'Nutrition Info', icon: '📊', color: 'bg-teal-500' },
    { id: 'sign', label: 'Sign/Text', icon: '🔤', color: 'bg-indigo-500' },
  ]

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file || !selectedType) return

    const reader = new FileReader()
    reader.onloadend = () => {
      const imageData = reader.result as string
      onCapture(imageData, selectedType)
    }
    reader.readAsDataURL(file)
  }

  const triggerCamera = (type: string) => {
    setSelectedType(type)
    // Slight delay to ensure state is set
    setTimeout(() => {
      fileInputRef.current?.click()
    }, 100)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Take a Photo</h2>
            <p className="text-base text-gray-600 mt-1">What would you like to scan?</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-2"
          >
            <X size={28} />
          </button>
        </div>

        {/* Analysis Type Selection */}
        <div className="grid grid-cols-1 gap-3">
          {analysisTypes.map((type) => (
            <button
              key={type.id}
              onClick={() => triggerCamera(type.id)}
              className={`${type.color} text-white rounded-2xl p-5 flex items-center gap-4 hover:opacity-90 transition-opacity shadow-lg active:scale-95`}
              style={{ touchAction: 'manipulation' }}
            >
              <span className="text-3xl">{type.icon}</span>
              <div className="text-left flex-1">
                <div className="text-xl font-semibold">{type.label}</div>
                <div className="text-sm opacity-90">
                  {type.id === 'prescription' && 'Read prescription details'}
                  {type.id === 'medication' && 'Read medication bottle'}
                  {type.id === 'doctor_note' && 'Read doctor notes'}
                  {type.id === 'recipe' && 'Read recipe instructions'}
                  {type.id === 'food_label' && 'Read food ingredients'}
                  {type.id === 'nutrition' && 'Read nutrition facts'}
                  {type.id === 'sign' && 'Read any text'}
                </div>
              </div>
              <Camera size={24} />
            </button>
          ))}
        </div>

        {/* Hidden file input for camera */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileSelect}
          className="hidden"
        />

        {/* Instructions */}
        <div className="mt-6 p-4 bg-blue-50 rounded-2xl">
          <h3 className="font-semibold text-gray-900 mb-2">📸 Tips for Best Results</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• Make sure text is clear and readable</li>
            <li>• Use good lighting</li>
            <li>• Hold camera steady</li>
            <li>• Get close enough to read the text</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
