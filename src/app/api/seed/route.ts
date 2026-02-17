import { createAdminClient } from '@/lib/supabase/admin'
import { NextResponse } from 'next/server'

export async function GET() {
    const supabase = createAdminClient()

    // 1. Seed Opportunities
    const dummyJobs = [
        {
            title: 'Junior Software Engineer',
            company: 'Tech Solutions Ltd',
            location: 'Nairobi',
            type: 'job',
            description: 'We are looking for a junior developer with React and Node.js skills.',
            url: 'https://example.com/job1',
            status: 'active',
            source: 'Internal'
        },
        {
            title: 'Marketing Intern',
            company: 'Growth Agency',
            location: 'Remote',
            type: 'internship',
            description: 'Join our marketing team and learn SEO, content marketing, and social media strategies.',
            url: 'https://example.com/intern1',
            status: 'active',
            source: 'Internal'
        },
        {
            title: 'IT Attachment',
            company: 'Government Ministry',
            location: 'Mombasa',
            type: 'attachment',
            description: 'attachment opportunity for 3rd year students. Must have a letter from the university.',
            url: 'https://example.com/attach1',
            status: 'active',
            source: 'Internal'
        },
        {
            title: 'Data Analyst',
            company: 'FinTech Corp',
            location: 'Nairobi',
            type: 'job',
            description: 'Analyze financial data and generate reports. SQL and Python required.',
            url: 'https://example.com/job2',
            status: 'active',
            source: 'Internal'
        },
        {
            title: 'Graphic Design Intern',
            company: 'Creative Studio',
            location: 'Kisumu',
            type: 'internship',
            description: 'Create visuals for social media and marketing campaigns. Photoshop and Illustrator skills.',
            url: 'https://example.com/intern2',
            status: 'active',
            source: 'Internal'
        }
    ]

    const { error: insertError } = await supabase.from('opportunities').insert(dummyJobs)

    if (insertError) {
        return NextResponse.json({ error: `Insert Error: ${insertError.message}` }, { status: 500 })
    }

    // 2. Create Test User
    const { data: user, error: userError } = await supabase.auth.admin.createUser({
        email: 'test@kazilink.com',
        password: 'password123',
        email_confirm: true
    })

    if (userError) {
        console.error('User creation error (might already exist):', userError.message)
    }

    return NextResponse.json({
        message: 'Seeded successfully',
        testUser: {
            email: 'test@kazilink.com',
            password: 'password123'
        }
    })
}
