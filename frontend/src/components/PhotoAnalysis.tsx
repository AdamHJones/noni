'use client'

import { useState } from 'react'
import { X, AlertTriangle, CheckCircle, Info } from 'lucide-react'

interface PhotoAnalysisProps {
  imageData: string
  analysisType: string
  result: {
    success: boolean
    analysis: string
    warnings?: string[]
    suggestions?: string[]
    extractedData?: any
  }
  onClose: () => void
}

export default function PhotoAnalysis({ imageData, analysisType, result, onClose }: PhotoAnalysisProps) {
  const getTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      prescription: 'Prescription',
      medication: 'Medication Label',
      doctor_note: 'Doctor Note',
      recipe: 'Recipe',
      food_label: 'Food Label',
      nutrition: 'Nutrition Info',
      sign: 'Sign/Text',
    }
    return labels[type] || type
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-3xl">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{getTypeLabel(analysisType)}</h2>
              <p className="text-base text-gray-600 mt-1">Analysis Results</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 p-2"
            >
              <X size={28} />
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Photo Preview */}
          <div className="rounded-2xl overflow-hidden border-2 border-gray-200">
            <img
              src={imageData}
              alt="Captured"
              className="w-full h-auto"
            />
          </div>

          {/* Main Analysis */}
          <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-5">
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Info size={20} className="text-blue-600" />
              What I Found
            </h3>
            <p className="text-lg text-gray-900 leading-relaxed whitespace-pre-line">
              {result.analysis}
            </p>
          </div>

          {/* Warnings */}
          {result.warnings && result.warnings.length > 0 && (
            <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-5">
              <h3 className="font-semibold text-red-900 mb-3 flex items-center gap-2">
                <AlertTriangle size={20} className="text-red-600" />
                ⚠️ Important Warnings
              </h3>
              <ul className="space-y-2">
                {result.warnings.map((warning, idx) => (
                  <li key={idx} className="text-base text-red-900 leading-relaxed">
                    • {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Suggestions */}
          {result.suggestions && result.suggestions.length > 0 && (
            <div className="bg-green-50 border-2 border-green-200 rounded-2xl p-5">
              <h3 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
                <CheckCircle size={20} className="text-green-600" />
                Recommendations
              </h3>
              <ul className="space-y-2">
                {result.suggestions.map((suggestion, idx) => (
                  <li key={idx} className="text-base text-green-900 leading-relaxed">
                    • {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Extracted Data (if medication) */}
          {result.extractedData && (
            <div className="bg-purple-50 border-2 border-purple-200 rounded-2xl p-5">
              <h3 className="font-semibold text-purple-900 mb-3">Extracted Information</h3>
              <div className="space-y-2 text-base">
                {Object.entries(result.extractedData).map(([key, value]) => (
                  <div key={key} className="flex gap-2">
                    <span className="font-semibold capitalize">{key}:</span>
                    <span>{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="space-y-3">
            <button
              onClick={onClose}
              className="w-full bg-purple-600 text-white py-4 rounded-2xl text-lg font-semibold hover:bg-purple-700 transition-colors"
            >
              Done
            </button>
            <button
              onClick={() => {
                // TODO: Save to database
                alert('Saving this information...')
              }}
              className="w-full bg-gray-200 text-gray-700 py-4 rounded-2xl text-lg font-semibold hover:bg-gray-300 transition-colors"
            >
              Save This Information
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
