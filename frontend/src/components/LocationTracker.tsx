'use client'

import { useState, useEffect } from 'react'
import { MapPin, AlertCircle, Check } from 'lucide-react'

interface LocationTrackerProps {
  userId: number
  onLocationUpdate?: (lat: number, lng: number) => void
}

export default function LocationTracker({ userId, onLocationUpdate }: LocationTrackerProps) {
  const [tracking, setTracking] = useState(false)
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null)
  const [error, setError] = useState<string>('')
  const [lastUpdate, setLastUpdate] = useState<string>('')

  useEffect(() => {
    if (tracking) {
      startTracking()
    }

    return () => {
      if ('geolocation' in navigator && tracking) {
        // Clean up watch when component unmounts
      }
    }
  }, [tracking])

  const startTracking = () => {
    if (!('geolocation' in navigator)) {
      setError('Location tracking is not supported on this device')
      return
    }

    // Request permission and start watching
    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude

        setLocation({ lat, lng })
        setError('')
        setLastUpdate(new Date().toLocaleTimeString())

        // Send to backend
        sendLocationToBackend(lat, lng, position.coords.accuracy)

        // Callback
        if (onLocationUpdate) {
          onLocationUpdate(lat, lng)
        }
      },
      (err) => {
        setError(getErrorMessage(err))
        setTracking(false)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000, // Cache for 1 minute
      }
    )

    // Store watch ID to stop later
    return () => navigator.geolocation.clearWatch(watchId)
  }

  const sendLocationToBackend = async (lat: number, lng: number, accuracy?: number) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/location/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          latitude: lat,
          longitude: lng,
          accuracy: accuracy,
          timestamp: new Date().toISOString(),
        }),
      })

      if (!response.ok) {
        console.error('Failed to send location to backend')
      }
    } catch (error) {
      console.error('Error sending location:', error)
    }
  }

  const getErrorMessage = (error: GeolocationPositionError) => {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        return 'Location permission denied. Please allow location access in your settings.'
      case error.POSITION_UNAVAILABLE:
        return 'Location information is unavailable.'
      case error.TIMEOUT:
        return 'Location request timed out.'
      default:
        return 'An unknown error occurred.'
    }
  }

  const toggleTracking = () => {
    setTracking(!tracking)
  }

  return (
    <div className="bg-white rounded-2xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <MapPin size={24} className="text-purple-600" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Location Sharing</h3>
            <p className="text-sm text-gray-600">
              {tracking ? 'Active' : 'Off'}
            </p>
          </div>
        </div>

        <button
          onClick={toggleTracking}
          className={`px-5 py-3 rounded-xl font-semibold transition-colors ${
            tracking
              ? 'bg-green-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          {tracking ? 'On' : 'Off'}
        </button>
      </div>

      {tracking && location && (
        <div className="bg-green-50 border border-green-200 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Check size={16} className="text-green-600" />
            <span className="text-sm font-semibold text-green-900">Sharing Location</span>
          </div>
          <div className="text-sm text-gray-700 space-y-1">
            <div>Latitude: {location.lat.toFixed(6)}</div>
            <div>Longitude: {location.lng.toFixed(6)}</div>
            <div>Last updated: {lastUpdate}</div>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex items-start gap-2">
            <AlertCircle size={16} className="text-red-600 mt-0.5" />
            <p className="text-sm text-red-900">{error}</p>
          </div>
        </div>
      )}

      <div className="mt-4 p-3 bg-blue-50 rounded-xl">
        <p className="text-xs text-gray-700">
          📍 Your caregivers can see your location when sharing is on. This helps them know you're safe.
        </p>
      </div>
    </div>
  )
}
