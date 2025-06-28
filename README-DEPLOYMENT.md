# Django Psytest - Vercel Deployment Guide

This Django application has been configured for deployment on Vercel. Follow this guide to deploy your application successfully.

## 📋 Prerequisites

1. [Vercel CLI](https://vercel.com/cli) installed: `npm i -g vercel`
2. A PostgreSQL database (see Database Options below)
3. Vercel account

## 🚀 Quick Deployment

### 1. Install Vercel CLI and Login
```bash
npm i -g vercel
vercel login
```

### 2. Set up Database
Choose one of these PostgreSQL providers:
- **Vercel Postgres** (recommended): Add in Vercel dashboard
- **Supabase**: Free tier available at [supabase.com](https://supabase.com)
- **Railway**: Free tier available at [railway.app](https://railway.app)
- **Amazon RDS**, **Google Cloud SQL**, etc.

### 3. Deploy to Vercel
```bash
# From your project directory
vercel --prod
```

### 4. Configure Environment Variables
In your Vercel dashboard, add these environment variables:

#### Required Database Variables:
- `PGDATABASE` - Your PostgreSQL database name
- `PGUSER` - Your PostgreSQL username  
- `PGPASSWORD` - Your PostgreSQL password
- `PGHOST` - Your PostgreSQL host
- `PGPORT` - Your PostgreSQL port (usually 5432)

#### Required Django Variables:
- `SECRET_KEY` - Generate a new secure secret key for production
- `EMAIL_HOST_USER` - Your email host user
- `EMAIL_HOST_PASSWORD` - Your email host password

#### Optional Social Auth Variables:
- `FB_CLIENT_ID` - Facebook OAuth client ID
- `FB_SECRET_KEY` - Facebook OAuth secret key
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_SECRET_KEY` - Google OAuth secret key

### 5. Redeploy
After setting environment variables:
```bash
vercel --prod
```

## 🔧 Local Testing

To test the production configuration locally:

### Windows (PowerShell):
```powershell
.\deploy_prep.ps1
```

### Linux/Mac:
```bash
chmod +x deploy_prep.sh
./deploy_prep.sh
```

## 📁 File Structure

The following files have been added/modified for Vercel deployment:

- `vercel.json` - Vercel configuration
- `build_files.sh` - Build script for Vercel
- `psytests/settings/vercel.py` - Production settings for Vercel
- `psytests/wsgi.py` - Updated WSGI with Vercel detection
- `.vercelignore` - Files to exclude from deployment
- `psytests/management/commands/deploy_prep.py` - Deployment helper command

## ⚙️ Configuration Details

### Static Files
- Handled by WhiteNoise middleware
- Automatically collected during build process
- Served directly by Vercel CDN

### Database
- Configured for PostgreSQL with SSL
- Uses environment variables for connection
- Automatic connection pooling

### Security
- HTTPS enforcement in production
- Secure cookies and headers
- CSRF protection enabled

## 🏥 Health Check

A health check endpoint is available at `/health/` for monitoring:
```
GET https://your-app.vercel.app/health/
```

Returns:
```json
{
  "status": "healthy",
  "service": "psytest", 
  "version": "1.0.0"
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all environment variables are set correctly
2. **Database Connection**: Ensure PostgreSQL credentials are correct and SSL is enabled
3. **Static Files**: Verify WhiteNoise is in MIDDLEWARE in settings
4. **Memory Issues**: Large dependencies like scikit-learn may need optimization

### Debugging:
- Check Vercel function logs in dashboard
- Use `vercel logs` command
- Test locally with production settings first

## 📊 Database Migration

After first deployment, run migrations:
```bash
# If you have Vercel CLI connected to your project
vercel env pull .env.production
python manage.py migrate --settings=psytests.settings.vercel
```

Or run migrations through Django admin or a management command deployed to Vercel.

## 🔄 Updates

To deploy updates:
1. Commit your changes to git
2. Run `vercel --prod`
3. Vercel will automatically rebuild and deploy

## 📞 Support

For issues with:
- Vercel deployment: [Vercel Documentation](https://vercel.com/docs)
- Django configuration: [Django Documentation](https://docs.djangoproject.com/)
- Database setup: Refer to your database provider's documentation
