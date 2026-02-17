'use client'

import { useState } from 'react'
import { OpportunityType } from '@/types/database'

interface SectionSwitcherProps {
    activeSection: OpportunityType
    onSwitch: (section: OpportunityType) => void
}

const sections = [
    {
        type: 'attachment' as OpportunityType,
        label: 'Attachments',
        icon: '📎',
        description: 'For current students',
        color: 'from-blue-500 to-blue-600'
    },
    {
        type: 'internship' as OpportunityType,
        label: 'Internships',
        icon: '🎓',
        description: 'For fresh graduates',
        color: 'from-green-500 to-green-600'
    },
    {
        type: 'job' as OpportunityType,
        label: 'Jobs',
        icon: '💼',
        description: 'For professionals',
        color: 'from-orange-500 to-orange-600'
    }
]

export default function SectionSwitcher({ activeSection, onSwitch }: SectionSwitcherProps) {
    return (
        <div className="w-full max-w-4xl mx-auto px-4 py-8">
            {/* Mobile: Segmented Control */}
            <div className="lg:hidden bg-slate-800 p-1.5 rounded-2xl shadow-2xl">
                <div className="grid grid-cols-3 gap-1">
                    {sections.map((section) => (
                        <button
                            key={section.type}
                            onClick={() => onSwitch(section.type)}
                            className={`
                relative px-4 py-3 rounded-xl font-semibold text-sm transition-all duration-300
                ${activeSection === section.type
                                    ? 'bg-gradient-to-r ' + section.color + ' text-white shadow-lg scale-105'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
                                }
              `}
                        >
                            <span className="block text-xl mb-1">{section.icon}</span>
                            <span className="block text-xs">{section.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Desktop: Card Selection */}
            <div className="hidden lg:grid grid-cols-3 gap-6">
                {sections.map((section) => (
                    <button
                        key={section.type}
                        onClick={() => onSwitch(section.type)}
                        className={`
              group relative overflow-hidden rounded-2xl p-8 transition-all duration-500
              ${activeSection === section.type
                                ? 'ring-4 ring-offset-4 ring-offset-slate-950 shadow-2xl scale-105'
                                : 'hover:scale-102 hover:shadow-xl'
                            }
            `}
                        style={{
                            background: activeSection === section.type
                                ? `linear-gradient(135deg, ${section.type === 'attachment' ? '#3B82F6, #2563EB' : section.type === 'internship' ? '#10B981, #059669' : '#FF7675, #E74C3C'})`
                                : '#1E293B'
                        }}
                    >
                        {/* Background gradient overlay */}
                        <div className={`
              absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-500
              ${section.color}
            `} />

                        <div className="relative z-10 text-center">
                            <div className="text-5xl mb-4 transform group-hover:scale-110 transition-transform duration-300">
                                {section.icon}
                            </div>
                            <h3 className={`
                text-2xl font-bold mb-2 transition-colors duration-300
                ${activeSection === section.type ? 'text-white' : 'text-white group-hover:text-white'}
              `}>
                                {section.label}
                            </h3>
                            <p className={`
                text-sm transition-colors duration-300
                ${activeSection === section.type ? 'text-white/90' : 'text-slate-400 group-hover:text-white/80'}
              `}>
                                {section.description}
                            </p>
                        </div>

                        {/* Active indicator */}
                        {activeSection === section.type && (
                            <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2">
                                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                            </div>
                        )}
                    </button>
                ))}
            </div>

            {/* Active section description */}
            <div className="mt-8 text-center">
                <p className="text-slate-300 text-lg">
                    {sections.find(s => s.type === activeSection)?.description}
                </p>
            </div>
        </div>
    )
}
