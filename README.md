# KaziLink - Professional Portal

A comprehensive platform connecting Kenyan students and graduates with attachments, internships, and entry-level jobs.

## 🎯 Project Overview

KaziLink is a multi-platform professional portal that automatically scrapes and categorizes job opportunities from major Kenyan job boards, making it easier for students, graduates, and early-career professionals to find relevant opportunities.

### Key Features

- **Intelligent Categorization**: LLM-powered classification into 3 segments:
  - 📎 **Attachments**: For current students requiring institution letters
  - 🎓 **Internships**: For fresh graduates (0-2 years experience)
  - 💼 **Jobs**: For professionals seeking full-time employment

- **Multi-Platform**: 
  - Web App (Next.js 15)
  - Mobile App (Flutter 3.x) - Coming soon
  - Python Scraper (Automated data collection)

- **Real-Time Updates**: Automated scraping from Fuzu, MyJobMag, and BrighterMonday
- **Smart Notifications**: Push notifications for new opportunities in your area

## 📁 Project Structure

```
KaziLink/
├── scraper/              # Python web scraper
│   ├── scrapers/         # Site-specific scrapers
│   │   ├── fuzu.py
│   │   ├── myjobmag.py
│   │   └── brightermonday.py
│   ├── categorizer.py    # LLM-based categorization
│   ├── scraper.py        # Main orchestrator
│   └── requirements.txt
│
├── web/                  # Next.js 15 web application
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Supabase clients
│   │   └── types/        # TypeScript definitions
│   └── package.json
│
├── mobile/               # Flutter mobile app (coming soon)
│
├── supabase/             # Database migrations
│   └── migrations/
│       ├── 001_initial_schema.sql
│       └── 002_rls_policies.sql
│
└── assets/               # Branding and design assets
    └── branding/
        ├── site.webmanifest
        └── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for web app)
- Python 3.10+ (for scraper)
- Supabase account
- OpenAI API key (for LLM categorization)

### 1. Set Up Supabase

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Run the migrations:
   ```sql
   -- Copy and run the SQL from supabase/migrations/001_initial_schema.sql
   -- Then run 002_rls_policies.sql
   ```
3. Note your project URL and anon key

### 2. Configure Environment Variables

**For the scraper:**
```bash
cd scraper
cp .env.example .env
# Edit .env with your credentials:
# - SUPABASE_URL
# - SUPABASE_SERVICE_ROLE_KEY
# - OPENAI_API_KEY
```

**For the web app:**
```bash
cd web
cp .env.local.example .env.local
# Edit .env.local with:
# - NEXT_PUBLIC_SUPABASE_URL
# - NEXT_PUBLIC_SUPABASE_ANON_KEY
```

### 3. Run the Scraper

```bash
cd scraper
pip install -r requirements.txt
playwright install chromium

# Test run (dry-run mode, no database writes)
python scraper.py --dry-run --pages 1

# Full scrape
python scraper.py --pages 3
```

### 4. Run the Web App

```bash
cd web
npm install
npm run dev
```

Visit `http://localhost:3000`

## 🎨 Branding

- **Primary Color**: Professional Slate (#2D3436)
- **Accent Color**: Kinetic Orange (#FF7675)
- **Logo**: Growth ladder 'K' with three ascending bars
- **Font**: Inter (web), Roboto (Android), SF Pro (iOS)

## 🏗️ Tech Stack

### Backend (Scraper)
- Python 3.10+
- Playwright (dynamic content)
- BeautifulSoup4 (HTML parsing)
- OpenAI GPT-4 (categorization)
- Supabase Python SDK

### Frontend (Web)
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Supabase SSR

### Database
- PostgreSQL (via Supabase)
- Row Level Security
- Full-text search

### Mobile (Coming Soon)
- Flutter 3.x
- Firebase Cloud Messaging
- Supabase Flutter SDK

## 📊 Database Schema

Key tables:
- `opportunities`: Job listings with category, location, deadline
- `user_saved_opportunities`: Bookmarked jobs
- `notification_preferences`: User alert settings
- `applications`: Application tracking

See `supabase/migrations/` for full schema.

## 🤖 How the Scraper Works

1. **Scraping**: Playwright visits job boards and extracts listings
2. **Categorization**: GPT-4 analyzes job descriptions to determine type
3. **Deduplication**: Checks existing URLs to avoid duplicates
4. **Storage**: Saves to Supabase with proper categorization

## 📱 Mobile App (Coming Soon)

Flutter app features:
- Bottom navigation with 3 tabs
- Push notifications per category
- Location-based filtering
- Offline support
- Dark mode

## 🔐 Security

- Row Level Security (RLS) on all tables
- Service role key only for scraper
- Anon key for public reads
- User authentication via Supabase Auth

## 🚢 Deployment

### Web App
```bash
cd web
vercel deploy
```

### Scraper (Scheduled)
Run as a cron job on your server or using GitHub Actions:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

## 📈 Future Enhancements

- [ ] Email alerts
- [ ] Resume builder
- [ ] Application tracking
- [ ] Company profiles
- [ ] Salary insights
- [ ] Interview prep resources

## 🤝 Contributing

This is a learning project. Feel free to learn from the code structure and adapt for your own use cases.

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

For questions or issues with setup, refer to:
- Supabase docs: https://supabase.com/docs
- Next.js docs: https://nextjs.org/docs
- Playwright docs: https://playwright.dev/python/docs/intro

---

**Built with ❤️ for Kenyan students and graduates**
