# pingsweep
Demonstration of Single Thread and Multi Thread Ping Sweeps

# Description
This was written for my own learning purposes.  It does a ping sweep.  

st.pingsweep.py - does single threaded (scans /24 in a few minutes)
mt.pingsweep.py - does multi threaded (scans /24 in about 2.5s)

It uses the ipaddress module so you can specify just about any CIDR you want.
From the CIDR specified it will:

* build a list of ip addresses to scan
* loop over that list, checking for specified timeout, unreachable or "Reply/bytes"
* sort final replies and print them
* give timed result and hosts found count

There are much better tools for this, but this oen taught me the basics of multi threading.

See screenshots for examples.