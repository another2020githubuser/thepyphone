# The PyPhone - Voice and SMS/MMS on a Raspberry Pi 3B+

Effective communication with minimal dependencies.  The PyPhone is open source software, using open protocols (https and sip) and running on (fairly) open hardware. No Apple ID, No Google Account, No SIM, no AdSense, no Apps, no Ads.

## Hardware Requirements
* Raspberry Pi 3B+ with an official 7" Touch Screen
* Logitech USB H390 Headset
* Ethernet cable

## Installation
```python
pip3 install thepyphone
```
## Configuration
Get an account
https://www.thepyphone.com/getaccount

Start the PyPhone
```
cd pyphone
./pi_run_pyphone
```
Enter your credentials and start calling

## Demos
Task | Link
---------
Start up | www.youtube.com
Make a voice call | www.youtube.com
Send an SMS | www.youtube.com
Receive a voice call | www.youtube.com
## Possible Use Cases
Dedicated home phone.  Only give your number to your closest friends.
Dedicated 2FA phone. No SIM jacking.
Dedicated business line.  Compartmentalize your personal and business personas.
## Network
The PyPhone works over Ethernet or Wi-Fi.  I prefer Ethernet, if you use Ethernet then you can power off the Wi-Fi radio.
## Code Status
Production stable.  I use this as my daily driver and I have for over a year.  I reboot the phone every few months.
## International Usage
The PyPhone has been tested and confirmed to work in multiple contintents including North and South America and Europe. I used it to do to my US business while I was abroad.
## Extra
If you like your cell phone, you can keep your cell phone
Built backwards, I built this for myself first, so no barely working MVP here.  This is  stable code that I use as my daily driver.
All you need is a Raspberry 3B+ with touchscreen, a Logitech USB H390 Headset an ethernet cable and a PyPhone account.  
My vision is to re-think and de-centralize communication, from both a hardware and software perspective.  Security and privacy are really important to me, but the current trends are toward closed source, proprietary devices, less private platforms etc.  The PyPhone is in many ways a 21st century home phone.

Start with a 21st century home phone with a touch screen.  Make the home phone the always on hub of your communications.  Use a mobile phone when necessary.  This simp
## The Code
The code is Python 3 (with a bunch of packages from PyPy) and GTK. 
