import socket

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
        #exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    rcs.connect(server_binding)

    # Receive data from the server
    data_from_server = rcs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    rcs.close()
    exit()