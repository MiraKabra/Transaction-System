import ast

import core
import click
import re
import time
import numpy as np
import sys
# Prompts for user arguments for a given transaction one by one
global total_latency
total_latency = 0
NUM_USERS = len(core.user_map.keys())

def two_hop_operation(transaction_num, first_hop_param, second_hop_param):
    first_hop_tr_argument_map = {}
    first_hop_tr_argument_map[transaction_num] = first_hop_param
    second_hop_tr_argument_map = {}
    second_hop_tr_argument_map[transaction_num] = second_hop_param

    first_hop_index = np.random.randint(0, NUM_USERS)
    second_hop_index = np.random.randint(0, NUM_USERS)

    latency, returned_data = util(first_hop_index, first_hop_tr_argument_map, True, transaction_num)
    print(transaction_num, returned_data)
    second_hop_tr_argument_map[transaction_num].append(returned_data)
    util(second_hop_index, second_hop_tr_argument_map, False, transaction_num)
    print(latency)
    if inputMethod == 1:
        latency_file.write(str(latency) + "\n")
        latency_file.flush()
        data_file.write(str(None) + "\n") #We don't get data other than None for any two hop transactions
        data_file.flush()
    return latency

def one_hop_operation(transaction_num, first_hop_param):
    first_hop_tr_argument_map = {}
    first_hop_tr_argument_map[transaction_num] = first_hop_param
    first_hop_index = np.random.randint(0, NUM_USERS)
    latency, returned_data = util(first_hop_index, first_hop_tr_argument_map, True, transaction_num)
    print(latency)
    if inputMethod == 1:
        latency_file.write(str(latency) + "\n")
        latency_file.flush()
        data_file.write(str(returned_data) + "\n")
        data_file.flush()
    return first_hop_param, latency

def write_data_to_file(data):
    return

def util(index, transaction_argument_map, isFirstHop, transaction_num = 0):
    country = core.country_map[index]
    port = core.ports[country]
    clients = [client_8080, client_8085, client_8090]
    if port == 8080:
        s = client_8080
    elif port == 8085:
        s = client_8085
    elif port == 8090:
        s = client_8090
    print("isFirstHop: " + str(isFirstHop))
    if isFirstHop:
        print("Txn #: ", transaction_num)
        if transaction_num == 3:
            t, returned_data = core.sendWithRecv(s, str(transaction_argument_map))
            return t, returned_data
        if transaction_num == 4 or transaction_num == 6:
            first_send = True
            t = 0
            for s in clients:
                if first_send:
                    t, returned_data = core.sendWithRecv(s, str(transaction_argument_map))
                    first_send = False
                else:    
                    t, returned_data = core.sendWithRecv(s, str(transaction_argument_map))
            return t, returned_data
        else:    
            t, returned_data = core.sendWithRecv(s, str(transaction_argument_map))
            print("Printed from Util: Txn #", transaction_num, "Returned Data:", returned_data)
            return t, returned_data
    #Second hop update to all the servers
    for s in clients:
        t, returned_data = core.sendWithRecv(s, str(transaction_argument_map))
    return t, returned_data

# Transaction 1: Add a new book
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
@click.option("--isbn", prompt="Enter the book's ISBN", type=str)
def t1(title, fn, ln, price, isbn):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, title, fn, ln, price, isbn]
    second_hop_param = [2, ts, title, fn, ln, price, isbn]

    latency = two_hop_operation(1, first_hop_param, second_hop_param)
    total_latency += latency
    return latency

# Transaction 2: Update book price
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
def t2(title, price):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, title, price]
    second_hop_param = [2, ts, title, price]
    latency = two_hop_operation(2, first_hop_param, second_hop_param)
    total_latency += latency
    return latency

# Transaction 3: Retrieve author information
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
def t3(fn, ln):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, fn, ln]
    param, latency = one_hop_operation(3, first_hop_param)
    total_latency += latency
    return latency

# Transaction 4: Update author description
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--desc", prompt="Enter the author description", type=str)
def t4(fn, ln, desc):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, fn, ln, desc]
    param, latency = one_hop_operation(4, first_hop_param)
    total_latency += latency
    return latency

# Transaction 5: Record a sale
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--quantity", prompt="Enter the quantity of books purchased", type=int)
def t5(title, quantity):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, title, quantity]
    second_hop_param = [2, ts, title, quantity]
    latency = two_hop_operation(5, first_hop_param, second_hop_param)
    total_latency += latency
    return latency

# Transaction 6: Remove a sale record
@click.command()
@click.option("--saleid", prompt="Enter the sale record ID", type=str)
def t6(saleid):
    global total_latency
    ts = time.time()
    first_hop_param = [1, ts, saleid]
    param, latency = one_hop_operation(6, first_hop_param)
    total_latency += latency
    return latency

def getUserInput(inputMethod=0, path=None):
    options = {1: t1, 2: t2, 3: t3, 4: t4, 5: t5, 6: t6}
    if inputMethod==0:
        print("Please choose one of the following transactions:")
        print("1. Add a new book")
        print("2. Update book price")
        print("3. Retrieve author information")
        print("4. Update author description")
        print("5. Record a sale")
        print("6. Remove a sale record")
        print("7. Exit")
        inp = input()
        while True:
            try:
                mode = int(inp)
                break
            except:
                print("Invalid input, please enter a valid transaction number (e.g. 5)")
                inp = input()
        if mode == 7:
            return mode
        else:
            options[mode](standalone_mode = False)
            return mode
    elif inputMethod==1:
        file = open(path, 'r')
        txnCount = 0
        startTime = time.time()
        while True:
            # read file line by line
            line = file.readline()
            print(line[:-1])
            mode = int(line[0])
            if mode == 1:
                inp = re.split('(--title|--fn|--ln|--price|--isbn)', line[:-1])[1:]
                txnCount += 1
            elif mode == 2:
                inp = re.split('(--title|--price)', line[:-1])[1:]
                txnCount += 1
            elif mode == 3:
                inp = re.split('(--fn|--ln)', line[:-1])[1:]
                txnCount += 1
            elif mode == 4:
                inp = re.split('(--fn|--ln|--desc)', line[:-1])[1:]
                txnCount += 1
            elif mode == 5:
                inp = re.split('(--title|--quantity)', line[:-1])[1:]
                txnCount += 1
            elif mode == 6:
                inp = re.split('(--saleid)', line[:-1])[1:]
                txnCount += 1
            elif mode == 7:
                break
            inp = [i.strip() for i in inp]
            options[mode](inp, standalone_mode=False)
        endTime = time.time()
        file.close()
    if total_latency > 0:
        print("Total Duration:", endTime - startTime)
        print("Total # of Txns:", txnCount)
        print("Throughput:", (txnCount / float(total_latency)))
    return mode


if __name__ == '__main__':
    inputMethod = 1
    if inputMethod == 1:
        path = sys.argv[1]
        data_file = open("dataFile.txt", "a")
    else:
        path = ""
    # print(path)
    client_8080 = core.client(8080)
    # print(client_8080)
    client_8085 = core.client(8085)
    # print(client_8085)
    client_8090 = core.client(8090)
    # print(client_8090)
    while True:

        latency_file = open("latency.txt", "a")
        # Alternatively, uncomment below to let user choose input Method in CLI
        # inputMethod = int(input())

        print("line before getUserInput")
        mode = getUserInput(inputMethod, path)
        latency_file.close()
        if mode == 7:
            client_8080.close()
            client_8085.close()
            client_8090.close()
            if inputMethod == 1:
                data_file.close()
            break
