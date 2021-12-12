# CSEC769 Project

## BLEPDoS

BLEPDoS is comprised of two denial of service attacks against Bluetooth LE (Low Power) that being BlueSmack and our novel attack, BlueChar, which is a deviation of the attack proposed in https://dl.acm.org/doi/pdf/10.1145/2851613.2851685 against Jawbone Health Trackers.

### BlueSmack
Three arguments: (string) target MAC (int) Number of Threads (int) Packet Size

BlueSmack attack is a type of 'ping attack' which involves swarming the slave Bluetooth LE device with a large number of L2CAP echo requests to temporarily disable the slave device from connecting.

This attack is carried out using l2ping.

### BlueChar
One argument: (string) target MAC (int) Number of Processes

BlueChar attack is an undocumented type of attack (which we decidedly named BlueChar) which involves swarming the slave Bluetooth LE connection with read characteristics in multiple processes utilizing the same bluetoothctl wrapper.  NOTE: This deviates from the 'sending multiple connection requests and read characteristics' since there is only one connection being formed.  


## How does it Work?
We abuse the peripheral bluetooth controller's fault in that it does not timeout connections formed with attacker after an extended period of time despite not being paired.  Funny enough the bluetooth controller appears to have such a timeout capability if there is no ongoing communication for 10 seconds or more.  We recommend bluetooth chipset manufacturers to implement the timeout to apply to ongoing communicating devices that aren't paired or at the very least provide this secuirty option to mitigate availability attacks.


Some Issues:
It appears that bluetoothctl has a large delay in forming connections and disconnects making it not suitable for avaliability attacks.  The tool connects directly to the controller making multiple syncrhonous connections difficult and slow.  Since gattool is depreciated we can no longer utilize it's quick connection with randomized MACs.

## Bluetoothctl Wrapper
BOTH attacks are carried out using a bluetoothctl wrapper based on Dan castis's pexpect design https://gist.github.com/castis/0b7a162995d0b465ba9c84728e60ec01.  I introduce new functions to the wrapper for parts of the GATT menu and make modifications on current functions to fit the needs 


## Dependencies
Device should be using BlueZ Bluetooth Protocol Stack (MOST LINUX BASED SYSTEMS)

Python3.6.8 or above

## Setting Up Vulnerable Raspberry PI(VICTIM) for BlueSmack Attack
    bluetoothctl
    discoverable on # Note if you take too long, you will need to do this again

## Setting Up Vulnerable Raspberry PI(VICTIM) for BlueChar Attack
    bluetoothctl
    advertise off
    advertise peripheral
    discoverable on # Note if you take too long, you will need to do this again
    
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
    sys.argv[3]: Thread/Process Number
    sys.argv[4]: Packet size
