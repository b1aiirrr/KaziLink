-- Row Level Security Policies for KaziLink

-- Enable RLS on all tables
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_saved_opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

-- Opportunities: Public read, admin write
CREATE POLICY "Opportunities are viewable by everyone"
  ON opportunities FOR SELECT
  USING (true);

CREATE POLICY "Only admins can insert opportunities"
  ON opportunities FOR INSERT
  WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Only admins can update opportunities"
  ON opportunities FOR UPDATE
  USING (auth.jwt() ->> 'role' = 'service_role');

-- User Saved Opportunities: Users can manage their own
CREATE POLICY "Users can view their own saved opportunities"
  ON user_saved_opportunities FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can save opportunities"
  ON user_saved_opportunities FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can unsave opportunities"
  ON user_saved_opportunities FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update their saved opportunity notes"
  ON user_saved_opportunities FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Notification Preferences: Users manage their own
CREATE POLICY "Users can view their own notification preferences"
  ON notification_preferences FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own notification preferences"
  ON notification_preferences FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own notification preferences"
  ON notification_preferences FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- User Profiles: Users manage their own
CREATE POLICY "Users can view their own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own profile"
  ON user_profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Applications: Users manage their own
CREATE POLICY "Users can view their own applications"
  ON applications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own applications"
  ON applications FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own applications"
  ON applications FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own applications"
  ON applications FOR DELETE
  USING (auth.uid() = user_id);
