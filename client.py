import socket
import threading
import time


def connectTs():
    try:
        tcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
    port = 50008
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    tcs.connect(server_binding)
    return tcs


def client():
    try:
        rcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        # exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    rcs.connect(server_binding)

    with open('PROJI-HNS.txt') as f:
        lines = f.readlines()

    print(lines)

    f = open("RESOLVED.txt", "w")
    for line in lines:
        rcs.send(line.strip("\n").encode('utf-8'))

        time.sleep(1.5)

        data_from_server = rcs.recv(1024)
        d = data_from_server.decode('utf-8')
        if d.endswith("A") or d.endswith("A\n"):
            time.sleep(1.5)
            print("[C]: Data matched in RS table and received from server:", d)
            f.write(d)
        elif d.endswith("N") or d.endswith("N\n"):
            time.sleep(1.5)
            print("[C]: No match found in RS table, data ends with NS", d)
            connectTS = connectTs()

            connectTS.send(line.strip("\n").encode('utf-8'))
            time.sleep(1.5)

            data_from_ts_server = connectTS.recv(1024)
            m = data_from_ts_server.decode('utf-8')
            if m.endswith("A") or m.endswith("A\n"):
                print("[C]: Data matched in TS table and received from server", m)
                f.write(m)
            else:
                print("[C]: Hostname - error: HOST NOT FOUND", m)
                f.write(m)

    f.close()
    rcs.close()
    exit()


t2 = threading.Thread(name='client', target='client')
t2.start()
input("hit ENTER to exit")

exit()
