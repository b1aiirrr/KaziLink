export type OpportunityType = 'attachment' | 'internship' | 'job'
export type OpportunityStatus = 'active' | 'expired' | 'filled'

export interface Opportunity {
    id: string
    title: string
    company: string
    type: OpportunityType
    description: string | null
    requirements: string | null
    location: string | null
    salary_range: string | null
    application_deadline: string | null
    source_url: string
    source_platform: string | null
    status: OpportunityStatus
    scraped_at: string
    created_at: string
    updated_at: string
    experience_required: string | null
    education_level: string | null
    industry: string | null
    is_remote: boolean
}

export interface UserSavedOpportunity {
    user_id: string
    opportunity_id: string
    saved_at: string
    notes: string | null
}

export interface NotificationPreferences {
    user_id: string
    notify_attachments: boolean
    notify_internships: boolean
    notify_jobs: boolean
    preferred_locations: string[]
    preferred_industries: string[] | null
    notification_frequency: 'immediate' | 'daily' | 'weekly' | 'never'
    fcm_token: string | null
    fcm_updated_at: string | null
    created_at: string
    updated_at: string
}
