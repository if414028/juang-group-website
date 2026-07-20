# Juang Group Website

Official company profile for Juang Group and its initial business ecosystem: Juang Cafe, Juang Ice Cream, and Juang Books. The current release is static and intentionally database-free.

## Technology Stack

Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4, React Server Components, and Lucide React.

## Local Development

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Production Build

```bash
npm run build
npm run start
```

`next start` reads the `PORT` environment variable supplied by the hosting environment.

## Environment Variables

Copy `.env.example` to `.env.local` and set:

```env
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

Use the final production URL in deployment so sitemap, robots, and metadata URLs resolve correctly.

## Project Structure

- `app/` — routes, layouts, metadata, sitemap, robots, and global styles
- `components/` — shared navigation, footer, cards, buttons, founder visual, and under-development UI
- `data/` — structured TypeScript content designed to be replaceable by API data
- `public/` — static assets

## Updating Website Content

Edit `data/site.ts` for navigation, business units, values, and contact information. Edit `data/cafe.ts` for Juang Cafe concept content. Longer narrative copy currently lives in each route file for clarity.

## Replacing Images

The current site uses original editorial illustrations under `public/images/` for the founder journey, Juang Cafe, Juang Ice Cream, and Juang Books. The founder illustration is intentionally symbolic and does not claim to be Justin’s portrait. When an approved portrait is available, place it at `public/images/founder/justin.webp`, update `components/ui.tsx`, and preserve meaningful alt text. Future approved Juang Cafe photography should live under `public/images/juang-cafe/`. The existing `app/favicon.ico` is a starter placeholder and should be replaced with an approved Juang Group mark.

## Design System

The implementation follows `design.md`: warm cream and ceramic surfaces, role-specific green tones, pill controls, 12px cards, tight typography, restrained layered shadows, and dark-green feature bands. Manrope is used as the permitted open-source substitute for the proprietary reference typeface.

## Hostinger Deployment

Hostinger dashboard wording can change, so adapt these steps to the available Node.js App interface:

1. Upload or clone the repository.
2. Select a Node.js version supported by the installed Next.js version.
3. Set install command to `npm install`.
4. Set build command to `npm run build`.
5. Set start command to `npm run start`.
6. Add `NEXT_PUBLIC_SITE_URL=https://your-domain.com`.
7. Connect the domain to the Node.js application and restart after deployment.

This project uses normal Node.js output, not static export, so future server rendering and API/database work remain possible.

## Future Database Integration

The arrays and typed objects in `data/` are the initial content source. They can later be replaced by repository functions that read MySQL or an external API while keeping page and component props stable. Add validation and a server-only data layer before introducing an ORM or credentials; no database package or connection is included now.
