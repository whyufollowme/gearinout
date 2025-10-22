#!/bin/bash
set -e

echo "📦 Installing GearInOut..."

sudo apt update
sudo apt install -y python3 python3-flask git

if [ ! -d "/opt/gearinout" ]; then
    sudo git clone https://github.com/whyufollowme/gearinout.git /opt/gearinout
else
    sudo git -C /opt/gearinout pull
fi

sudo tee /usr/local/bin/gearinout > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/gearinout/app.py
EOF

sudo chmod +x /usr/local/bin/gearinout

echo "✅ Installed! Run with 'gearinout'"
