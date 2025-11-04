'use client'

import { Calendar, DollarSign, Pill, Mail } from 'lucide-react'

export default function QuickActions() {
  const actions = [
    {
      icon: Calendar,
      label: "What's on my calendar?",
      color: 'bg-blue-500',
      query: "What's on my calendar today?",
    },
    {
      icon: DollarSign,
      label: 'Do I have enough money?',
      color: 'bg-green-500',
      query: 'Do I have enough money?',
    },
    {
      icon: Pill,
      label: 'What pills should I take?',
      color: 'bg-purple-500',
      query: 'What pills should I take right now?',
    },
    {
      icon: Mail,
      label: 'Do I have any messages?',
      color: 'bg-orange-500',
      query: 'Do I have any messages?',
    },
  ]

  const handleAction = (label: string, query: string) => {
    // TODO: Implement quick action handler
    // For now, just show coming soon
    console.log('Quick action:', query)
    alert(`This feature is coming soon!\n\nYou asked: "${query}"`)
  }

  return (
    <div className="mt-6">
      <h2 className="text-xl md:text-2xl font-semibold text-gray-700 mb-4 text-center">
        Quick Questions
      </h2>
      <div className="grid grid-cols-1 gap-3">
        {actions.map((action, index) => {
          const Icon = action.icon
          return (
            <button
              key={index}
              onClick={() => handleAction(action.label, action.query)}
              className={`${action.color} text-white rounded-2xl p-5 flex items-center gap-4 active:opacity-80 transition-opacity shadow-lg`}
              style={{ touchAction: 'manipulation' }}
            >
              <Icon size={32} className="flex-shrink-0" />
              <span className="text-lg md:text-xl font-semibold text-left">
                {action.label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
