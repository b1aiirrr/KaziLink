'use client'

import Link from 'next/link'
import { Opportunity } from '@/types/database'
import { Calendar, MapPin, Building2, ExternalLink, Bookmark } from 'lucide-react'

interface OpportunityCardProps {
    opportunity: Opportunity
    variant?: 'default' | 'compact'
}

const categoryBadges = {
    attachment: 'bg-blue-500/20 text-blue-400 ring-blue-500/30',
    internship: 'bg-green-500/20 text-green-400 ring-green-500/30',
    job: 'bg-orange-500/20 text-orange-400 ring-orange-500/30'
}

const categoryLabels = {
    attachment: 'Attachment',
    internship: 'Internship',
    job: 'Full-Time Job'
}

export default function OpportunityCard({ opportunity, variant = 'default' }: OpportunityCardProps) {
    const isExpiringSoon = opportunity.application_deadline
        ? new Date(opportunity.application_deadline).getTime() - Date.now() < 7 * 24 * 60 * 60 * 1000
        : false

    return (
        <div className="group relative bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 hover:border-slate-600 hover:shadow-xl hover:shadow-slate-900/50 transition-all duration-300">
            {/* Category badge */}
            <div className="flex items-center justify-between mb-4">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ring-1 ${categoryBadges[opportunity.type]}`}>
                    {categoryLabels[opportunity.type]}
                </span>

                {/* Bookmark button */}
                <button className="p-2 rounded-full hover:bg-slate-700/50 transition-colors">
                    <Bookmark className="w-5 h-5 text-slate-400 hover:text-orange-500 transition-colors" />
                </button>
            </div>

            {/* Title and company */}
            <div className="mb-4">
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-orange-400 transition-colors line-clamp-2">
                    {opportunity.title}
                </h3>
                <div className="flex items-center text-slate-300 mb-2">
                    <Building2 className="w-4 h-4 mr-2" />
                    <span className="font-medium">{opportunity.company}</span>
                </div>
            </div>

            {/* Description */}
            {opportunity.description && variant === 'default' && (
                <p className="text-slate-400 text-sm mb-4 line-clamp-3">
                    {opportunity.description}
                </p>
            )}

            {/* Meta information */}
            <div className="flex flex-wrap gap-3 mb-4 text-sm text-slate-400">
                {opportunity.location && (
                    <div className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        <span>{opportunity.location}</span>
                    </div>
                )}

                {opportunity.application_deadline && (
                    <div className={`flex items-center ${isExpiringSoon ? 'text-orange-400 font-semibold' : ''}`}>
                        <Calendar className="w-4 h-4 mr-1" />
                        <span>
                            {isExpiringSoon && '⚡ '}
                            Deadline: {new Date(opportunity.application_deadline).toLocaleDateString()}
                        </span>
                    </div>
                )}
            </div>

            {/* Source platform badge */}
            {opportunity.source_platform && (
                <div className="mb-4">
                    <span className="inline-block px-2 py-1 bg-slate-700/50 text-slate-400 text-xs rounded">
                        {opportunity.source_platform}
                    </span>
                </div>
            )}

            {/* Action button */}
            <Link
                href={opportunity.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center w-full px-4 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-300 group-hover:shadow-lg group-hover:shadow-orange-500/50"
            >
                View & Apply
                <ExternalLink className="w-4 h-4 ml-2" />
            </Link>
        </div>
    )
}
