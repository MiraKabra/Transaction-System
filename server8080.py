import ast
import datetime
import socket
import time
import threading

import psycopg2


def print_database_identification():
    try:
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
            return conn, cursor
        else:
            print("Unable to fetch database identification.")

    except psycopg2.Error as e:
        print(f"Error: {e}")


def server(cursor, connection):
    thread_8080 = threading.Thread(target=spin_new_server, args=(cursor, connection, 8080,))
    thread_8080.start()


def startTxn1_FH(value_string, cursor, connection):
    print("Starting Transaction 1: Add New Book")
    # value_list = ast.literal_eval(value_string) #Turns string into list
    #Each element from the list getting put in its own variable
    hop = value_string[0]
    currTS = value_string[1]
    book_title = value_string[2]
    author_fname = value_string[3]
    author_lname = value_string[4]
    book_price = value_string[5]
    bool_isbn = value_string[6]

    #printing the query that will be run
    print("Running Txn 1 First Hop Query: SELECT from Authors")

    #writing the query and storing in variable
    query = """SELECT author_id 
                FROM public."Authors"   
                WHERE author_first_name = %s AND author_last_name = %s"""
    cursor.execute(query, (author_fname, author_lname)) #executing the query and adding parameters
    rows = cursor.fetchall() # fetching all rows that return from the query
    for row in rows:
        author_id = int(row[0])
        print("Author ID: {}".format(author_id)) # printing the author's id
    print("Completed First Hop Query: SELECT from Authors")
    return [author_id] #returning the author id for the client to send back to the server that will complete the req
    # print("New Book Not Yet Added")

def startTxn1_SH(value_list, cursor, connection):
    start = time.time()
    # value_list = ast.literal_eval(value_string)
    book_title = value_list[-6]
    book_price = value_list[-3]
    book_isbn = value_list[-2]
    author_id = value_list[-1]
    print("Running Txn 1 Second Hop Query: INSERT INTO Books")
    query = """INSERT INTO public."Books" (title, price, isbn, author_id)
                VALUES ( %s, %s, %s, %s)
    """
    cursor.execute(query, (book_title, book_price, book_isbn, author_id))
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into table")
    return [0]

#Code block for commutative property for txn 1:
# # Check if the book already exists based on the title
# select_query = """
#     SELECT * FROM public."Books"
#     WHERE title = %s
# """
# cursor.execute(select_query, (title,))
# existing_book = cursor.fetchone()

# if existing_book:
#     print(f"Book '{title}' already exists. Not adding it again.")
# else:
#     # Add the book to the table if it doesn't exist
#     insert_query = """
#         INSERT INTO public."Books" (title, price, isbn, author_id)
#         VALUES (%s, %s, %s, %s)
#     """
#     cursor.execute(insert_query, (title, price, isbn, author_id))
#     print(f"Book '{title}' added to the table.")

#     # Commit the transaction to make the changes permanent
#     connection.commit()

def startTxn2_FH(value_string, cursor, connection):
    print("Starting Transaction 2: Update Book Price")
    # value_list = list(value_string)  # Turns string into list
    # Each element from the list getting put in its own variable
    hop = value_string[0]
    currTS = value_string[1]
    book_title = value_string[-2]
    book_price = value_string[-1]

    #printing the query that will be run
    print("Running Txn 2 First Hop Query: SELECT from Books")

    #writing the query and storing in variable
    query = """SELECT book_id 
                FROM public."Books"   
                WHERE title = %s"""
    cursor.execute(query, (book_title,)) #executing the query and adding parameters
    rows = cursor.fetchall() # fetching all rows that return from the query
    for row in rows:
        book_id = int(row[0])
        print("Book ID: {}".format(book_id)) # printing the book's id
    print("Completed First Hop Query: SELECT from Books")
    return [book_id] #returning the book id for the client to send back to the server that will complete the req


def startTxn2_SH(value_list, cursor, connection):
    # value_list = ast.literal_eval(value_string)
    # hop = value_list[0]
    # currTS = value_list[1]
    book_id = value_list[-1]
    book_title = value_list[-3]
    book_price = value_list[-2]
    print("Running Second Hop Query for Transaction 2")
    print("Running Txn 2 Second Hop Query: INSERT INTO Books")
    query = """UPDATE public."Books" SET price = %s WHERE book_id = %s"""
    cursor.execute(query, (book_price, book_id))
    connection.commit()
    print("Completed Second Hop Query: UPDATE Books")
    return [0]

# Code block for commutative property for txn 2:
# # Fetch current price from the database for the given book_id
# select_query ="""
#     SELECT price FROM public."Books"
#     WHERE book_id = %s
# """
# cursor.execute(select_query, (book_id,))
# current_price = cursor.fetchone()[0]

# # Calculate the maximum of current and new prices
# max_price = max(current_price, new_price)

# # Update the price in the database with the maximum value
# update_query ="""
#     UPDATE public."Books"
#     SET price = %s
#     WHERE book_id = %s
# """
# cursor.execute(update_query, (max_price, book_id))

# # Commit the transaction to make the changes permanent
# connection.commit()

def startTxn3_FH(value_list, cursor, connection):
    print("Starting Transaction 3: Retrieve Author Information")
    # value_list = ast.literal_eval(value_string)
    hop = value_list[0]
    currTS = value_list[1]
    author_firstname = value_list[-2]
    author_lastname = value_list[-1]
    print("Running Query: SELECT * FROM Authors WHERE author_first_name = '{}' and author_last_name = '{}'".format(author_firstname, author_lastname))
    query = """SELECT * 
                FROM public."Authors" 
                WHERE author_first_name = %s AND author_last_name = %s"""
    cursor.execute(query, (author_firstname, author_lastname))
    rows = cursor.fetchall()

    for row in rows:
        author_id, author_first_name, author_last_name, region, description, timestamp = row
        print("Author ID: ", author_id)
        print("Author First Name: ", author_first_name)
        print("Author Last Name: ", author_last_name)
        print("Author's Region:", region)
        print("Author's Description: ", description)
        print("Last Updated Timestamp: ", timestamp)

    # cursor.close()
    print("Author's Information Printed")
    return rows


def startTxn4_FH(value_list, cursor, connection):
    print("Starting Transaction 4: Update Author Description")
    # value_list = ast.literal_eval(value_string)
    hop = value_list[0]
    currTS = value_list[1]
    author_firstname = value_list[-3]
    author_lastname = value_list[-2]
    description = value_list[-1]
    new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Running Query: SELECT * FROM Authors WHERE author_first_name = '{}' and author_last_name = '{}'".format(
        author_firstname, author_lastname))
    query = """UPDATE public."Authors" SET description = %s, timestamp = %s  WHERE author_first_name = %s and author_last_name = %s"""
    cursor.execute(query, (description, new_timestamp, author_firstname, author_lastname))
    connection.commit()
    count = cursor.rowcount
    print(count, "record updated successfully")
    print("Author's Information Updated")
    return [0]

# Code block for commutative property for txn 4:
# # Fetch current timestamp and description from the database for the given author_id
# select_query = """
#     SELECT description, timestamp FROM public."Authors"
#     WHERE author_id = %s
# """
# cursor.execute(select_query, (author_id,))
# current_description, current_timestamp = cursor.fetchone()

# # Calculate the maximum of current and new timestamps
# max_timestamp = max(current_timestamp, new_timestamp)

# # Update the description and timestamp in the database with the maximum value
# update_query = """
#     UPDATE public."Authors"
#     SET description = %s, timestamp = %s
#     WHERE author_id = %s
# """
# cursor.execute(update_query, (new_description, max_timestamp, author_id))

# # Commit the transaction to make the changes permanent
# connection.commit()

def startTxn5_FH(value_string, cursor, connection):
    print("Starting Transaction 5: Record Sale")
    # value_list = ast.literal_eval(value_string)  # Turns string into list
    # Each element from the list getting put in its own variable
    hop = value_string[0]
    currTS = value_string[1]
    book_title = value_string[-2]
    book_quantity = value_string[-1]

    # printing the query that will be run
    print("Running Txn 5 First Hop Query: SELECT from Books")
    # writing the query and storing in variable
    query = """SELECT book_id 
                    FROM public."Books"   
                    WHERE title = %s"""
    cursor.execute(query, (book_title,))  # executing the query and adding parameters
    rows = cursor.fetchall()  # fetching all rows that return from the query
    for row in rows:
        book_id = int(row[0])
        print("Book ID: {}".format(book_id))  # printing the book's id
    print("Completed First Hop Query: SELECT from Books")
    return [book_id]  # returning the book id for the client to send back to the server that will complete the req

def startTxn5_SH(value_list, cursor, connection):
    print("Running Second Hop Query for Transaction 5")
    # value_list = ast.literal_eval(value_string)
    hop = value_list[0]
    currTS = value_list[1]
    book_id = int(value_list[-1])
    book_title = value_list[-3]
    book_quantity = value_list[-2]
    sale_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    print("Running Txn 2 Second Hop Query: INSERT INTO Books")
    query = """INSERT INTO public."Sales" (book_id, title, quantity_sold, sale_date)
                    VALUES (%s, %s, %s, %s)
        """
    cursor.execute(query, (book_id, book_title, book_quantity, sale_timestamp))
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into table")
    return [0]


def startTxn6_FH(value_string, cursor, connection):
    print("Starting Transaction 6: Remove Sale Record")
    # value_list = ast.literal_eval(value_string)  # Turns string into list
    # Each element from the list getting put in its own variable
    hop = value_string[0]
    currTS = value_string[1]
    sale_id = value_string[-1]

    # writing the query and storing in variable
    query = """DELETE FROM public."Sales" WHERE sale_id = %s"""
    cursor.execute(query, (sale_id,))  # executing the query and adding parameters
    connection.commit()
    print("Completed First Hop Query: DELETE from Sales")
    return [0]

# def startTxn6_SH(value_string, cursor, connection):
#     print("Running Second Hop Query for Transaction 6")
#     print("Sale Record Removed")



def spin_new_server(cursor, connection, port=8080):
    options = {1: [startTxn1_FH, startTxn1_SH], 2:[startTxn2_FH, startTxn2_SH], 3: [startTxn3_FH], 4: [startTxn4_FH], 5: [startTxn5_FH, startTxn5_SH], 6: [startTxn6_FH]}

    while True:
        print("Server started at port: " + str(port))
        host = socket.gethostname()   # get local machine name
        s = socket.socket()
        s.bind((host, port))

        s.listen(1)
        client_socket, adress = s.accept()
        print("Connection from: " + str(adress))
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)
            print('Received request at server running at port: ' + str(port))
            print(time.time())
            data = data.strip('{}')
            key, value = data.split(':')
            # result = switch(int(key), value, cursor)
            print("Key:", key, type(key))
            print("Value", value, type(value))
            valueList = ast.literal_eval(value)
            print(valueList)
            result = options[int(key)][valueList[0] - 1](valueList, cursor, connection)
            data_dict = {key: value}
            print("result:", result[0])
            print("result:", str(result[0]))
            print(time.time())
            print('From online user: ' + data)
            data = data.upper()
            print("server finished processing request")
            client_socket.send(str(result[0]).encode('utf-8'))
        client_socket.close()


def main():
    db_connection, db_cursor = print_database_identification()
    server(db_cursor, db_connection)


if __name__ == "__main__":
    main()
