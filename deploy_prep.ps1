Write-Host "🚀 Preparing Django app for Vercel deployment..." -ForegroundColor Green

# Set environment variables for testing
$env:DJANGO_SETTINGS_MODULE = "psytests.settings.vercel"

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "🗃️ Running database migrations..." -ForegroundColor Yellow
python manage.py migrate --settings=psytests.settings.vercel

Write-Host "📁 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear --settings=psytests.settings.vercel

Write-Host "🔍 Running deployment preparation command..." -ForegroundColor Yellow
python manage.py deploy_prep --settings=psytests.settings.vercel

Write-Host "✅ Deployment preparation completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Set up a PostgreSQL database (Vercel Postgres, Supabase, Railway, etc.)"
Write-Host "2. Configure environment variables in Vercel dashboard"
Write-Host "3. Deploy to Vercel using 'vercel --prod'"
