# SmartBoostPro - Quick Reference Guide

## 🚀 Quick Deployment Commands

### Deploy Updates
```bash
# Automated deployment (recommended)
sudo /var/www/smartboostpro/deploy.sh

# Manual deployment
cd /var/www/smartboostpro
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart django.service
sudo systemctl restart nginx
```

### Backup Database and Media
```bash
# Automated backup (recommended)
sudo /var/www/smartboostpro/backup.sh

# Manual database backup
sudo -u postgres pg_dump smartboost > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql
```

---

## 🔧 Service Management

### Check Service Status
```bash
sudo systemctl status django.service
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Restart Services
```bash
sudo systemctl restart django.service
sudo systemctl restart nginx
sudo systemctl restart postgresql
```

### View Service Logs
```bash
# Django logs
sudo journalctl -u django.service -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

---

## 🗄️ Database Operations

### Access Database
```bash
sudo -u postgres psql smartboost
```

### Common SQL Commands
```sql
-- List all tables
\dt

-- Describe a table
\d table_name

-- List all databases
\l

-- Quit
\q
```

### Backup and Restore
```bash
# Backup
sudo -u postgres pg_dump smartboost > backup.sql

# Restore
sudo -u postgres psql smartboost < backup.sql
```

---

## 📁 File Locations

### Important Directories
- **Project Root**: `/var/www/smartboostpro`
- **Virtual Environment**: `/var/www/smartboostpro/venv`
- **Static Files**: `/var/www/smartboostpro/staticfiles`
- **Media Files**: `/var/www/smartboostpro/media`
- **Backups**: `/var/backups/smartboostpro`

### Configuration Files
- **Django Settings**: `/var/www/smartboostpro/config/settings.py`
- **Environment Variables**: `/var/www/smartboostpro/.env`
- **Nginx Config**: `/etc/nginx/sites-available/smartboostpro`
- **Systemd Service**: `/etc/systemd/system/django.service`
- **SSL Certificates**: `/etc/letsencrypt/live/smartboostpro.com/`

---

## 🐍 Django Management

### Activate Virtual Environment
```bash
cd /var/www/smartboostpro
source venv/bin/activate
```

### Common Django Commands
```bash
# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Run development server (manual)
python manage.py runserver 0.0.0.0:8000
```

---

## 🔒 SSL Certificate Management

### Check Certificate Status
```bash
sudo certbot certificates
```

### Renew Certificate
```bash
# Test renewal
sudo certbot renew --dry-run

# Force renewal
sudo certbot renew --force-renewal
```

### Auto-renewal
Certbot automatically sets up a cron job or systemd timer for renewal.

---

## 🛠️ Troubleshooting

### Django Service Not Starting
```bash
# Check logs
sudo journalctl -u django.service -n 50

# Check if port is in use
sudo netstat -tlnp | grep :8000

# Kill process on port 8000
sudo kill -9 $(sudo lsof -t -i:8000)

# Restart service
sudo systemctl restart django.service
```

### Static Files Not Loading
```bash
cd /var/www/smartboostpro
source venv/bin/activate
python manage.py collectstatic --noinput
sudo chown -R www-data:www-data staticfiles/
sudo systemctl restart nginx
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -d smartboost -c "SELECT 1;"

# Check credentials in .env
cat /var/www/smartboostpro/.env | grep DB_
```

### Nginx 502 Bad Gateway
```bash
# Check if Django is running
sudo systemctl status django.service

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Restart both services
sudo systemctl restart django.service nginx
```

---

## 📊 Monitoring

### Check System Resources
```bash
# Disk usage
df -h

# Memory usage
free -h

# CPU and processes
htop

# Network connections
sudo netstat -tlnp
```

### Check Application Health
```bash
# Test local Django
curl http://localhost:8000

# Test through Nginx
curl https://smartboostpro.com

# Check response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://smartboostpro.com
```

---

## 🔐 Security

### Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### Update Python Packages
```bash
cd /var/www/smartboostpro
source venv/bin/activate
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Check File Permissions
```bash
# .env file should be 600
ls -la /var/www/smartboostpro/.env

# Fix if needed
sudo chmod 600 /var/www/smartboostpro/.env
```

---

## 📝 Environment Variables

### View Environment Variables (Safe)
```bash
cat /var/www/smartboostpro/.env | grep -v "PASSWORD\|SECRET"
```

### Edit Environment Variables
```bash
sudo nano /var/www/smartboostpro/.env
# After editing, restart Django service
sudo systemctl restart django.service
```

---

## 🌐 Network

### Check Open Ports
```bash
sudo netstat -tlnp
```

### Firewall Status
```bash
sudo ufw status
```

### Add Firewall Rule
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 📞 Emergency Contacts

### Current Setup
- **Domain**: smartboostpro.com, www.smartboostpro.com
- **Server IP**: 109.176.198.41
- **Django Port**: 8000
- **Database**: PostgreSQL 16 (smartboost)
- **SSL Expires**: 2026-02-21

### Quick Health Check
```bash
# One-liner to check all services
echo "Django: $(systemctl is-active django.service) | Nginx: $(systemctl is-active nginx) | PostgreSQL: $(systemctl is-active postgresql)"
```

---

## 📚 Additional Resources

- Full deployment guide: `/var/www/smartboostpro/DEPLOYMENT_GUIDE.md`
- Deployment script: `/var/www/smartboostpro/deploy.sh`
- Backup script: `/var/www/smartboostpro/backup.sh`

---

**Last Updated**: January 4, 2026
