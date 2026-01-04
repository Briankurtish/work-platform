# SmartBoostPro - Complete Deployment Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Configuration Files](#configuration-files)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)

---

## 🖥️ System Overview

### Current Deployment Architecture
- **Server OS**: Ubuntu 24.04 LTS (Linux 6.8.0-52-generic)
- **Python Version**: 3.12.3
- **Web Server**: Nginx 1.24.0
- **Database**: PostgreSQL 16.11
- **Application Server**: Django Development Server (port 8000)
- **SSL/TLS**: Let's Encrypt (Certbot)
- **Domain**: smartboostpro.com, www.smartboostpro.com
- **Project Location**: `/var/www/smartboostpro`

### Current Running Services
- ✅ Nginx (reverse proxy)
- ✅ PostgreSQL 16
- ✅ Django Development Server (manual start)
- ⚠️ Django systemd service (configured but not active)

---

## 📦 Prerequisites

### Required Software
```bash
# System packages
- Python 3.12+
- PostgreSQL 16+
- Nginx 1.24+
- Certbot (for SSL)
- Git
- pip
- virtualenv
```

### Server Requirements
- Minimum 2GB RAM
- 20GB disk space
- Root or sudo access
- Open ports: 80 (HTTP), 443 (HTTPS), 8000 (Django)

---

## 🚀 Step-by-Step Deployment

### Step 1: Update System and Install Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
sudo apt install -y nginx

# Install Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx

# Install other utilities
sudo apt install -y git curl wget build-essential
```

### Step 2: Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user (in PostgreSQL shell)
CREATE DATABASE smartboost;
CREATE USER postgres WITH PASSWORD 'your-secure-password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE smartboost TO postgres;
\q

# Exit PostgreSQL shell
```

### Step 3: Clone or Setup Project

```bash
# Create web directory
sudo mkdir -p /var/www

# Navigate to web directory
cd /var/www

# Clone your project (or copy files)
# git clone <your-repo-url> smartboostpro
# OR copy your existing project to /var/www/smartboostpro

# Set permissions
sudo chown -R $USER:$USER /var/www/smartboostpro
cd /var/www/smartboostpro
```

### Step 4: Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

```bash
# Create .env file
nano /var/www/smartboostpro/.env
```

Add the following content (replace with your actual values):

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-strong-one
DEBUG=False
DJANGO_ENVIRONMENT=production
BASE_URL=https://smartboostpro.com

# Database Configuration
DB_NAME=smartboost
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@smartboostpro.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=SmartBoostPro <info@smartboostpro.com>
```

```bash
# Secure the .env file
chmod 600 /var/www/smartboostpro/.env
```

### Step 6: Run Django Migrations and Collect Static Files

```bash
# Activate virtual environment if not already active
source /var/www/smartboostpro/venv/bin/activate

# Navigate to project directory
cd /var/www/smartboostpro

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set proper permissions for static and media files
sudo chown -R www-data:www-data /var/www/smartboostpro/staticfiles
sudo chown -R www-data:www-data /var/www/smartboostpro/media
```

### Step 7: Configure Nginx

```bash
# Create Nginx configuration file
sudo nano /etc/nginx/sites-available/smartboostpro
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name smartboostpro.com www.smartboostpro.com;

    # Redirect all HTTP traffic to HTTPS (will be configured after SSL)
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name smartboostpro.com www.smartboostpro.com;

    # SSL configuration (will be added by Certbot)
    # ssl_certificate /etc/letsencrypt/live/smartboostpro.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/smartboostpro.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    # Additional security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    # Proxy settings for Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files for Django
    location /static/ {
        alias /var/www/smartboostpro/staticfiles/;
        expires 6M;
        add_header Cache-Control "public";
    }

    # Media files for Django
    location /media/ {
        alias /var/www/smartboostpro/media/;
    }

    # Let's Encrypt ACME challenge for SSL renewal
    location /.well-known/acme-challenge/ {
        root /var/www/smartboostpro;
        allow all;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/smartboostpro /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx
```

### Step 8: Setup SSL with Let's Encrypt

```bash
# Obtain SSL certificate
sudo certbot --nginx -d smartboostpro.com -d www.smartboostpro.com

# Follow the prompts:
# - Enter your email address
# - Agree to terms of service
# - Choose whether to redirect HTTP to HTTPS (recommended: Yes)

# Test automatic renewal
sudo certbot renew --dry-run
```

### Step 9: Create Systemd Service for Django

**Option A: Using Django Development Server (Current Setup)**

```bash
# Create systemd service file
sudo nano /etc/systemd/system/django.service
```

Add the following content:

```ini
[Unit]
Description=Django Development Server
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/smartboostpro
Environment="PATH=/var/www/smartboostpro/venv/bin"
ExecStart=/var/www/smartboostpro/venv/bin/python /var/www/smartboostpro/manage.py runserver 0.0.0.0:8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Option B: Using Gunicorn (Recommended for Production)**

```bash
# Create systemd service file for Gunicorn
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn daemon for SmartBoostPro Django Application
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/smartboostpro
Environment="PATH=/var/www/smartboostpro/venv/bin"
ExecStart=/var/www/smartboostpro/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info \
    config.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory for Gunicorn
sudo mkdir -p /var/log/gunicorn
sudo chown -R root:www-data /var/log/gunicorn

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start the service (choose one)
# For Django development server:
sudo systemctl enable django.service
sudo systemctl start django.service

# OR for Gunicorn (recommended):
sudo systemctl enable gunicorn.service
sudo systemctl start gunicorn.service

# Check service status
sudo systemctl status django.service
# OR
sudo systemctl status gunicorn.service
```

### Step 10: Configure Firewall (Optional but Recommended)

```bash
# Install UFW if not already installed
sudo apt install -y ufw

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check firewall status
sudo ufw status
```

### Step 11: Final Verification

```bash
# Check if all services are running
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status django.service  # or gunicorn.service

# Check if Django is responding
curl http://localhost:8000

# Check if Nginx is serving the site
curl https://smartboostpro.com

# View logs if there are issues
sudo journalctl -u django.service -f
# OR
sudo journalctl -u gunicorn.service -f
sudo tail -f /var/log/nginx/error.log
```

---

## 📝 Configuration Files

### Project Structure
```
/var/www/smartboostpro/
├── apps/                    # Django applications
├── config/                  # Django configuration
│   ├── settings.py         # Main settings file
│   ├── urls.py             # URL configuration
│   └── wsgi.py             # WSGI configuration
├── media/                   # User uploaded files
├── static/                  # Development static files
├── staticfiles/            # Production static files (collected)
├── templates/              # HTML templates
├── venv/                   # Virtual environment
├── .env                    # Environment variables (SECRET!)
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── gunicorn-cfg.py        # Gunicorn configuration
```

### Important Files

**gunicorn-cfg.py** (Current Configuration):
```python
bind = '0.0.0.0:5005'
workers = 1
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
```

**requirements.txt** (Current Dependencies):
```
asgiref==3.8.1
certifi==2024.8.30
crispy-bootstrap4==2024.10
crispy-bootstrap5==2024.10
Django==5.1.3
django-crispy-forms==2.3
gunicorn==22.0.0
packaging==24.1
pillow==11.0.0
psycopg==3.2.3
psycopg2-binary==2.9.10
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
sib-api-v3-sdk==7.6.0
six==1.17.0
sqlparse==0.5.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
whitenoise==6.7.0
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Django Service Won't Start
```bash
# Check service logs
sudo journalctl -u django.service -n 50 --no-pager

# Check if port 8000 is already in use
sudo netstat -tlnp | grep :8000

# Kill process using port 8000
sudo kill -9 <PID>

# Restart service
sudo systemctl restart django.service
```

#### 2. Static Files Not Loading
```bash
# Recollect static files
cd /var/www/smartboostpro
source venv/bin/activate
python manage.py collectstatic --noinput

# Fix permissions
sudo chown -R www-data:www-data /var/www/smartboostpro/staticfiles
```

#### 3. Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d smartboost -c "SELECT 1;"

# Check .env file has correct credentials
cat /var/www/smartboostpro/.env | grep DB_
```

#### 4. Nginx 502 Bad Gateway
```bash
# Check if Django/Gunicorn is running
sudo systemctl status django.service

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Restart both services
sudo systemctl restart django.service
sudo systemctl restart nginx
```

#### 5. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Test Nginx configuration
sudo nginx -t
```

---

## 🔄 Maintenance

### Regular Maintenance Tasks

#### Update Application Code
```bash
cd /var/www/smartboostpro

# Pull latest code (if using Git)
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Django service
sudo systemctl restart django.service
```

#### Database Backup
```bash
# Create backup directory
mkdir -p /var/backups/smartboostpro

# Backup database
sudo -u postgres pg_dump smartboost > /var/backups/smartboostpro/smartboost_$(date +%Y%m%d_%H%M%S).sql

# Compress backup
gzip /var/backups/smartboostpro/smartboost_$(date +%Y%m%d_%H%M%S).sql
```

#### Database Restore
```bash
# Restore from backup
sudo -u postgres psql smartboost < /var/backups/smartboostpro/backup_file.sql
```

#### View Logs
```bash
# Django/Gunicorn logs
sudo journalctl -u django.service -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

#### Monitor System Resources
```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
htop

# Check open ports
sudo netstat -tlnp
```

### Security Updates
```bash
# Update system packages regularly
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd /var/www/smartboostpro
source venv/bin/activate
pip list --outdated
pip install --upgrade <package-name>

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🎯 Quick Commands Reference

### Service Management
```bash
# Start services
sudo systemctl start django.service
sudo systemctl start nginx
sudo systemctl start postgresql

# Stop services
sudo systemctl stop django.service
sudo systemctl stop nginx
sudo systemctl stop postgresql

# Restart services
sudo systemctl restart django.service
sudo systemctl restart nginx
sudo systemctl restart postgresql

# Check status
sudo systemctl status django.service
sudo systemctl status nginx
sudo systemctl status postgresql

# Enable on boot
sudo systemctl enable django.service
sudo systemctl enable nginx
sudo systemctl enable postgresql
```

### Django Management
```bash
# Activate virtual environment
cd /var/www/smartboostpro
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server manually
python manage.py runserver 0.0.0.0:8000

# Django shell
python manage.py shell
```

---

## 📞 Support and Resources

### Useful Links
- Django Documentation: https://docs.djangoproject.com/
- Nginx Documentation: https://nginx.org/en/docs/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Let's Encrypt: https://letsencrypt.org/
- Gunicorn Documentation: https://docs.gunicorn.org/

### Current Deployment Status
- ✅ Nginx configured and running
- ✅ PostgreSQL database configured
- ✅ SSL certificate active (expires: 2026-02-21)
- ✅ Django application running on port 8000
- ⚠️ Using Django development server (consider switching to Gunicorn for production)
- ✅ Static files served by Nginx
- ✅ Media files configured

---

## 📌 Notes

1. **Security**: The current setup runs Django development server as root. For production, consider:
   - Using Gunicorn instead of Django development server
   - Running services as a non-root user
   - Implementing proper file permissions

2. **Performance**: Consider adding:
   - Redis for caching
   - Celery for background tasks
   - Database connection pooling

3. **Monitoring**: Consider implementing:
   - Application monitoring (e.g., Sentry)
   - Server monitoring (e.g., Prometheus, Grafana)
   - Log aggregation (e.g., ELK stack)

4. **Backup Strategy**: Implement automated backups for:
   - Database (daily)
   - Media files (daily)
   - Configuration files (weekly)

---

**Last Updated**: January 4, 2026
**Version**: 1.0
**Author**: Deployment Documentation
