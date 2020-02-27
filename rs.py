import threading
import time
import random
import socket
import sys


def readFile():
    fh = open("PROJI-DNSRS.txt")

    for ln in fh:
        rec = ln.split(' ')
        if rec[2].endswith("NS") or rec[2].endswith("NS\n"):
            dict1["NS"] = (rec[0] + " " + rec[2])
            continue
        dict1[rec[0]] = (rec[0] + " " + rec[1] + " " + rec[2])
    fh.close()


def checkKey(k, dict1):
    for key in dict1:
        if k == key:
            print(dict1[key][0])
            return (dict1[key])
        else:
            if dict1[key][1] == 'NS\n':
                print(key, dict1[key])
                return (dict1[key])


def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    # server_binding = ('', 50007)
    server_binding = ('', int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))
    while 1:
        hn = csockid.recv(1024)
        hostname = hn.decode('utf-8')
        print(hostname)
        readFile()

        # Close the server socket
        if hostname is "end":
            ss.close()
            exit()

        # msg = checkKey(hostname, dict1)
        if dict1.get(hostname, "dne") == "dne":
            msg = dict1["NS"]
            print("ns")
        else:
            msg = dict1.get(hostname, "dne")
            print("found")

        csockid.send(msg.encode('utf-8'))





dict1 = {}
t1 = threading.Thread(name='rsServer', target=server)
t1.start()
