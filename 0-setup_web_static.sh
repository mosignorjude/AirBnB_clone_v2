#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static.
# - Install Nginx if it not already installed
# - Create the folder /data/web_static/releases/test/ if it doesn’t already exist
# - Create a fake HTML file /data/web_static/releases/test/index.html
# - Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# - Give ownership of the /data/ folder to the ubuntu user AND group
# - Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static

sudo apt update
# installs nginx if not installed.
if ! command -v nginx &> /dev/null; then
    sudo apt install nginx -y

fi

# create directories - gracefully handles if they already exist.
mkdir -p  /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# create index.html file in the directory with simple content.
echo "Holberton school" > /data/web_static/releases/test/index.html

# create a new symbolic link and delete any pre-existing link
link_name="/data/web_static/current"
target_path="/data/web_static/releases/test/"

if [ -L "$link_name" ]; then
    #deletes link if it already exists
    rm "$link_name"
fi

#create a symbolic link
ln -sf "$target_path" "$link_name"

# give ownership of /data folder to ubuntu
chown -R ubuntu /data
chgrp -R ubuntu /data

# updates server configuration
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://cuberule.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
