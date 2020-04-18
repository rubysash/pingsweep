import time       # let's time our script

import ipaddress  # https://docs.python.org/3/library/ipaddress.html
                  # convert ip/mask to list of hosts


import subprocess # https://docs.python.org/3/library/subprocess.html
                  # to make a popup window quiet

from colorama import init  # colors https://en.wikipedia.org/wiki/ANSI_escape_code
init()                     # https://pypi.org/project/colorama/


import threading           # for threading functions, lock, queue
from queue import Queue    # https://docs.python.org/3/library/queue.html

# define a lock that we can use later to keep
# prints from writing over itself
print_lock = threading.Lock()

# Prompt the user to input a network address
net_addr = input("Enter Network (192.168.1.0/24): ")

# actual code start time
startTime = time.time()

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# quick message/update
print ('Sweeping Network with ICMP: ', net_addr)

# the actual ping definition and logic.
# it's called from a pool, repeatedly threaded, not serial
def pingsweep(ip):
    
    # for windows:   -n is ping count, -w is wait (ms)
    # for linux: -c is ping count, -w is wait (ms)
    # the ping count must change if OS changes
    # fixme: code this to detect OS type

    # in practice, some computers on the local network took up to 300ms to respond.
    # If you set the timeout too low, you might get an incomplete response list
    output = subprocess.Popen(['ping', '-n', '1', '-w', 
      '1000', str(all_hosts[ip])], stdout=subprocess.PIPE, 
      startupinfo=info).communicate()[0]
    
    # lock this section, until we get a complete chunk
    # then free it (so it doesn't write all over itself)
    with print_lock:
      
      # normalize colors to grey
      print('\033[93m', end='')

      # code logic if we have/don't have good response
      if "Reply" in output.decode('utf-8'):
         print(str(all_hosts[ip]), '\033[32m'+"is Online")
      elif "Destination host unreachable" in output.decode('utf-8'):
         print(str(all_hosts[ip]), '\033[90m'+"is Offline (Unreachable)")
         pass
      elif "Request timed out" in output.decode('utf-8'):
         print(str(all_hosts[ip]), '\033[90m'+"is Offline (Timeout)")
         pass
      else:
         # print colors in green if online
         print("UNKNOWN", end='')

# defines a new ping using def pingsweep for each thread
# holds task until thread completes
def threader():
   while True:
      worker = q.get()
      pingsweep(worker)
      q.task_done()
      
q = Queue()

# up to 100 threads, daemon for cleaner shutdown   
# just spawns the threads and makes them daemon mode
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()

# loops over the last octet in our network object
# passing it to q.put (entering it into queue)
for worker in range(len(all_hosts)):
   q.put(worker)

# queue management   
q.join()

# ok, give us a final time report
runtime = float("%0.2f" % (time.time() - startTime))
print("Run Time: ", runtime, "seconds")
