# Quick Start Guide - AWS EC2 Deployment

This is a condensed version of the full deployment guide. Refer to `DEPLOYMENT_GUIDE.md` for detailed instructions.

## Prerequisites Checklist

- [ ] AWS Account with EC2 access
- [ ] NeonDB account and database created
- [ ] SSH key pair for EC2
- [ ] Domain name (optional)

## Step-by-Step Quick Deployment

### 1. Launch EC2 Instance

```bash
# In AWS Console:
# - AMI: Ubuntu 22.04 LTS
# - Instance Type: t3.medium (minimum) or t3.large (recommended)
# - Security Group: Allow SSH (22), HTTP (80), HTTPS (443)
# - Storage: 30 GB
```

### 2. Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 3. Install Docker

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### 4. Clone/Upload Project

```bash
# Option 1: Git
git clone <your-repo> /home/ubuntu/aviatrax
cd /home/ubuntu/aviatrax/Aviatrax

# Option 2: SCP from local machine
# scp -r -i your-key.pem ./Aviatrax ubuntu@<EC2_IP>:/home/ubuntu/aviatrax/
```

### 5. Configure Environment

```bash
# Backend .env
cd backend
nano .env
# Add:
# SECRET_KEY=your-secret-key-here
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=your_host.neon.tech
# DB_PORT=5432
# DEBUG=False
# FLASK_ENV=production

# Frontend .env.production (optional - Nginx handles proxying)
cd ../frontend
nano .env.production
# Add:
# VITE_API_BASE_URL=http://localhost:8000
```

### 6. Import Database Schema

**Run from EC2 (Recommended)** or your local machine:

```bash
# On EC2: Install PostgreSQL client first
sudo apt install -y postgresql-client

# Navigate to project directory
cd /home/ubuntu/aviatrax/Aviatrax

# Import database schema using your AWS RDS credentials
psql "postgresql://postgres:aviatraxtrial@aviatrax-trial.cbgmomk60nq8.ap-south-1.rds.amazonaws.com:5432/postgres?sslmode=require" < ERP_full.sql

# Verify tables were created
psql "postgresql://postgres:aviatraxtrial@aviatrax-trial.cbgmomk60nq8.ap-south-1.rds.amazonaws.com:5432/postgres?sslmode=require" -c "\dt"
```

**Note**: Ensure your RDS security group allows connections from your EC2 instance.

### 7. Deploy with Docker

```bash
cd /home/ubuntu/aviatrax/Aviatrax
docker compose build
docker compose up -d
```

### 8. Verify Deployment

```bash
# Check containers
docker compose ps

# Check logs
docker compose logs -f

# Test backend
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:80
```

### 9. Access Application

Open browser: `http://<EC2_PUBLIC_IP>`

## Common Commands

```bash
# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart services
docker compose restart

# Stop services
docker compose down

# Update application
git pull
docker compose build --no-cache
docker compose up -d

# Check resource usage
docker stats
```

## Troubleshooting

**Backend won't start?**
```bash
docker compose logs backend
# Check database connection in logs
```

**Frontend won't load?**
```bash
docker compose logs frontend
# Check if backend is healthy
curl http://localhost:8000/api/health
```

**Database connection issues?**
```bash
# Test connection from EC2
psql "postgresql://user:pass@host.neon.tech:5432/dbname?sslmode=require"
```

**Out of disk space?**
```bash
docker system prune -a
df -h
```

## Next Steps

1. Set up SSL/HTTPS (Let's Encrypt or AWS Certificate Manager)
2. Configure custom domain
3. Set up automated backups
4. Configure CloudWatch monitoring
5. Set up CI/CD pipeline (optional)

For detailed information, see `DEPLOYMENT_GUIDE.md`.

