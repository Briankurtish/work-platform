#!/bin/bash

# SmartBoostPro Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "================================================"
echo "SmartBoostPro Deployment Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root or with sudo"
    exit 1
fi

PROJECT_DIR="/var/www/smartboostpro"
VENV_DIR="$PROJECT_DIR/venv"

# Navigate to project directory
cd $PROJECT_DIR

print_info "Starting deployment process..."
echo ""

# Step 1: Pull latest code (if using Git)
if [ -d ".git" ]; then
    print_info "Pulling latest code from Git..."
    git pull origin main || git pull origin master
    print_success "Code updated"
else
    print_info "Not a Git repository, skipping pull"
fi
echo ""

# Step 2: Activate virtual environment and update dependencies
print_info "Activating virtual environment..."
source $VENV_DIR/bin/activate
print_success "Virtual environment activated"
echo ""

print_info "Installing/updating dependencies..."
pip install -r requirements.txt --quiet
print_success "Dependencies installed"
echo ""

# Step 3: Run migrations
print_info "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
print_success "Migrations completed"
echo ""

# Step 4: Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"
echo ""

# Step 5: Set proper permissions
print_info "Setting file permissions..."
chown -R www-data:www-data $PROJECT_DIR/staticfiles
chown -R www-data:www-data $PROJECT_DIR/media
chmod 600 $PROJECT_DIR/.env
print_success "Permissions set"
echo ""

# Step 6: Restart services
print_info "Restarting Django service..."
if systemctl is-active --quiet django.service; then
    systemctl restart django.service
    print_success "Django service restarted"
elif systemctl is-active --quiet gunicorn.service; then
    systemctl restart gunicorn.service
    print_success "Gunicorn service restarted"
else
    print_error "No Django/Gunicorn service found running"
    print_info "Starting Django service..."
    systemctl start django.service || print_error "Failed to start Django service"
fi
echo ""

print_info "Restarting Nginx..."
systemctl restart nginx
print_success "Nginx restarted"
echo ""

# Step 7: Check service status
print_info "Checking service status..."
echo ""

if systemctl is-active --quiet django.service; then
    print_success "Django service is running"
elif systemctl is-active --quiet gunicorn.service; then
    print_success "Gunicorn service is running"
else
    print_error "Django/Gunicorn service is not running!"
fi

if systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
else
    print_error "Nginx is not running!"
fi

if systemctl is-active --quiet postgresql; then
    print_success "PostgreSQL is running"
else
    print_error "PostgreSQL is not running!"
fi

echo ""
echo "================================================"
print_success "Deployment completed successfully!"
echo "================================================"
echo ""
print_info "You can check the application at: https://smartboostpro.com"
echo ""
print_info "To view logs, run:"
echo "  sudo journalctl -u django.service -f"
echo "  sudo tail -f /var/log/nginx/error.log"
echo ""
