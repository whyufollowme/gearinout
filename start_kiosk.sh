#!/bin/bash
cd /home/gear-kiosk/app
source venv/bin/activate

# Start Flask in background
python3 app.py &

# Give Flask a couple of seconds to start
sleep 2

# Start Firefox in kiosk mode in foreground
firefox --kiosk http://127.0.0.1:5000

