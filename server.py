import threading
import socket
import os

clients = []
usernames = []

def printart():
    print('\033[92m' + r' _______  _        _______  _______  _______     _______           _______ _________', '\n'
          r'(  ____ \( \      (  ___  )(  ____ \(  ____ \   (  ____ \|\     /|(  ___  )\__   __/', '\n'
          r'| (    \/| (      | (   ) || (    \/| (    \/   | (    \/| )   ( || (   ) |   ) (   ', '\n'
          r'| |      | |      | (___) || (_____ | (_____    | |      | (___) || (___) |   | |   ', '\n'
          r'| |      | |      |  ___  |(_____  )(_____  )   | |      |  ___  ||  ___  |   | |   ', '\n'
          r'| |      | |      | (   ) |      ) |      ) |   | |      | (   ) || (   ) |   | |   ', '\n'
          r'| (____/\| (____/\| )   ( |/\____) |/\____) |   | (____/\| )   ( || )   ( |   | |   ', '\n'
          r'(_______/(_______/|/     \|\_______)\_______)   (_______/|/     \||/     \|   )_(   ', '\n'
          '                       (server edition v0.3 made by j-bom)                        ')



def passmsg(data):
    for i in clients:
        i.send(data)

def recive(c):
    while True:
        try:
            msg = c.recv(1024)
            if msg.decode() != 'QUT' and msg.decode != '':
                passmsg(msg)
            else:
                if c in clients:
                    rip = usernames[clients.index(c)]
                    clients.remove(c)
                    c.close()
                    usernames.remove(rip)
                    passmsg(f'\033[92m system {rip} had left'.encode())
                    break
        except socket.error as err:
            if c in clients:
                rip = clients.index(c)
                clients.remove(c)
                passmsg(f'\033[92m system {usernames[rip]} had left'.encode())
                usernames.remove(rip)
                c.close()
                break



def main():
    host = '0.0.0.0'
    port = 6969
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    os.system('cls')
    printart()
    print(socket.gethostbyname(socket.gethostname()))
    roomname = input('\nplease enter the name for your room: ')

    s.bind((host,port))
    s.listen(5)
    print('\033[92m system:> server is online.')

    while True:
        (c, addr) = s.accept()
        print(f'accepted {addr}')
        c.send('hi'.encode())
        willjoin = c.recv(3).decode()
        if willjoin == 'JON':
            name = c.recv(1024).decode()

            print(f'new conneciton from {addr} as {name}')
            passmsg(f'\033[92m system {name} had joined us!'.encode())
            usernames.append(name)
            clients.append(c)

            t = threading.Thread(target=recive, args=(c,))
            t.start()

        elif willjoin == 'DIS':
            c.send(roomname.encode())
            c.close()

if __name__ == '__main__':
    main()