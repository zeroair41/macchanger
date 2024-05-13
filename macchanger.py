import subprocess
import sys
import requests
import time

def change_mac_address(mac_address):
    try:
        # Kill processes that might interfere with changing MAC address
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
        
        # Start monitor mode
        subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan0'], check=True)
        
        # Take down the interface
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'], check=True)
        
        # Change MAC address
        subprocess.run(['sudo', 'macchanger', '-m', mac_address, 'wlan0'], check=True)
        
        # Set interface mode to managed
        subprocess.run(['sudo', 'iwconfig', 'wlan0', 'mode', 'managed'], check=True)
        
        # Bring the interface back up
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'], check=True)
        
        # Restart NetworkManager service
        subprocess.run(['sudo', 'service', 'NetworkManager', 'start'], check=True)
        
        print("MAC address changed successfully!")
        
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        public_ip = response.text
        print("Your public IP address is:", public_ip)
    except requests.RequestException as e:
        print("Error occurred while fetching public IP:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <new_mac_address>")
    else:
        new_mac = sys.argv[1]
        change_mac_address(new_mac)
        print("Waiting for 15-30 seconds before checking internet connection...")
        time.sleep(15)  # Adjust the sleep time as needed
        get_public_ip()
