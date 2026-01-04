#!/bin/bash

# SmartBoostPro Backup Script
# This script backs up the database and media files

set -e  # Exit on any error

echo "================================================"
echo "SmartBoostPro Backup Script"
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

# Configuration
PROJECT_DIR="/var/www/smartboostpro"
BACKUP_DIR="/var/backups/smartboostpro"
DB_NAME="smartboost"
DB_USER="postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

print_info "Starting backup process..."
echo ""

# Step 1: Backup Database
print_info "Backing up PostgreSQL database..."
sudo -u postgres pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

if [ $? -eq 0 ]; then
    print_success "Database backed up: db_backup_$TIMESTAMP.sql"
    
    # Compress the backup
    print_info "Compressing database backup..."
    gzip $BACKUP_DIR/db_backup_$TIMESTAMP.sql
    print_success "Database backup compressed: db_backup_$TIMESTAMP.sql.gz"
else
    print_error "Database backup failed!"
    exit 1
fi
echo ""

# Step 2: Backup Media Files
print_info "Backing up media files..."
if [ -d "$PROJECT_DIR/media" ]; then
    tar -czf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz -C $PROJECT_DIR media/
    print_success "Media files backed up: media_backup_$TIMESTAMP.tar.gz"
else
    print_info "No media directory found, skipping media backup"
fi
echo ""

# Step 3: Backup .env file (important!)
print_info "Backing up environment configuration..."
if [ -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env $BACKUP_DIR/env_backup_$TIMESTAMP
    chmod 600 $BACKUP_DIR/env_backup_$TIMESTAMP
    print_success "Environment file backed up: env_backup_$TIMESTAMP"
else
    print_error ".env file not found!"
fi
echo ""

# Step 4: Calculate backup sizes
print_info "Backup Summary:"
echo ""
ls -lh $BACKUP_DIR/*$TIMESTAMP* | awk '{print "  " $9 " - " $5}'
echo ""

# Step 5: Clean up old backups (keep last 7 days)
print_info "Cleaning up old backups (keeping last 7 days)..."
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "env_backup_*" -mtime +7 -delete
print_success "Old backups cleaned up"
echo ""

# Step 6: Show remaining backups
BACKUP_COUNT=$(ls -1 $BACKUP_DIR/db_backup_*.sql.gz 2>/dev/null | wc -l)
print_info "Total database backups: $BACKUP_COUNT"
echo ""

echo "================================================"
print_success "Backup completed successfully!"
echo "================================================"
echo ""
print_info "Backup location: $BACKUP_DIR"
echo ""
print_info "To restore database, run:"
echo "  gunzip -c $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz | sudo -u postgres psql $DB_NAME"
echo ""
print_info "To restore media files, run:"
echo "  tar -xzf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz -C $PROJECT_DIR"
echo ""
