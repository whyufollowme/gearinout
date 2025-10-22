#!/bin/bash
set -e

echo "📦 Installing GearInOut..."

# install dependencies
sudo apt update
sudo apt install -y python3 python3-flask git sqlite3

# clone or update repo
if [ ! -d "/opt/gearinout" ]; then
    sudo git clone https://github.com/whyufollowme/gearinout.git /opt/gearinout
else
    sudo git -C /opt/gearinout pull
fi

# create DB folder and placeholder DB
sudo mkdir -p /opt/gearinout/db
sudo chown -R $USER:$USER /opt/gearinout/db
if [ ! -f /opt/gearinout/db/gear.db ]; then
    sqlite3 /opt/gearinout/db/gear.db ".databases"
fi

# create launcher
sudo tee /usr/local/bin/gearinout > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/gearinout/app.py
EOF

sudo chmod +x /usr/local/bin/gearinout

echo "✅ Installed! Run with 'gearinout'"
