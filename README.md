## BLEPDoS
CSEC769 Project
Requires ROOT PRIV

## Depenedencies
sudo apt-get install python3-pip libglib2.0-dev

sudo pip3 install bluepy

## Install
git clone should do the trick!

## Running
python3 BLEPDOS.py (optional arguments)

    sys.argv[1]: target <Device Name/MAC Address>
    sys.argv[2]: Attack Type <1 (pairing)  /  2 (l2ping)>
    sys.argv[3]: Thread Number
    sys.argv[4]: packet size
