## CSEC769 Project

## BLEPDoS

BLEPDoS is comprised of two denial of service attacks against Bluetooth LE (Low Power) that being Bluessmack and a reinvented attack found in the paper https://dl.acm.org/doi/pdf/10.1145/2851613.2851685.

### BlueSmack
Three arguments: (string) target MAC (int) Thread Number (int) Packet Size
BlueSmack attack is a type of 'ping attack' which involves swarming the slave Bluetooth LE device with a large number of L2CAP echo requests to temporarily disable the slave device from connecting.

This attack is carried out using the l2ping tool

### BlueChar
One argument: (string) target MAC
BlueChar attack is a mostly undocumented type of attack which involves swarming the slave Bluetooth LE

## Depenedencies
Device should be using BlueZ Bluetooth Protocol Stack
Python3.6.8 or above

## Install
git clone https://github.com/spk3077/BLEPDoS

## Running
Requires ROOT PRIV

sudo python3 BLEPDOS.py (optional arguments)

    sys.argv[1]: target <Device Name/MAC Address>
    sys.argv[2]: Attack Type <1 (pairing)  /  2 (l2ping)>
    sys.argv[3]: Thread Number
    sys.argv[4]: packet size
