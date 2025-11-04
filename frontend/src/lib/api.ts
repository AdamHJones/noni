const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const USER_ID = parseInt(process.env.NEXT_PUBLIC_USER_ID || '1')

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatResponse {
  response: string
  suggested_action?: any
  needs_confirmation: boolean
  context_used?: any
}

interface VisionAnalysisResponse {
  success: boolean
  analysis: string
  warnings?: string[]
  suggestions?: string[]
  extracted_data?: any
}

export async function sendMessage(
  message: string,
  conversationHistory: Message[]
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_id: USER_ID,
        conversation_history: conversationHistory,
      }),
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error calling API:', error)
    throw error
  }
}

export async function analyzeImage(
  imageData: string,
  analysisType: string
): Promise<VisionAnalysisResponse> {
  try {
    const response = await fetch(`${API_URL}/api/vision/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_data: imageData,
        analysis_type: analysisType,
        user_id: USER_ID,
      }),
    })

    if (!response.ok) {
      throw new Error(`Vision API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error analyzing image:', error)
    throw error
  }
}

export async function checkMedicationInteractions(medication: string) {
  try {
    const response = await fetch(
      `${API_URL}/api/vision/check-interactions?medication=${encodeURIComponent(medication)}&user_id=${USER_ID}`,
      {
        method: 'POST',
      }
    )
    if (!response.ok) throw new Error('Failed to check interactions')
    return await response.json()
  } catch (error) {
    console.error('Error checking medication interactions:', error)
    throw error
  }
}

export async function getMedications() {
  try {
    const response = await fetch(`${API_URL}/api/medications/${USER_ID}`)
    if (!response.ok) throw new Error('Failed to fetch medications')
    return await response.json()
  } catch (error) {
    console.error('Error fetching medications:', error)
    throw error
  }
}

export async function getCalendar() {
  try {
    const response = await fetch(`${API_URL}/api/calendar/today/${USER_ID}`)
    if (!response.ok) throw new Error('Failed to fetch calendar')
    return await response.json()
  } catch (error) {
    console.error('Error fetching calendar:', error)
    throw error
  }
}

export async function getBalance() {
  try {
    const response = await fetch(`${API_URL}/api/banking/balance/${USER_ID}`)
    if (!response.ok) throw new Error('Failed to fetch balance')
    return await response.json()
  } catch (error) {
    console.error('Error fetching balance:', error)
    throw error
  }
}

export async function updateLocation(lat: number, lng: number, accuracy?: number) {
  try {
    const response = await fetch(`${API_URL}/api/location/update`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: USER_ID,
        latitude: lat,
        longitude: lng,
        accuracy,
        timestamp: new Date().toISOString(),
      }),
    })
    if (!response.ok) throw new Error('Failed to update location')
    return await response.json()
  } catch (error) {
    console.error('Error updating location:', error)
    throw error
  }
}
