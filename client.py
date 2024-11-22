import socket
import threading
import os
import time
from ssl import socket_error

class bcolors:
	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	WHITE = '\033[0m'



username = ''
roomnames = []
roomaddrs = []
color = bcolors.WHITE
stopcom = False
kill = False

def printart():
    print('\033[92m' + r' _______  _        _______  _______  _______     _______           _______ _________', '\n'
          r'(  ____ \( \      (  ___  )(  ____ \(  ____ \   (  ____ \|\     /|(  ___  )\__   __/', '\n'
          r'| (    \/| (      | (   ) || (    \/| (    \/   | (    \/| )   ( || (   ) |   ) (   ', '\n'
          r'| |      | |      | (___) || (_____ | (_____    | |      | (___) || (___) |   | |   ', '\n'
          r'| |      | |      |  ___  |(_____  )(_____  )   | |      |  ___  ||  ___  |   | |   ', '\n'
          r'| |      | |      | (   ) |      ) |      ) |   | |      | (   ) || (   ) |   | |   ', '\n'
          r'| (____/\| (____/\| )   ( |/\____) |/\____) |   | (____/\| )   ( || )   ( |   | |   ', '\n'
          r'(_______/(_______/|/     \|\_______)\_______)   (_______/|/     \||/     \|   )_(   ', '\n'
          '                       (client edition v0.3 made by j-bom)                        ')

def discover(port):
    global roomnames
    global roomaddrs
    ip = socket.gethostbyname(socket.gethostname())
    split = ip.split('.')
    newip = '.'.join(split[:3])
    for i in range(1,225):
        tocheck = f'{newip}.{i}'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect((tocheck,port))
            s.recv(3)
            s.settimeout(300)
            s.send('DIS'.encode())
            name = s.recv(1024).decode()
            s.close()
            roomaddrs.append(tocheck)
            roomnames.append(name)
        except socket_error as err:
            s.close()

def recive(s):
    global color
    global stopcom
    global username
    while True:
        if stopcom:
            break
        try:
            msg = s.recv(1024).decode()
            if msg != '':
                splitted = msg.split()
                if len(splitted) > 1:
                    if splitted[1] != username:
                        formatted = ''
                        for i in range(2,len(splitted)):
                            formatted += splitted[i] + ' '
                        print(f'\n\n{splitted[0]}{splitted[1]}:> {formatted}\n{color}\n:>', end='')
        except socket_error as err:
            print(f'an error occured. here are the details: {err}')
            s.close()
            break

def write(s):
    global  kill
    global color
    global  stopcom
    global username
    while True:
        if stopcom:
            break
        data = input(f'{color}')
        print(f'{color}:>',end='')
        if data != '':
            if data != 'quit':
                splitted = data.split()
                if splitted[0] == '/HELP':
                    if len(splitted) > 1:
                        if splitted[1] == '/COLOR':
                            print('\n\033[92msystem:> /COLOR (color here) \n'
                                  '\033[95mPURPLE\n'                            
                                  '\033[94mBLUE\n'
                                  '\033[96mCYAN\n'
                                  '\033[92mGREEN\n'
                                  '\033[93mYELLOW\n'
                                  '\033[91mRED\n'
                                  '\033[0mWHITE\n')
                    else:
                        print('\n\033[92msystem:> help menu:\n'
                            '/COLOR - lets you change the color of your messages\n'
                            '\nmore commands to come if i wanna keep working on this project\n')
                    print(f'{color}:>', end='')
                else:
                    if splitted[0] == '/COLOR':
                        try:
                            color = getattr(bcolors,splitted[1])
                        except:
                            print('no such color')
                        data = ''
                        for i in range(2, len(splitted)):
                            data += splitted[i] + " "
                    tosend = f'{color} {username} {data}'
                    s.send(tosend.encode())
            else:
                s.send('QUT'.encode())
                answer = input('\nwould you like to return to the menu? (Y/N): ').lower()
                print(answer)
                color = bcolors.WHITE
                if answer == 'n':
                    kill = True
                stopcom = True

def main():
    global kill
    global username
    global stopcom
    global roomnames
    global roomaddrs
    port = 6969

    while not kill:
        os.system('cls')
        stopcom = False
        roomnames = []
        roomaddrs = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        printart()
        username = input('\nplease enter a username: ')
        print('scanning for active rooms...')
        discover(port)

        print('*****************************************************************************\n' * 2)
        for i in range(len(roomnames)):
            print(f'{i+ 1}. {roomnames[i]} on {roomaddrs[i]}\n')
        print('*****************************************************************************\n' * 2)

        print('\nwhich room would you like to connect to: ', end='')
        choice = input()
        s.connect((roomaddrs[int(choice) - 1], port))
        s.settimeout(300)
        s.send('JON'.encode())
        s.send(username.encode())

        print(f'\nsystem:> welcome to {roomnames[int(choice) - 1]}! enjoy your time :)')
        print('system:> type quit to leave or /HELP for help')
        print(f'{color}:>',end='')
        rt = threading.Thread(target=recive, args=(s,))
        rt.start()
        wt = threading.Thread(target=write,args=(s,))
        wt.start()
        rt.join()
        wt.join()
        time.sleep(0.3)
        s.close()

if __name__ == '__main__':
    main()
