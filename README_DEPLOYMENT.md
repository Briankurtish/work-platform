# SmartBoostPro - Deployment Documentation

## 📚 Documentation Overview

This repository contains comprehensive deployment documentation for the SmartBoostPro Django application. All documentation has been created based on the current server deployment analysis.

---

## 📖 Available Documentation

### 1. **DEPLOYMENT_GUIDE.md** - Complete Deployment Instructions
**Purpose**: Step-by-step guide to deploy SmartBoostPro from scratch

**Contents**:
- System requirements and prerequisites
- Detailed installation steps (1-11)
- Configuration file examples
- Troubleshooting guide
- Maintenance procedures
- Regular update workflows

**When to use**: When deploying to a new server or recreating the entire deployment

---

### 2. **QUICK_REFERENCE.md** - Quick Command Reference
**Purpose**: Fast access to common commands and operations

**Contents**:
- Quick deployment commands
- Service management commands
- Database operations
- File locations
- Django management commands
- SSL certificate management
- Troubleshooting quick fixes

**When to use**: Daily operations, quick lookups, emergency fixes

---

### 3. **DEPLOYMENT_SUMMARY.md** - Architecture Overview
**Purpose**: High-level overview of the deployment architecture

**Contents**:
- Current deployment status
- Technology stack details
- Architecture diagrams
- Configuration file locations
- Security improvements made
- Performance optimization opportunities
- Maintenance checklist
- Emergency procedures

**When to use**: Understanding the overall system, planning improvements, onboarding new team members

---

### 4. **ARCHITECTURE.txt** - Visual Architecture Diagram
**Purpose**: ASCII art visualization of the deployment

**Contents**:
- Network topology diagram
- Data flow visualization
- Security layers breakdown
- Component relationships
- Quick command reference

**When to use**: Quick visual reference, presentations, documentation

---

### 5. **Automation Scripts**

#### `deploy.sh` - Automated Deployment Script
```bash
sudo /var/www/smartboostpro/deploy.sh
```
**What it does**:
- Pulls latest code from Git
- Installs/updates dependencies
- Runs database migrations
- Collects static files
- Sets proper permissions
- Restarts services
- Checks service status

#### `backup.sh` - Automated Backup Script
```bash
sudo /var/www/smartboostpro/backup.sh
```
**What it does**:
- Backs up PostgreSQL database
- Backs up media files
- Backs up .env configuration
- Compresses backups
- Cleans up old backups (>7 days)
- Shows backup summary

---

## 🚀 Quick Start

### For First-Time Deployment
1. Read: `DEPLOYMENT_GUIDE.md`
2. Follow steps 1-11 in order
3. Verify deployment with final checks

### For Daily Operations
1. Use: `QUICK_REFERENCE.md`
2. Run automated scripts when needed
3. Check service status regularly

### For Understanding the System
1. Read: `DEPLOYMENT_SUMMARY.md`
2. View: `ARCHITECTURE.txt`
3. Review configuration files

---

## 📋 Current Deployment Status

### ✅ What's Working
- **Web Server**: Nginx 1.24.0 (running)
- **Application**: Django 5.1.3 on Python 3.12.3 (running)
- **Database**: PostgreSQL 16.11 (running)
- **SSL**: Let's Encrypt certificate (valid until 2026-02-21)
- **Domain**: smartboostpro.com, www.smartboostpro.com
- **Security**: Credentials secured in environment variables

### ⚠️ Recommended Improvements
1. **Switch to Gunicorn**: Replace Django development server with production-ready Gunicorn
2. **Automated Backups**: Setup cron jobs for regular backups
3. **Monitoring**: Implement application and server monitoring
4. **Firewall**: Configure UFW for additional security
5. **Non-root User**: Run application as dedicated user

---

## 🔧 Common Tasks

### Deploy Code Updates
```bash
# Automated (recommended)
sudo /var/www/smartboostpro/deploy.sh

# Manual
cd /var/www/smartboostpro
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart django.service
```

### Backup Database
```bash
# Automated (recommended)
sudo /var/www/smartboostpro/backup.sh

# Manual
sudo -u postgres pg_dump smartboost > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql
```

### Restart Services
```bash
sudo systemctl restart django.service
sudo systemctl restart nginx
sudo systemctl restart postgresql
```

### View Logs
```bash
# Django logs
sudo journalctl -u django.service -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log

# All logs
sudo journalctl -u django.service -u nginx -f
```

### Check Service Status
```bash
# One-liner health check
echo "Django: $(systemctl is-active django.service) | Nginx: $(systemctl is-active nginx) | PostgreSQL: $(systemctl is-active postgresql)"

# Detailed status
sudo systemctl status django.service nginx postgresql
```

---

## 📁 Important File Locations

### Configuration Files
```
/etc/nginx/sites-available/smartboostpro    # Nginx configuration
/etc/systemd/system/django.service          # Django systemd service
/var/www/smartboostpro/config/settings.py   # Django settings
/var/www/smartboostpro/.env                 # Environment variables (SECRET!)
/etc/letsencrypt/live/smartboostpro.com/    # SSL certificates
```

### Application Files
```
/var/www/smartboostpro/                     # Project root
/var/www/smartboostpro/venv/                # Virtual environment
/var/www/smartboostpro/staticfiles/         # Static files
/var/www/smartboostpro/media/               # Media files
```

### Logs
```
/var/log/nginx/access.log                   # Nginx access log
/var/log/nginx/error.log                    # Nginx error log
journalctl -u django.service                # Django logs
/var/log/postgresql/                        # PostgreSQL logs
```

### Backups
```
/var/backups/smartboostpro/                 # Backup directory
```

---

## 🔒 Security Notes

### ✅ Security Measures Implemented
1. **SSL/TLS**: HTTPS enabled with Let's Encrypt
2. **Environment Variables**: All credentials in `.env` file
3. **Git Ignore**: `.env` file is gitignored
4. **Security Headers**: HSTS, X-Frame-Options, etc. configured in Nginx
5. **CSRF Protection**: Django CSRF protection enabled
6. **Database Credentials**: Secured in environment variables
7. **Email Credentials**: Secured in environment variables

### 🔐 Important Security Files
- **DO NOT COMMIT**: `.env` file
- **DO NOT SHARE**: Database passwords, email passwords, SECRET_KEY
- **DO BACKUP**: `.env` file (securely, not in Git)
- **DO RESTRICT**: File permissions on `.env` (chmod 600)

---

## 🆘 Emergency Procedures

### Application is Down
```bash
# Check what's wrong
sudo systemctl status django.service nginx postgresql

# Restart everything
sudo systemctl restart django.service nginx

# Check logs
sudo journalctl -u django.service -n 100
```

### Database Connection Failed
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Test connection
sudo -u postgres psql -d smartboost -c "SELECT 1;"
```

### SSL Certificate Expired
```bash
# Check certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew --force-renewal

# Restart Nginx
sudo systemctl restart nginx
```

### Out of Disk Space
```bash
# Check disk usage
df -h

# Clean old logs
sudo journalctl --vacuum-time=7d

# Clean old backups
find /var/backups/smartboostpro -mtime +30 -delete
```

---

## 📞 Support Information

### Server Details
- **IP Address**: 109.176.198.41
- **Domain**: smartboostpro.com
- **OS**: Ubuntu 24.04 LTS
- **SSH Access**: `ssh root@109.176.198.41`

### Service Ports
- **HTTP**: 80 (redirects to HTTPS)
- **HTTPS**: 443
- **Django**: 8000 (internal)
- **PostgreSQL**: 5432 (internal)

### Important Dates
- **Deployment Date**: December 6, 2024
- **SSL Expiry**: February 21, 2026
- **Documentation Created**: January 4, 2026

---

## 📚 Additional Resources

### Django Documentation
- Official Docs: https://docs.djangoproject.com/
- Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

### Server Documentation
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- Let's Encrypt: https://letsencrypt.org/docs/

### Tools
- Gunicorn: https://docs.gunicorn.org/
- Systemd: https://www.freedesktop.org/software/systemd/man/

---

## 🎯 Next Steps

### Immediate (This Week)
1. ✅ Review all documentation
2. ⚠️ Test automated scripts (`deploy.sh`, `backup.sh`)
3. ⚠️ Setup automated backups (cron job)
4. ⚠️ Switch to Gunicorn for production
5. ⚠️ Change `DEBUG=False` in production

### Short Term (This Month)
1. Implement monitoring/alerting
2. Setup firewall (UFW)
3. Create non-root user for application
4. Test disaster recovery procedures
5. Optimize database queries

### Long Term (This Quarter)
1. Add Redis caching
2. Implement CI/CD pipeline
3. Setup staging environment
4. Performance optimization
5. Load balancing (if needed)

---

## 📝 Documentation Maintenance

### When to Update Documentation
- After major deployment changes
- When adding new services
- After security updates
- When changing architecture
- Quarterly review

### How to Update
1. Edit the relevant markdown file
2. Update version numbers and dates
3. Test any changed commands
4. Commit changes to Git (except `.env`)

---

## ✅ Deployment Checklist

Use this checklist when deploying to a new server:

- [ ] Server setup (Ubuntu, updates, packages)
- [ ] Install Python 3.12+
- [ ] Install PostgreSQL 16+
- [ ] Install Nginx
- [ ] Create database and user
- [ ] Clone/copy project to `/var/www/smartboostpro`
- [ ] Create virtual environment
- [ ] Install Python dependencies
- [ ] Create and configure `.env` file
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Configure Nginx
- [ ] Setup SSL with Let's Encrypt
- [ ] Create systemd service
- [ ] Start and enable services
- [ ] Test application access
- [ ] Setup automated backups
- [ ] Configure monitoring
- [ ] Document any customizations

---

## 📄 License & Credits

**Project**: SmartBoostPro  
**Framework**: Django 5.1.3  
**Documentation Version**: 1.0  
**Last Updated**: January 4, 2026  

---

## 🤝 Contributing

When making changes to the deployment:
1. Document all changes
2. Update relevant documentation files
3. Test changes in staging first (if available)
4. Keep backups before major changes
5. Update this README if structure changes

---

**For questions or issues, refer to the specific documentation files listed above.**

**Quick Links**:
- 📖 [Full Deployment Guide](DEPLOYMENT_GUIDE.md)
- ⚡ [Quick Reference](QUICK_REFERENCE.md)
- 🏗️ [Architecture Overview](DEPLOYMENT_SUMMARY.md)
- 🎨 [Visual Architecture](ARCHITECTURE.txt)
