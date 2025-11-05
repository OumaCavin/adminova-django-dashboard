# Deployment Guide for Adminova

## Deployment Options

Adminova can be deployed to multiple platforms:
1. Traditional VM (Ubuntu + Nginx + Gunicorn)
2. Docker-based deployment
3. Platform-as-a-Service (Vercel, Netlify)
4. Supabase Edge Functions (for API only)

## Prerequisites

- Python 3.12+
- PostgreSQL or MySQL database
- Domain with SSL certificate
- M-Pesa production credentials

## Option 1: Ubuntu Server with Nginx

### Server Setup

1. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install dependencies**
```bash
sudo apt install python3.12 python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

3. **Create application user**
```bash
sudo adduser adminova
sudo usermod -aG sudo adminova
su - adminova
```

4. **Clone repository**
```bash
git clone https://github.com/OumaCavin/adminova-django-dashboard.git
cd adminova-django-dashboard
```

5. **Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/production.txt
```

6. **Configure environment**
```bash
cp .env.example .env
nano .env  # Edit with production settings
```

7. **Set up database**
```bash
sudo -u postgres psql
CREATE DATABASE adminova;
CREATE USER adminova WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE adminova TO adminova;
\q
```

8. **Run migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Gunicorn Setup

1. **Create systemd service**
```bash
sudo nano /etc/systemd/system/adminova.service
```

```ini
[Unit]
Description=Adminova Django Application
After=network.target

[Service]
User=adminova
Group=www-data
WorkingDirectory=/home/adminova/adminova-django-dashboard
Environment="PATH=/home/adminova/adminova-django-dashboard/venv/bin"
ExecStart=/home/adminova/adminova-django-dashboard/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/adminova/adminova-django-dashboard/adminova.sock \
          adminova.wsgi:application

[Install]
WantedBy=multi-user.target
```

2. **Start and enable service**
```bash
sudo systemctl start adminova
sudo systemctl enable adminova
sudo systemctl status adminova
```

### Nginx Configuration

1. **Create Nginx config**
```bash
sudo nano /etc/nginx/sites-available/adminova
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/adminova/adminova-django-dashboard/staticfiles/;
    }

    location /media/ {
        alias /home/adminova/adminova-django-dashboard/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/adminova/adminova-django-dashboard/adminova.sock;
    }
}
```

2. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/adminova /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

3. **Configure SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Option 2: Docker Deployment

### Build and Run

1. **Build image**
```bash
docker build -t adminova:latest .
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

3. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Docker Production

For production, use docker-compose.prod.yml:

```yaml
version: '3.8'

services:
  web:
    image: adminova:latest
    command: gunicorn --bind 0.0.0.0:8000 --workers 3 adminova.wsgi:application
    env_file:
      - .env.production
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: always

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: adminova
      POSTGRES_USER: adminova
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    restart: always

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./staticfiles:/staticfiles:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
```

## Option 3: Platform Deployment

### Vercel (API Only)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
vercel --prod
```

Note: Configure environment variables in Vercel dashboard.

### Netlify (Static + Functions)

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Login and deploy**
```bash
netlify login
netlify deploy --prod
```

## Supabase Configuration

### Database Setup

1. **Create tables via Supabase Dashboard**
   - Go to SQL Editor
   - Run Django migrations SQL dump

2. **Configure connection**
```env
DB_HOST=brxiwidkpkmyqkbzdhht.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Airtel!23!23
DB_PORT=5432
```

## Post-Deployment

### 1. Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up firewall (UFW)
- [ ] Configure fail2ban
- [ ] Regular backups

### 2. Monitoring Setup

1. **Application logs**
```bash
sudo journalctl -u adminova -f
```

2. **Nginx logs**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Database Backups

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U adminova adminova > /backups/adminova_$DATE.sql
```

### 4. SSL Certificate Renewal

Certbot auto-renews. Test renewal:
```bash
sudo certbot renew --dry-run
```

## Maintenance

### Update Application

```bash
cd /home/adminova/adminova-django-dashboard
git pull origin main
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart adminova
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Clear Cache

```bash
python manage.py clearsessions
```

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u adminova -n 50
```

### Database connection issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U adminova -d adminova -h localhost
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

## Support

For deployment support, contact:
- Email: cavin.otieno012@gmail.com
- GitHub: https://github.com/OumaCavin/adminova-django-dashboard

## Deployment Tokens

Store these securely:
```env
VERCEL_TOKEN=fdHzM3Ra2jrdkOlc7rT84auM
NETLIFY_TOKEN=nfp_QSr9Vci3QZ1bL2CyNx6D1wJnMuKgEZfUc2d4
```
