import socket
import threading
import time
import sys


def connectTs(host):
    try:
        tcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
    tsListenPort = int(sys.argv[3])
    port = tsListenPort
    localhost_addr = socket.gethostbyname(host)

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    print(localhost_addr)
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
    rsListenPort = int(sys.argv[2])
    port = rsListenPort
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    rcs.connect(server_binding)

    hostlist = sys.argv[1]
    with open(hostlist) as f:
        lines = f.readlines()

    #print(lines)

    f = open("RESOLVED.txt", "w+")

    time.sleep(1.5)

    connectTS = 0

    for line in lines:
        line = line.lower()

        # send to RS
        rcs.send(line.strip("\n").encode('utf-8'))

        data_from_server = rcs.recv(1024)
        d = data_from_server.decode('utf-8')
        print('works', d)
        if d.endswith("A") or d.endswith("A\n"):
            time.sleep(1.5)
            print("[C]: Data matched in RS table and received from server:", d)
            f.write(d)
        elif d.endswith("NS") or d.endswith("NS\n"):
            time.sleep(1.5)
            print("[C]: No match found in RS table, data ends with NS")
            host = d.split(' ')
            # send to TS
            if connectTS == 0:
                print(host[0])
                connectTS = connectTs(host[0])

            connectTS.send(line.strip("\n").encode('utf-8'))
            time.sleep(1.5)

            data_from_ts_server = connectTS.recv(1024)
            m = data_from_ts_server.decode('utf-8')
            if m.endswith("A") or m.endswith("A\n"):
                print("[C]: Data matched in TS table and received from server")
                f.write(m)
            else:
                print("[C]: Hostname - error: HOST NOT FOUND")
                f.write(m)

    rcs.send("end".encode('utf-8'))
    if connectTS != 0:
        connectTS.send("end".encode('utf-8'))
    f.close()
    rcs.close()
    exit()


t2 = threading.Thread(name='client', target=client)
t2.start()

time.sleep(5)
# input("hit ENTER to exit")

exit()
