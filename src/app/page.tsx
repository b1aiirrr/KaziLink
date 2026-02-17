'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import { Opportunity, OpportunityType } from '@/types/database'
import SectionSwitcher from '@/components/SectionSwitcher'
import OpportunityCard from '@/components/OpportunityCard'
import { Search, MapPin, TrendingUp } from 'lucide-react'

export default function HomePage() {
  const [activeSection, setActiveSection] = useState<OpportunityType>('attachment')
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [locationFilter, setLocationFilter] = useState('')

  const supabase = createClient()

  useEffect(() => {
    loadOpportunities()
  }, [activeSection])

  async function loadOpportunities() {
    setLoading(true)
    try {
      let query = supabase
        .from('opportunities')
        .select('*')
        .eq('type', activeSection)
        .eq('status', 'active')
        .order('created_at', { ascending: false })
        .limit(12)

      if (searchQuery) {
        query = query.ilike('title', `%${searchQuery}%`)
      }

      if (locationFilter) {
        query = query.ilike('location', `%${locationFilter}%`)
      }

      const { data, error } = await query

      if (error) throw error
      setOpportunities(data || [])
    } catch (error) {
      console.error('Error loading opportunities:', error)
      setOpportunities([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <img src="/logo.png" alt="KaziLink" className="h-10 w-auto" />
              <div>
                <h1 className="text-2xl font-bold text-white">
                  KaziLink
                </h1>
                <p className="text-orange-400 text-xs font-medium">Your ladder to success</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <Link href="/login">
                <button className="px-4 py-2 text-white hover:text-orange-400 transition-colors">
                  Sign In
                </button>
              </Link>
              <Link href="/signup">
                <button className="px-6 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all">
                  Get Started
                </button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero section */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            From Student to{' '}
            <span className="bg-gradient-to-r from-orange-400 to-orange-500 bg-clip-text text-transparent">
              Professional
            </span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 mb-4 max-w-2xl mx-auto leading-relaxed">
            Discover attachments, internships, and jobs curated for Kenyan students and graduates.
          </p>
          <div className="flex items-center justify-center space-x-2 text-slate-400 text-sm">
            <TrendingUp className="w-4 h-4" />
            <span>Updated daily from top Kenyan job boards</span>
          </div>
        </div>
      </section>

      {/* Section Switcher */}
      <SectionSwitcher activeSection={activeSection} onSwitch={setActiveSection} />

      {/* Search and filters */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search opportunities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && loadOpportunities()}
              className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          <div className="md:w-64 relative">
            <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <select
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none"
            >
              <option value="">All Locations</option>
              <option value="Nairobi">Nairobi</option>
              <option value="Mombasa">Mombasa</option>
              <option value="Kisumu">Kisumu</option>
              <option value="Nakuru">Nakuru</option>
              <option value="Eldoret">Eldoret</option>
            </select>
          </div>

          <button
            onClick={loadOpportunities}
            className="px-8 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all"
          >
            Search
          </button>
        </div>
      </section>

      {/* Opportunities grid */}
      <section className="max-w-7xl mx-auto px-4 py-8 pb-20">
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent"></div>
            <p className="text-slate-400 mt-4">Loading opportunities...</p>
          </div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold text-white mb-2">No opportunities found</h3>
            <p className="text-slate-400">Try adjusting your search or filters</p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-white">
                {opportunities.length} {activeSection === 'attachment' ? 'Attachments' : activeSection === 'internship' ? 'Internships' : 'Jobs'} Available
              </h3>
              <select className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-orange-500">
                <option>Most Recent</option>
                <option>Deadline Soon</option>
                <option>Company A-Z</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {opportunities.map((opportunity) => (
                <OpportunityCard key={opportunity.id} opportunity={opportunity} />
              ))}
            </div>
          </>
        )}
      </section>
    </div>
  )
}
