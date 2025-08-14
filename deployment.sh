#!/bin/bash
# deploy.sh - Deploy latest code to production

set -e  # Exit if any command fails

APP_DIR="/var/www/SW_LOB_PORTAL"   # Path to your Django project
BRANCH="main"                      # Git branch to deploy
VENV_DIR="$APP_DIR/venv"            # Virtual environment path

echo "---- Starting deployment ----"

cd "$APP_DIR"

echo "Fetching latest changes from GitHub..."
git fetch --all
git reset --hard origin/$BRANCH

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing/updating Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying Django migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "---- Deployment complete! ----"
