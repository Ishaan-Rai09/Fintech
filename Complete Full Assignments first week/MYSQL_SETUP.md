# MySQL Database Setup Guide

## Prerequisites
- MySQL 8.0 or higher
- MySQL Workbench (optional, for GUI management)

## Installation Options

### Option 1: Standalone MySQL
Download from: https://dev.mysql.com/downloads/mysql/

### Option 2: XAMPP (Recommended for Windows)
Download from: https://www.apachefriends.org/
- Includes MySQL, phpMyAdmin, and Apache
- Easy to start/stop services

### Option 3: WAMP
Download from: https://www.wampserver.com/

## Step-by-Step Setup

### 1. Start MySQL Service

**XAMPP Users:**
```bash
# Open XAMPP Control Panel
# Click "Start" next to MySQL
```

**Standalone MySQL:**
```bash
# Windows
net start MySQL80

# Linux/Mac
sudo systemctl start mysql
```

### 2. Create Database

**Using MySQL Command Line:**
```bash
# Login to MySQL
mysql -u root -p
# Enter your password when prompted

# Create database
CREATE DATABASE finsight_db;

# Verify
SHOW DATABASES;

# Exit
EXIT;
```

**Using phpMyAdmin (XAMPP):**
1. Open http://localhost/phpmyadmin
2. Click "New" in left sidebar
3. Enter database name: `finsight_db`
4. Click "Create"

### 3. Configure Application

Edit the `.env` file:
```env
# Update this line with your MySQL password
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/finsight_db
```

**Connection String Format:**
```
mysql+mysqlconnector://username:password@host:port/database
```

**Examples:**
```env
# Default XAMPP (no password)
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/finsight_db

# With password
DATABASE_URL=mysql+mysqlconnector://root:mypassword@localhost:3306/finsight_db

# Custom user
DATABASE_URL=mysql+mysqlconnector://finsight_user:password123@localhost:3306/finsight_db
```

### 4. Initialize Database Schema

```bash
# Activate virtual environment
venv\Scripts\activate

# Run initialization script
python -m backend.database.init_db
```

This will create all 11 tables:
- users
- transactions
- portfolios
- portfolio_holdings
- stocks
- predictions
- risk_reports
- tax_records
- scraped_data
- risk_profiles
- advisory_recommendations

### 5. Verify Setup

**Check tables created:**
```bash
mysql -u root -p
USE finsight_db;
SHOW TABLES;
```

You should see all 11 tables listed.

## MySQL Configuration (Optional)

### Set Root Password (if not set)
```sql
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
FLUSH PRIVILEGES;
```

### Create Dedicated User (Recommended for Production)
```sql
# Login as root
mysql -u root -p

# Create user
CREATE USER 'finsight_user'@'localhost' IDENTIFIED BY 'strong_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON finsight_db.* TO 'finsight_user'@'localhost';
FLUSH PRIVILEGES;

# Test login
EXIT;
mysql -u finsight_user -p finsight_db
```

Then update `.env`:
```env
DATABASE_URL=mysql+mysqlconnector://finsight_user:strong_password_here@localhost:3306/finsight_db
```

## Troubleshooting

### Port 3306 Already in Use
```bash
# Check what's using port 3306
netstat -ano | findstr :3306

# Change MySQL port in my.ini (MySQL config file)
# Then update .env with new port
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3307/finsight_db
```

### Access Denied Error
```sql
# Reset permissions
mysql -u root -p
FLUSH PRIVILEGES;
GRANT ALL PRIVILEGES ON finsight_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Connection Timeout
```bash
# Check MySQL is running
# XAMPP: Check XAMPP Control Panel
# Standalone: 
netstat -ano | findstr :3306
```

### Table Creation Errors
```bash
# Drop and recreate database
mysql -u root -p
DROP DATABASE finsight_db;
CREATE DATABASE finsight_db;
EXIT;

# Reinitialize
python -m backend.database.init_db
```

### Character Set Issues
```sql
# Set UTF-8 encoding
ALTER DATABASE finsight_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## MySQL Workbench (GUI Tool)

### Installation
Download from: https://dev.mysql.com/downloads/workbench/

### Connect to Database
1. Open MySQL Workbench
2. Click "+" next to "MySQL Connections"
3. Enter:
   - Connection Name: FinSight AI
   - Hostname: localhost
   - Port: 3306
   - Username: root
4. Test Connection
5. Click "OK"

## Backup and Restore

### Backup Database
```bash
# Backup to SQL file
mysqldump -u root -p finsight_db > finsight_backup.sql

# Backup with timestamp
mysqldump -u root -p finsight_db > finsight_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sql
```

### Restore Database
```bash
mysql -u root -p finsight_db < finsight_backup.sql
```

## Performance Tuning (Optional)

### Edit my.ini (MySQL config)
```ini
[mysqld]
# Increase max connections
max_connections = 200

# Increase buffer pool size (40-80% of RAM)
innodb_buffer_pool_size = 2G

# Increase log file size
innodb_log_file_size = 512M
```

Restart MySQL after changes.

## Database Maintenance

### Optimize Tables
```sql
USE finsight_db;
OPTIMIZE TABLE users, transactions, portfolios;
```

### Check Table Status
```sql
SHOW TABLE STATUS;
```

### View Database Size
```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'finsight_db'
GROUP BY table_schema;
```

## Security Best Practices

1. **Never use root in production** - Create dedicated user
2. **Use strong passwords** - Minimum 12 characters
3. **Limit privileges** - Only grant necessary permissions
4. **Enable SSL** - For remote connections
5. **Regular backups** - Automate daily backups
6. **Update MySQL** - Keep MySQL server updated

## Quick Reference

### Common Commands
```sql
-- Show all databases
SHOW DATABASES;

-- Use database
USE finsight_db;

-- Show tables
SHOW TABLES;

-- Describe table structure
DESCRIBE users;

-- Count records
SELECT COUNT(*) FROM users;

-- View recent records
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;

-- Delete database (CAREFUL!)
DROP DATABASE finsight_db;
```

### Check MySQL Status
```bash
# Windows (Command Prompt as Admin)
sc query MySQL80

# Check version
mysql --version
```

## Next Steps

After MySQL setup is complete:
1. Run `python run.py` to start the application
2. Register a user at http://localhost:8000
3. Check database: `SELECT * FROM users;`
4. Start using the platform!

---

**For application issues, see QUICKSTART.md**  
**For API documentation, visit http://localhost:8000/docs**
