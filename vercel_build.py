#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command):
    """Run a command and handle errors"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result.stdout

def main():
    """Main build process for Vercel"""
    print("🚀 Starting Vercel build process...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psytests.settings.vercel')
    
    # Install dependencies
    print("📦 Installing dependencies...")
    run_command("pip install -r requirements.txt")
    
    # Run Django commands
    print("🗃️ Making migrations...")
    run_command("python manage.py makemigrations --noinput")
    
    print("🗃️ Running migrations...")
    run_command("python manage.py migrate --noinput")
    
    print("📁 Collecting static files...")
    run_command("python manage.py collectstatic --noinput --clear")
    
    print("✅ Build completed successfully!")

if __name__ == "__main__":
    main()
