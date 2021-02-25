# The PyPhone - Voice and SMS/MMS on a Raspberry Pi 3B+

Effective communication with minimal dependencies.  The PyPhone is open source software, using open protocols (https and sip) and running on (fairly) open hardware. No Apple ID, No Google Account, No SIM, no AdSense, no Apps, no Ads, no GPS, no Sensors.

## Motivation
I do not like the concessions required today for voice/sms.  So I built my own, from scratch, for myself.  Now I want to share this with like minded privacy concious professionals.

## About Me
I am a solo founder, a 25 year veteran of the software industry and a passionate digital privacy advocate.

## Intended Audience
Software professionals with Raspberry Pi and Linux experience.  Bash and Python 3 experience required. 

## Hardware Requirements
* Raspberry Pi 3B+ with an official 7" Touch Screen
* Logitech USB H390 Headset
* Ethernet cable (Wi-Fi works too)

## Get Calling
### Get the Installer
Free, no credit card required
https://myphone2020-1.weebly.com/account-request.html
After successful account creation, you will get a link to download the thepyphone.tar.gz which contains the fully configured PyPhone software.  Copy the installer into the home directory on the pi (/home/pi)
### Install The PyPhone
* $ cd ~
* $ pip3 install thepyphone.tar.gz --user
* $ cd pyphone
*  ./pi_run_pyphone.sh
## Demos of the PyPhone
| Task | Link |
| --- | --- |
| Installation | www.youtube.com |
| Start up | www.youtube.com |
| Make a voice call | www.youtube.com |
| Send an SMS | www.youtube.com |
| Send an MMS | www.youtube.com |
| Receive a voice call | www.youtube.com |
| Receive an SMS/MMS | www.youtube.com |
## Common Use Cases
* Dedicated home phone.  Only give your number to your closest friends.
* Dedicated 2FA phone. No SIM, so SIM jacking is not possible.
* Dedicated business line.  Compartmentalize your personal and business personas.
## Network
The PyPhone works over Ethernet or Wi-Fi.  I prefer Ethernet, if you use Ethernet then you can power off the Wi-Fi radio.
## VNC Friendly
The PyPhone works great over VNC.  I typically connect from my Desktop to the PyPhone.  A side benefit of this is I can type my SMS on my Desktop keyboard.  I can type far faster on a full size keyboard than on a mobile phone keyboard.
## Code Status
Production stable.  I use this as my daily driver and I have for over a year.  I reboot the phone every few months.
## International Usage
The PyPhone has been tested and confirmed to work in multiple contintents including North and South America and Europe. I used it to do to my US business while I was abroad.  The PyPhone appears to be physically located in the United States no matter where you are located in the world.
## The Code
The code is Python 3 (with a bunch of packages from PyPy) and GTK. 
