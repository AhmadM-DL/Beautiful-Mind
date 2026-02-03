#!/bin/bash

# 1. Copy temp config to live config
echo "Using temporary Nginx configuration..."
cp ./nginx/nginx.temp.conf ./nginx/nginx.conf

# 2. Run Nginx
echo "Starting Nginx..."
docker compose up -d nginx

# 3. Run Certbot
echo "Requesting SSL certificate..."
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ \
    --email ahmad.m.mustapha@hotmail.com --agree-tos --no-eff-email \
    -d beautifulmind.health

# 4. Copy main config to live config
echo "Switching to main Nginx configuration..."
cp ./nginx/nginx.main.conf ./nginx/nginx.conf

# 5. Docker down
echo "Stopping all services..."
docker compose down

echo "Done! You can now run 'docker compose up -d' to start the full stack with SSL."
