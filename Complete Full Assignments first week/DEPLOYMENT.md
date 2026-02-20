# FinSight AI - Deployment Guide (Local MySQL)

## 🏠 Local Development Deployment

### System Requirements
- Windows 10/11, Linux, or macOS
- Python 3.11+
- MySQL 8.0+
- 4GB RAM minimum
- 500MB disk space

---

## 📦 Production Deployment (Local Server)

### 1. Server Setup

**Windows Server:**
```powershell
# Install Python 3.11+
# Install MySQL 8.0+
# Install Git (optional)

# Create application directory
mkdir C:\Apps\FinSightAI
cd C:\Apps\FinSightAI
```

**Linux Server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install MySQL
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

# Create app directory
sudo mkdir -p /opt/finsight-ai
cd /opt/finsight-ai
```

### 2. MySQL Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Create production database
CREATE DATABASE finsight_prod;

# Create dedicated user (RECOMMENDED)
CREATE USER 'finsight_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON finsight_prod.* TO 'finsight_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Application Installation

```bash
# Copy application files to server
# (via FTP, Git, or direct copy)

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Production Configuration

Create `.env` file:
```env
# Application
APP_NAME=FinSight AI
DEBUG=False
ENVIRONMENT=production

# Security (IMPORTANT: Generate new key!)
SECRET_KEY=your_super_long_secret_key_here_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (PRODUCTION)
DATABASE_URL=mysql+mysqlconnector://finsight_user:strong_password_here@localhost:3306/finsight_prod

# Redis (Optional - for caching)
# REDIS_URL=redis://localhost:6379

# CORS (Update with your domain)
CORS_ORIGINS=["http://localhost:8000","http://your-domain.com","https://your-domain.com"]

# API Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/finsight_prod.log
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Initialize Database

```bash
# Create tables
python -m backend.database.init_db

# Verify tables created
mysql -u finsight_user -p finsight_prod
SHOW TABLES;
EXIT;
```

### 6. Run Application

**Option A: Direct (Testing)**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Option B: Production with Gunicorn (Linux)**
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info
```

**Option C: Windows Service**
```powershell
# Install NSSM (Non-Sucking Service Manager)
# Download from: https://nssm.cc/download

# Install as Windows service
nssm install FinSightAI "C:\Apps\FinSightAI\venv\Scripts\python.exe" ^
  "-m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

# Start service
nssm start FinSightAI
```

### 7. Configure Firewall

**Windows:**
```powershell
# Allow port 8000
netsh advfirewall firewall add rule name="FinSight AI" ^
  dir=in action=allow protocol=TCP localport=8000
```

**Linux:**
```bash
# UFW Firewall
sudo ufw allow 8000/tcp
sudo ufw enable
```

---

## 🔒 Security Hardening

### MySQL Security

```bash
# Run MySQL secure installation
mysql_secure_installation

# Answer prompts:
# - Set root password: YES
# - Remove anonymous users: YES
# - Disallow root login remotely: YES
# - Remove test database: YES
# - Reload privilege tables: YES
```

**Restrict MySQL to localhost:**
```bash
# Edit MySQL config
# Linux: /etc/mysql/mysql.conf.d/mysqld.cnf
# Windows: C:\ProgramData\MySQL\MySQL Server 8.0\my.ini

# Add/verify:
bind-address = 127.0.0.1
```

### Application Security

**1. Change Default Credentials**
```bash
# Generate new SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env with new key
```

**2. Disable Debug Mode**
```env
DEBUG=False
```

**3. Configure CORS Properly**
```env
# Only allow your domain
CORS_ORIGINS=["https://your-domain.com"]
```

**4. File Permissions (Linux)**
```bash
# Restrict .env file
chmod 600 .env

# Set app ownership
sudo chown -R www-data:www-data /opt/finsight-ai
```

**5. Regular Updates**
```bash
# Update dependencies quarterly
pip list --outdated
pip install --upgrade <package-name>
```

---

## 🌐 Reverse Proxy with Nginx (Linux)

### Install Nginx
```bash
sudo apt install nginx -y
```

### Configure Nginx
Create `/etc/nginx/sites-available/finsight`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/finsight-ai/frontend;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/finsight /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Let's Encrypt (Optional)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

---

## 🔄 Process Management

### Systemd Service (Linux)

Create `/etc/systemd/system/finsight.service`:
```ini
[Unit]
Description=FinSight AI Application
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/finsight-ai
Environment="PATH=/opt/finsight-ai/venv/bin"
ExecStart=/opt/finsight-ai/venv/bin/gunicorn \
  backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/finsight/access.log \
  --error-logfile /var/log/finsight/error.log
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Manage service:**
```bash
# Create log directory
sudo mkdir -p /var/log/finsight
sudo chown www-data:www-data /var/log/finsight

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable finsight
sudo systemctl start finsight

# Check status
sudo systemctl status finsight

# View logs
sudo journalctl -u finsight -f
```

---

## 📊 Monitoring

### Application Health Check
```bash
# Check if app is running
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "app": "FinSight AI",
  "version": "1.0.0"
}
```

### MySQL Monitoring
```bash
# Check connection
mysql -u finsight_user -p -e "SELECT 1"

# View slow queries
mysql -u root -p
SHOW STATUS LIKE 'Slow_queries';

# Check table sizes
SELECT 
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.tables
WHERE table_schema = 'finsight_prod'
ORDER BY (data_length + index_length) DESC;
```

### Log Monitoring
```bash
# Application logs
tail -f logs/finsight_prod.log

# Nginx logs (if using)
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u finsight -f
```

---

## 💾 Backup Strategy

### Database Backup

**Automated Daily Backup (Linux):**
```bash
#!/bin/bash
# Save as: /opt/finsight-ai/scripts/backup-db.sh

BACKUP_DIR="/opt/finsight-ai/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u finsight_user -p'strong_password_here' finsight_prod | gzip > $BACKUP_DIR/finsight_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "finsight_*.sql.gz" -mtime +30 -delete

echo "Backup completed: finsight_$DATE.sql.gz"
```

**Schedule with Cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/finsight-ai/scripts/backup-db.sh >> /var/log/finsight/backup.log 2>&1
```

**Windows Task Scheduler:**
```bat
@echo off
REM Save as: backup-db.bat

set BACKUP_DIR=C:\Apps\FinSightAI\backups
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%
mkdir %BACKUP_DIR%

mysqldump -u finsight_user -pstrong_password_here finsight_prod > %BACKUP_DIR%\finsight_%DATE%.sql

echo Backup completed: finsight_%DATE%.sql
```

### Restore Database
```bash
# Restore from backup
gunzip < /path/to/backup/finsight_20250116.sql.gz | mysql -u finsight_user -p finsight_prod

# Or from .sql file
mysql -u finsight_user -p finsight_prod < /path/to/backup/finsight_20250116.sql
```

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Python 3.11+ installed
- [ ] MySQL 8.0+ installed and secured
- [ ] Application files copied to server
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` configured with production settings
- [ ] SECRET_KEY generated and set
- [ ] Database created and initialized
- [ ] Firewall configured
- [ ] Backup strategy implemented

### Post-Deployment
- [ ] Application starts without errors
- [ ] Health check endpoint returns 200 OK
- [ ] User registration works
- [ ] User login works
- [ ] API endpoints accessible
- [ ] Frontend pages load correctly
- [ ] MySQL connections stable
- [ ] Logs are being written
- [ ] Process manager configured (systemd/NSSM)
- [ ] SSL certificate installed (if public)

### Security
- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY generated
- [ ] MySQL root password changed
- [ ] Dedicated MySQL user created
- [ ] MySQL bound to localhost
- [ ] CORS configured for specific domain
- [ ] .env file permissions restricted (600)
- [ ] Regular backup schedule set
- [ ] Monitoring configured

---

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Check logs
tail -n 100 logs/finsight_prod.log

# Check if port is in use
netstat -tuln | grep 8000

# Test database connection
python -c "from backend.database.connection import get_db; print('DB OK')"
```

### MySQL Connection Errors
```bash
# Test MySQL connection
mysql -u finsight_user -p finsight_prod

# Check MySQL service
# Linux:
sudo systemctl status mysql
# Windows:
net start MySQL80
```

### High Memory Usage
```bash
# Check process memory
ps aux | grep python

# Reduce Gunicorn workers
gunicorn ... --workers 2 ...

# Configure MySQL buffer pool
# Edit my.cnf/my.ini:
innodb_buffer_pool_size = 256M
```

### Slow Response Times
```bash
# Check MySQL slow queries
mysql> SHOW STATUS LIKE 'Slow_queries';

# Add indexes to frequently queried columns
# Check query execution plans

# Enable Redis caching (optional)
pip install redis
# Set REDIS_URL in .env
```

---

## 📚 Additional Resources

- [MYSQL_SETUP.md](MYSQL_SETUP.md) - Detailed MySQL setup
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Complete setup guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [TESTING.md](TESTING.md) - Testing procedures

---

## 🆘 Support

For deployment issues:
1. Check application logs: `logs/finsight_prod.log`
2. Check MySQL logs: `/var/log/mysql/error.log`
3. Review configuration: `.env` file
4. Test database connection
5. Verify all services are running

---

**Deployment Status:** 🟢 Production Ready (Local MySQL)  
**Last Updated:** 2025-01-16
