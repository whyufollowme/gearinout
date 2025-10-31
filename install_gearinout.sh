#!/bin/bash
set -e

echo "📦 Installing GearInOut..."

# --- Install dependencies ---
sudo apt update
sudo apt install -y python3 python3-flask git sqlite3

# --- Clone or update repo ---
if [ ! -d "/opt/gearinout" ]; then
    sudo git clone https://github.com/whyufollowme/gearinout.git /opt/gearinout
else
    sudo git -C /opt/gearinout pull
fi

# --- Create database folder and placeholder DB ---
sudo mkdir -p /opt/gearinout/database
sudo chown -R $USER:$USER /opt/gearinout/database

if [ ! -f /opt/gearinout/database/gear.db ]; then
    sqlite3 /opt/gearinout/database/gear.db ".databases"
fi

# --- Set permissions for reading/writing ---
sudo chmod 666 /opt/gearinout/database/gear.db
sudo chmod -R 777 /opt/gearinout/database

# --- Create launcher ---
sudo tee /usr/local/bin/gearinout > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/gearinout/app.py
EOF

sudo chmod +x /usr/local/bin/gearinout

echo "✅ Installed! Run with 'gearinout'"#!/bin/bash
set -e

echo "📦 Installing GearInOut..."

# --- Install dependencies ---
sudo apt update
sudo apt install -y python3 python3-flask git sqlite3

# --- Clone or update repo ---
if [ ! -d "/opt/gearinout" ]; then
    sudo git clone https://github.com/whyufollowme/gearinout.git /opt/gearinout
else
    sudo git -C /opt/gearinout pull
fi

# --- Create database folder and placeholder DB ---
sudo mkdir -p /opt/gearinout/database
sudo chown -R $USER:$USER /opt/gearinout/database

if [ ! -f /opt/gearinout/database/gear.db ]; then
    sqlite3 /opt/gearinout/database/gear.db ".databases"
fi

# --- Set permissions for reading/writing ---
sudo chmod 666 /opt/gearinout/database/gear.db
sudo chmod -R 777 /opt/gearinout/database

# --- Create launcher ---
sudo tee /usr/local/bin/gearinout > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/gearinout/app.py
EOF

sudo chmod +x /usr/local/bin/gearinout

echo "✅ Installed! Run with 'gearinout'"
#!/bin/bash
set -e

echo "📦 Installing GearInOut..."

# --- Install dependencies ---
sudo apt update
sudo apt install -y python3 python3-flask git sqlite3

# --- Clone or update repo ---
if [ ! -d "/opt/gearinout" ]; then
    sudo git clone https://github.com/whyufollowme/gearinout.git /opt/gearinout
else
    sudo git -C /opt/gearinout pull
fi

# --- Create database folder and placeholder DB ---
sudo mkdir -p /opt/gearinout/database
sudo chown -R $USER:$USER /opt/gearinout/database

if [ ! -f /opt/gearinout/database/gear.db ]; then
    sqlite3 /opt/gearinout/database/gear.db ".databases"
fi

# --- Set permissions for reading/writing ---
sudo chmod 666 /opt/gearinout/database/gear.db
sudo chmod -R 777 /opt/gearinout/database

# --- Create launcher ---
sudo tee /usr/local/bin/gearinout > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/gearinout/app.py
EOF

sudo chmod +x /usr/local/bin/gearinout

echo "✅ Installed! Run with 'gearinout'"
