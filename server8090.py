import socket
import time
import threading

def server():
    thread_8090 = threading.Thread(target=spin_new_server, args=(8090,))
    thread_8090.start()

def spin_new_server(port = 8090):
    print("Server started at port: " + str(port))
    host = socket.gethostname()   # get local machine name
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        print('Received request at server running at port: ' + str(port))
        print(time.time())
        time.sleep(5)
        print(time.time())
        if not data:
            break
        print('From online user: ' + data)
        data = data.upper()
        print("server finished processing request")
        client_socket.send(data.encode('utf-8'))
    client_socket.close()

if __name__ == '__main__':
    server()