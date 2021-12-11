# CSEC769 Project

## BLEPDoS

BLEPDoS is comprised of two denial of service attacks against Bluetooth LE (Low Power) that being BlueSmack and our reinvented attack, BlueChar, found in the paper https://dl.acm.org/doi/pdf/10.1145/2851613.2851685.

### BlueSmack
Three arguments: (string) target MAC (int) Number of Threads (int) Packet Size

BlueSmack attack is a type of 'ping attack' which involves swarming the slave Bluetooth LE device with a large number of L2CAP echo requests to temporarily disable the slave device from connecting.

This attack is carried out using l2ping.

### BlueChar
One argument: (string) target MAC (int) Number of Processes

BlueChar attack is an undocumented type of attack (which we decidedly named BlueChar) which involves swarming the slave Bluetooth LE with connection and read characteristics.

This attack is carried out using a bluetoothctl wrapper based on Egor Fedorov's with improvements expanding slightly to parts of the GATT menu.

## Dependencies
Device should be using BlueZ Bluetooth Protocol Stack

Python3.6.8 or above

## Install
git clone https://github.com/spk3077/BLEPDoS

## Running
```diff
- Usually requires multiple CTRL-C to Full Exit (Work In Progress Fix)
```
Requires ROOT PRIV

sudo python3 BLEPDOS.py (optional arguments)

    sys.argv[1]: target <Device Name/MAC Address>
    sys.argv[2]: Attack Type <1 (pairing)  /  2 (l2ping)>
    sys.argv[3]: Thread Number
    sys.argv[4]: Packet size
