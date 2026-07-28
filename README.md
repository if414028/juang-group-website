# Juang Group Website

Official company profile for Juang Group and its initial business ecosystem: Yeshua Cafe, Juang Ice Cream, and Juang Books. Contact messages are stored in MySQL and managed through a private admin inbox.

## Technology Stack

Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4, MySQL, React Server Components, and Lucide React.

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
DATABASE_URL=mysql://database_user:database_password@database_host:3306/database_name
SESSION_SECRET=replace-with-at-least-32-random-characters
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=replace-with-a-strong-password
ADMIN_NAME=Website Admin
```

Use the final production URL in deployment so sitemap, robots, and metadata URLs resolve correctly.
`DATABASE_URL` can be replaced with the individual `DB_HOST`, `DB_PORT`,
`DB_USER`, `DB_PASSWORD`, and `DB_NAME` variables shown in `.env.example`.
Keep database credentials and `SESSION_SECRET` server-side; never prefix them
with `NEXT_PUBLIC_`.

## Database and Admin Inbox

After creating an empty MySQL database and filling `.env.local`, create the
tables and first admin account:

```bash
npm run db:setup
npm run db:seed
```

The `ADMIN_PASSWORD` must contain at least 12 characters. After the account is
created, remove `ADMIN_PASSWORD` from the production environment because the
application never needs the plaintext password at runtime.

Open `/admin/login` to access the inbox. The dashboard supports unread/read
status, search, filtering, direct email replies, and permanent deletion. Public
contact submissions are validated, protected by a honeypot and basic rate
limiting, and stored in the `contact_messages` table.

## Project Structure

- `app/` — routes, layouts, metadata, sitemap, robots, and global styles
- `components/` — shared navigation, footer, cards, buttons, founder visual, and under-development UI
- `database/` — repeatable MySQL table schema
- `lib/` — server-only database, authentication, and message repositories
- `scripts/` — database setup and initial admin creation
- `data/` — structured TypeScript content designed to be replaceable by API data
- `public/` — static assets

## Updating Website Content

Edit `data/site.ts` for navigation, business units, values, and contact information. Edit `data/cafe.ts` for Yeshua Cafe concept content. Longer narrative copy currently lives in each route file for clarity.

## Replacing Images

The current site uses original editorial illustrations under `public/images/` for the founder journey, Yeshua Cafe, Juang Ice Cream, and Juang Books. The founder illustration is intentionally symbolic and does not claim to be Justin’s portrait. When an approved portrait is available, place it at `public/images/founder/justin.webp`, update `components/ui.tsx`, and preserve meaningful alt text. Future approved Yeshua Cafe photography should live under `public/images/juang-cafe/`. The existing `app/favicon.ico` is a starter placeholder and should be replaced with an approved Juang Group mark.

## Design System

The implementation follows `design.md`: warm cream and ceramic surfaces, role-specific green tones, pill controls, 12px cards, tight typography, restrained layered shadows, and dark-green feature bands. Manrope is used as the permitted open-source substitute for the proprietary reference typeface.

## Hostinger Deployment

Hostinger dashboard wording can change, so adapt these steps to the available Node.js App interface:

1. Upload or clone the repository.
2. Select a Node.js version supported by the installed Next.js version.
3. Set install command to `npm install`.
4. Set build command to `npm run build`.
5. Set start command to `npm run start`.
6. Create a MySQL database and user from hPanel.
7. Add `NEXT_PUBLIC_SITE_URL`, the MySQL variables, and `SESSION_SECRET` in
   Hostinger's environment variable settings.
8. Run `npm run db:setup` and `npm run admin:create` once using Hostinger's
   terminal or a local connection that can reach the production database.
9. Remove `ADMIN_PASSWORD` from the production environment, connect the domain,
   and restart the application.

This project uses normal Node.js output, not static export, so future server rendering and API/database work remain possible.
