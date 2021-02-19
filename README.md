# The PyPhone
Voice and SMS/MMS on a Raspberry Pi 3B+

Simple communication with minimal dependencies.  **All you need is a Raspberry 3B+ with touchscreen, a Logitech USB H390 Headset an ethernet cable and a PyPhone account.**  No Apple ID, No Google Account, No SIM, nothing else required.  The PyPhone is open source software, using open protocols (https and sip) and running on fairly open hardware.  

My vision is to re-think and de-centralize communication, from both a hardware and software perspective.  Security and privacy are really important to me, but the current trends are toward closed source, proprietary devices, less private platforms etc.  The PyPhone is in many ways a 21st century home phone.

Start with a 21st century home phone with a touch screen.  Make the home phone the always on hub of your communications.  Use a mobile phone when necessary.  This simp

Use the PyPhone as a home phone.  Only give your number to your closest friends.
Use the PyPhone as a dedicated 2FA phone.  

Works fine over Wi-Fi.  Tested in multiple contintents including North and South America and Europe.  Works fine. The phone appeared to be a US phone.

Not encrypted.  Everything you say or type will end up transmitted plain text over the public Internet.  Don't use this for illegal stuff.

The code is Python 3 (with a bunch of packages from PyPy) and GTK.  Built backwards, I built this for myself first, so no barely working MVP here.  This is  stable code that I use as my daily driver.

## Installation
pip3 install thepyphone


