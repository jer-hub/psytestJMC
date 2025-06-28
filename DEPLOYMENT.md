# Environment Variables for Vercel Deployment

You need to set the following environment variables in your Vercel dashboard:

## Required Environment Variables:

### Database (PostgreSQL)
- `PGDATABASE` - Your PostgreSQL database name
- `PGUSER` - Your PostgreSQL username
- `PGPASSWORD` - Your PostgreSQL password
- `PGHOST` - Your PostgreSQL host
- `PGPORT` - Your PostgreSQL port (usually 5432)

### Django Configuration
- `SECRET_KEY` - Django secret key for production (generate a new secure one)
- `DJANGO_SETTINGS_MODULE` - Set to `psytests.settings.vercel`

### Email Configuration
- `EMAIL_HOST_USER` - Your email host user (currently: psytestjmc@gmail.com)
- `EMAIL_HOST_PASSWORD` - Your email host password

### Social Authentication (Optional)
- `FB_CLIENT_ID` - Facebook OAuth client ID
- `FB_SECRET_KEY` - Facebook OAuth secret key
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_SECRET_KEY` - Google OAuth secret key

## Vercel Deployment Steps:

1. Install Vercel CLI: `npm i -g vercel`
2. Login to Vercel: `vercel login`
3. Deploy: `vercel --prod`
4. Set up a PostgreSQL database (recommend: Vercel Postgres, Supabase, or Railway)
5. Configure environment variables in Vercel dashboard
6. Redeploy: `vercel --prod`

## Database Setup:

For production, you'll need a PostgreSQL database. Popular options:
- Vercel Postgres (recommended for Vercel deployments)
- Supabase (free tier available)
- Railway (free tier available)
- Amazon RDS
- Google Cloud SQL

## Static Files:

Static files are handled by WhiteNoise and will be served directly by Vercel.

## Domain Configuration:

After deployment, update `ALLOWED_HOSTS` in `vercel.py` to include your custom domain if you have one.
