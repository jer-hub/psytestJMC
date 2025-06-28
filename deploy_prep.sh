#!/bin/bash

echo "🚀 Preparing Django app for Vercel deployment..."

# Set environment variables for testing
export DJANGO_SETTINGS_MODULE=psytests.settings.vercel

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️ Running database migrations..."
python manage.py migrate --settings=psytests.settings.vercel

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear --settings=psytests.settings.vercel

echo "🔍 Running deployment preparation command..."
python manage.py deploy_prep --settings=psytests.settings.vercel

echo "✅ Deployment preparation completed!"
echo ""
echo "Next steps:"
echo "1. Set up a PostgreSQL database (Vercel Postgres, Supabase, Railway, etc.)"
echo "2. Configure environment variables in Vercel dashboard"
echo "3. Deploy to Vercel using 'vercel --prod'"
