# The PyPhone - Voice and SMS/MMS on a Raspberry Pi 3B+

Effective communication with minimal dependencies.  The PyPhone is open source software, using open protocols (https and sip) and running on (fairly) open hardware. No Apple ID, No Google Account, No SIM, no AdSense, no Apps, no Ads, no GPS, no Sensors.

## Motivation
I do not like the concessions required today just for voice/sms.  So I built my own, from scratch, for myself.  Now I want to share this with like minded privacy concious professionals.

## About Me
I am a solo founder, a 25 year veteran of the software industry and a passionate digital privacy advocate. <br />
I use Linux exclusively.  I do not use Windows or OSX.

## Intended Audience
Ethical software professionals with Raspberry Pi, Linux, Bash and Python 3 experience. <br />
I don't want this to be used by scammers or other bad people for shady things.

## Hardware Requirements
* <a href="https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/dp/B07P4LSDYV/">Raspberry Pi 3B+</a> with an <a href="https://www.amazon.com/Raspberry-Pi-7-Touchscreen-Display/dp/B0153R2A9I/">official 7" Touch Screen</a>
* <a href="https://www.amazon.com/Logitech-Headset-H390-Noise-Cancelling/dp/B000UXZQ42">Logitech USB H390 Headset</a>
* Ethernet cable (Wi-Fi works too)

## Get Calling
Prerequisite: a fully updated, Internet connected Raspberry Pi 3B+.  Ethernet or Wi-Fi is fine.
### Get the Installer
Sign up for an account <a href="https://myphone2020-1.weebly.com/account-request.html">here</a>. It's a simple form, it's free, and there is no credit card required.  I'm a solo founder, and the actual account setup process is manual so please be patient.
 <br />
After successful account creation, you will get a link to download the thepyphone.tar.gz which contains the fully configured PyPhone software.  Copy the installer into the home directory on the pi (/home/pi)
### Install The PyPhone
cd ~ <br />
$ ./pi_install_pyphone  <br />
### Run The PyPhone
$ cd ~/pyphone  <br />
./pi_run_pyphone.sh <br />
## Demos of the PyPhone
Notes <br />
* I am a color blind engineer with minimal gui/video skills.  I build rock solid stuff that works forever, but I'm not great at making it pretty.  Please be kind :)
* No audio (yet) on any of these videos.
* All these demos use live phone numbers, so I blanked out the phone numbers so I don't dox myself.

| Task | Link |
| --- | --- |
| Installation and Start Up | https://youtu.be/5rWnr3jHFWQ |
| Make a voice call | https://youtu.be/IpL6BD8mGHA |
| Send an SMS | https://youtu.be/gVFxhu5gdkY |
| Send an MMS |  https://youtu.be/_ZHxHS4RqPo |
| Receive a voice call | https://youtu.be/nz82aCpR8q4 |
| Receive an SMS/MMS | https://youtu.be/YIqjVNbaYEE |

## Potential Use Cases
* Dedicated home phone.  Only give your number to your closest friends.
* Dedicated 2FA phone. No SIM, so SIM jacking is not possible.
* Dedicated business line.  Compartmentalize your personal and business personas.
## VNC Friendly
The PyPhone works great over VNC.  I typically connect from my Ubuntu Desktop to the PyPhone.  A side benefit of this is I can type my SMS on my Desktop keyboard.  I can type far faster on a full size keyboard than on a mobile phone keyboard.
## Code Status
Production stable.  I use this as my daily driver and I have for over a year.
## International Usage
The PyPhone has been tested and confirmed to work in multiple contintents including North and South America and Europe. I used it to do to my US business while I was abroad.  The PyPhone appears to be physically located in the United States no matter where you are located in the world.
## The Code
The code is Python 3 (with a bunch of packages from PyPy) and GTK. 
