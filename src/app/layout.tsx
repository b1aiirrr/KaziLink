import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'KaziLink - Your Ladder to Professional Success',
  description: 'Discover attachments, internships, and entry-level jobs curated specifically for Kenyan students and graduates.',
  keywords: ['Kenya jobs', 'internships', 'attachments', 'industrial attachment', 'graduate programs', 'entry-level jobs'],
  authors: [{ name: 'KaziLink' }],
  themeColor: '#FF7675',
  manifest: '/assets/branding/site.webmanifest',
  icons: {
    icon: '/assets/branding/favicon-32x32.png',
    apple: '/assets/branding/apple-touch-icon.png',
  },
  openGraph: {
    title: 'KaziLink - Your Ladder to Professional Success',
    description: 'Discover attachments, internships, and entry-level jobs in Kenya',
    type: 'website',
    locale: 'en_KE',
  }
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
