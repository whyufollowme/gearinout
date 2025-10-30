GearInOut

A simple Ubuntu-based system for managing student camera gear.

GearInOut uses basic HTML and SQLite to provide a database where students can sign gear in and out. The system can be customized for your school or personal use.

⚠️ This repo won’t get frequent updates — only when I need to pull it to a device or reinstall it.

Installation

Run the installer with:

curl https://raw.githubusercontent.com/whyufollowme/gearinout/main/install_gearinout.sh | bash


This will:

Install Python3, Flask, Git, and SQLite if needed

Clone the GearInOut repo into /opt/gearinout

Set up the gearinout command to launch the system

Usage

After installation, start the app with:

gearinout


Then open a web browser on the same device and go to:

http://localhost:5000

Admin Dashboard

The system includes an admin dashboard protected by a password.

Demo password: 1234

Important: Change this immediately! 1234 is not safe for students.
to change it go under the app.py and it should be line #14

Notes

The local database lives under db/gear.db inside the app folder

Only one command (gearinout) is needed to start the system

if you are getting internal server errors when trying to add/remove items or edit stuff it will be a permisson based fix with the commands provied

command to enable writing:
sudo chmod 666 /opt/gearinout/database/gear.db

command to enable reading:
sudo chmod -R 777 /opt/gearinout/database
