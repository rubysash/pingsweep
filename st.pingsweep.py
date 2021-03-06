# going to hide the windows spawned
import subprocess

# let's time our script
import time                 

# parse out the CIDR to a list
import ipaddress

# colors https://en.wikipedia.org/wiki/ANSI_escape_code
from colorama import init
init()

# Prompt the user to input a network address
net_addr = input("Enter Network (192.168.1.0/24): ")

# actual code start time
start = time.time()

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# For each IP address in the subnet, 
# run the ping command with subprocess.popen interface
# though it's much faster to use a small number like 15ms
# you'll miss hosts that take a long time on their response
count = 0
for i in range(len(all_hosts)):
    output = subprocess.Popen(['ping', '-n', '1', '-w', '300', 
        str(all_hosts[i])], stdout=subprocess.PIPE, 
        startupinfo=info).communicate()[0]
    
    # normalize colors
    print('\033[93m', end='')

    if "Destination host unreachable" in output.decode('utf-8'):
        print(str(all_hosts[i]), '\033[90m'+"is Offline (Unreachable)")
    elif "Request timed out" in output.decode('utf-8'):
        print(str(all_hosts[i]), '\033[90m'+"is Offline (Timeout)")
    else:
        # print colors in green if online
        print(str(all_hosts[i]), '\033[32m'+"is Online")
        count += 1


# normalize colors
print('\033[93m', end='')

# ok, give us a final time report to 2 decimal places
runtime = float("%0.2f" % (time.time() - start))
print(count, "hosts responded to ping in", runtime, "seconds")
