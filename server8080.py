import socket
import time
import threading
import psycopg2

def print_database_identification():
    try:
        # Replace these values with your database credentials
        conn = psycopg2.connect(
            dbname="BookStore8080",
            user="postgres",
            password="p@ssword",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()

        # Query to get current database and user
        cursor.execute("SELECT current_database(), current_user")
        database_identification = cursor.fetchone()

        if database_identification:
            current_database, current_user = database_identification
            print("Database BookStore8080 connected and ready to complete queries!")
            print(f"Current Database: {current_database}")
            print(f"Current User: {current_user}")
        else:
            print("Unable to fetch database identification.")

    except psycopg2.Error as e:
        print(f"Error: {e}")


def server():
    thread_8080 = threading.Thread(target=spin_new_server, args=(8080,))
    thread_8080.start()

def spin_new_server(port = 8080):
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

def main():
    server()
    print_database_identification()

if __name__ == "__main__":
    main()
