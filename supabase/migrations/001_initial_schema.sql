-- KaziLink Database Schema
-- Version: 1.0
-- Description: Initial schema for opportunities, user preferences, and saved items

-- Create custom types
CREATE TYPE opportunity_type AS ENUM ('attachment', 'internship', 'job');
CREATE TYPE opportunity_status AS ENUM ('active', 'expired', 'filled');

-- Main opportunities table
CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  type opportunity_type NOT NULL,
  description TEXT,
  requirements TEXT,
  location TEXT,
  salary_range TEXT,
  application_deadline TIMESTAMP,
  source_url TEXT UNIQUE NOT NULL,
  source_platform TEXT CHECK (source_platform IN ('fuzu', 'myjobmag', 'brightermonday')),
  status opportunity_status DEFAULT 'active',
  scraped_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Additional metadata
  experience_required TEXT,
  education_level TEXT,
  industry TEXT,
  company_size TEXT,
  is_remote BOOLEAN DEFAULT false,
  
  -- For search optimization
  search_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, '') || ' ' || coalesce(company, ''))
  ) STORED
);

-- User saved opportunities (bookmarks)
CREATE TABLE user_saved_opportunities (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  opportunity_id UUID REFERENCES opportunities(id) ON DELETE CASCADE,
  saved_at TIMESTAMP DEFAULT NOW(),
  notes TEXT,
  PRIMARY KEY (user_id, opportunity_id)
);

-- User notification preferences
CREATE TABLE notification_preferences (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Category toggles
  notify_attachments BOOLEAN DEFAULT true,
  notify_internships BOOLEAN DEFAULT true,
  notify_jobs BOOLEAN DEFAULT true,
  
  -- Location preferences
  preferred_locations TEXT[] DEFAULT ARRAY['Nairobi'],
  
  -- Industry preferences
  preferred_industries TEXT[],
  
  -- Notification frequency
  notification_frequency TEXT DEFAULT 'immediate' CHECK (notification_frequency IN ('immediate', 'daily', 'weekly', 'never')),
  
  -- Push notification tokens
  fcm_token TEXT,
  fcm_updated_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- User profiles (extended auth.users)
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  phone_number TEXT,
  education_level TEXT,
  institution TEXT,
  graduation_year INTEGER,
  field_of_study TEXT,
  resume_url TEXT,
  linkedin_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Application tracking
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  opportunity_id UUID REFERENCES opportunities(id) ON DELETE CASCADE,
  applied_at TIMESTAMP DEFAULT NOW(),
  status TEXT DEFAULT 'applied' CHECK (status IN ('applied', 'shortlisted', 'interviewed', 'offered', 'rejected', 'withdrawn')),
  notes TEXT,
  UNIQUE(user_id, opportunity_id)
);

-- Indexes for performance
CREATE INDEX idx_opportunities_type ON opportunities(type);
CREATE INDEX idx_opportunities_location ON opportunities(location);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_created ON opportunities(created_at DESC);
CREATE INDEX idx_opportunities_deadline ON opportunities(application_deadline);
CREATE INDEX idx_opportunities_search ON opportunities USING GIN(search_vector);
CREATE INDEX idx_opportunities_source ON opportunities(source_platform, scraped_at DESC);

CREATE INDEX idx_user_saved_user ON user_saved_opportunities(user_id);
CREATE INDEX idx_applications_user ON applications(user_id, applied_at DESC);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_preferences_updated_at BEFORE UPDATE ON notification_preferences
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to automatically mark expired opportunities
CREATE OR REPLACE FUNCTION mark_expired_opportunities()
RETURNS void AS $$
BEGIN
  UPDATE opportunities
  SET status = 'expired'
  WHERE status = 'active'
    AND application_deadline < NOW();
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE opportunities IS 'Main table storing all job opportunities from various sources';
COMMENT ON COLUMN opportunities.type IS 'Category: attachment (student), internship (graduate), or job (professional)';
COMMENT ON COLUMN opportunities.search_vector IS 'Full-text search index for title, description, and company';
