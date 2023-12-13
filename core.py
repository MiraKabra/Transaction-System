import socket
import time

user_map = {}
country_map = {}


user_map[0] = "Juian"
user_map[1] = "Katherine"
user_map[2] = "Michael"
user_map[3] = "Tiffany"
user_map[4] = "Vincent"
user_map[5] = "Kevin"

user_map[6] = "Ria"
user_map[7] = "Jesse"
user_map[8] = "Amanda"
user_map[9] = "Sarah"
user_map[10] = "John"

user_map[11] = "Nathan"
user_map[12] = "Jacob"
user_map[13] = "Andrew"
user_map[14] = "Joshua"

country_map[0] = "Europe"
country_map[1] = "Europe"
country_map[2] = "Europe"
country_map[3] = "Europe"
country_map[4] = "Europe"
country_map[5] = "Europe"

country_map[6] = "West Coast"
country_map[7] = "West Coast"
country_map[8] = "West Coast"
country_map[9] = "West Coast"
country_map[10] = "West Coast"


country_map[11] = "East Coast"
country_map[12] = "East Coast"
country_map[13] = "East Coast"
country_map[14] = "East Coast"

ports = {"Europe": 8080, "West Coast": 8085, "East Coast": 8090}

def client(port=8080):
  host = socket.gethostname()  # get local machine name
  s = socket.socket()
  print("before connection " + str(port))
  s.connect((host, port))
  print("after connection " + str(port))
  return s

def send(s, message):
    s.send(message.encode('utf-8'))
    print('Sent to server: ' + message)
    print(time.time())

def sendWithRecv(s, message):
    start = time.time()
    s.send(message.encode('utf-8'))
    print('Sent to server: ' + message)
    data = s.recv(1024).decode('utf-8')
    end = time.time()
    print('Received from server: ' + data)
    print(time.time())
    return end - start, data

# def close_conn(s):
#     s.close()

if __name__ == '__main__':
  client()