# KaziLink Logo Generation Instructions

The image generation service was temporarily unavailable during project setup.  
You can generate the logo using any AI image generator (DALL-E, Midjourney, etc.) or design tool.

## Logo Concept

**Design**: A stylized letter 'K' integrated with three ascending bars (like a bar chart)

### Visual Metaphor
The three bars represent the career growth ladder:
1. **Shortest bar** - Attachments (student level)
2. **Medium bar** - Internships (graduate level) 
3. **Tallest bar** - Jobs (professional level)

### Color Specifications
- **Primary**: Professional Slate (#2D3436)
- **Accent**: Kinetic Orange (#FF7675)
- Use gradient from slate to orange for modern look

### Design Requirements
- Modern, minimalist, geometric style
- Should work at small sizes (16x16px favicon)
- Professional and trustworthy aesthetic
- Clean lines, flat design
- Square format (1:1 aspect ratio)

## Prompt for AI Image Generators

```
Create a professional logo for "KaziLink" - a career platform.
Design: Stylized letter 'K' with three ascending bars integrated into its structure, representing career progression.
The bars should increase in height (short, medium, tall) like a bar chart showing growth.
Color: Gradient from dark slate (#2D3436) to vibrant orange (#FF7675).
Style: Modern, minimalist, geometric, flat design, corporate, clean lines.
Format: Square composition, suitable for app icon and favicon.
```

## Required Files

Once generated, create these sizes:
- `logo.svg` - Scalable vector (ideal)
- `favicon-16x16.png`
- `favicon-32x32.png`
- `favicon-192x192.png` (Android Chrome)
- `favicon-512x512.png` (PWA splash)
- `apple-touch-icon.png` (180x180, iOS)

## Alternative: Text-Based Logo

Until images are generated, you can use this simple text approach:

```html
<div style="font-size: 32px; font-weight: bold; color: #FF7675;">
  KaziLink
</div>
```

Or the emoji placeholder already used in the header: 📊

## Next Steps

1. Generate logo using the prompt above
2. Save files to `d:/KaziLink/assets/branding/`
3. Update references in `web/src/app/layout.tsx` if needed
4. Update `site.webmanifest` icon paths
