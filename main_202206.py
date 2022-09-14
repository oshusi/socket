#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import socket
import select # For multi-client server sockets.
import time
import concurrent.futures # For thread processing.

def make_socket(ip,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create server sockets.
  sock.bind((ip,port)) # Bind server sockets.
  sock.listen(16) # Listen server sockets.
  sock.setblocking(False) # Put sockets in non-blocking mode.
  print (f"[*] Server is listening at {ip}:{port}")
  return sock

def recv(_client_sock):
  conn, address = _client_sock.accept() # Accept connection.
  buf_size = 65536
  # When the request is received, the client address (source ip address and source port) and request data are displayed.
  try:
    time.sleep(1)
    data = conn.recv(buf_size) # もしかしたら不要？要評価　★不要（詳細は次ページ）
    print(f"socket is {_client_sock.getsockname()}")
    print(f"accept {address},{data}")  except:    pass  conn.close()
    def main():
      timeout = 10
      _readers = list()
      ip = “0.0.0.0” # NICの中のIPアドレス１つだけ指定すること　★解決
      ports = [23,80,2323,8080,10080]
      for port in ports:
        sock = make_socket(ip,port)
        _readers.append(sock)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        while True:
          _read, _, _ = select.select(_readers,[],[],timeout)
          if len(_read) == 0:
            print("select:timeout")
            continue
           // FORKする　★未解決
          for _client_sock in _read:
            executor.submit(recv,_client_sock)
            
if __name__ == '__main__’:
  main()

