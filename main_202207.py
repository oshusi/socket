import socket
# import select    # For multi-client server sockets.
import time
# import concurrent.futures    # For thread processing.
import netifaces as ni    # For get ethX ip address
import os   # For fork().
import sys

ETH_NAME = 'ens33'

def make_socket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create server sockets.
    sock.bind((ip,port))    # Bind server sockets.
    sock.listen(16)    # Listen server sockets.
    #sock.setblocking(False)    # Put sockets in non-blocking mode.
    print (f"[{os.getpid()}][*] Server is listening at {ip}:{port}") 
    return sock

def accept_loop(_sock):
    while True:
        conn, address = _sock.accept()

        pid = os.fork()
        if pid == 0:
            #_sock.close()
            print(f"[PID:{os.getpid()}(child)]:recv")
            time.sleep(10)
            conn.close()
            sys.exit()
        elif pid > 0:
            print(f"[PID:{os.getpid()}][child:{pid}]Accept:{address} -> {_sock.getsockname()} ")
            conn.close()
        else:
            conn.close()

def main():
    timeout = 10
    _readers = list()
    ni.ifaddresses(ETH_NAME)
    ip = ni.ifaddresses(ETH_NAME)[ni.AF_INET][0]['addr']
    ports = [23]
    #ports = [23,80,2323,8080,10080]
    #ports = list(range(1,1023))

    for port in ports:
        sock = make_socket(ip,port)
        try:
            accept_loop(sock)
        except KeyboardInterrupt:
            sock.close()

if __name__ == '__main__':
    main()
