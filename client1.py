import core
import click
import re
import time
import numpy as np
import sys
# Prompts for user arguments for a given transaction one by one

NUM_USERS = len(core.user_map.keys())

def two_hop_operation(transaction_num, first_hop_param, second_hop_param):
    first_hop_tr_argument_map = {}
    first_hop_tr_argument_map[transaction_num] = first_hop_param
    second_hop_tr_argument_map = {}
    second_hop_tr_argument_map[transaction_num] = second_hop_param

    first_hop_index = np.random.randint(0, NUM_USERS)
    second_hop_index = np.random.randint(0, NUM_USERS)

    latency = util(first_hop_index, first_hop_tr_argument_map, True)
    util(second_hop_index, second_hop_tr_argument_map, False)
    print(latency)
    if inputMethod == 1:
        latency_file.write(str(latency) + "\n")
        latency_file.flush()
    return latency

def one_hop_operation(transaction_num, first_hop_param):
    first_hop_tr_argument_map = {}
    first_hop_tr_argument_map[transaction_num] = first_hop_param
    first_hop_index = np.random.randint(0, NUM_USERS)
    latency = util(first_hop_index, first_hop_tr_argument_map, True)
    print(latency)
    if inputMethod == 1:
        latency_file.write(str(latency) + "\n")
        latency_file.flush()
    return first_hop_param, latency

def util(index, transaction_argument_map, isFirstHop):
    country = core.country_map[index]
    port = core.ports[country]
    if port == 8080:
        s = client_8080
    elif port == 8085:
        s = client_8085
    elif port == 8090:
        s = client_8090
    if isFirstHop:
        t = core.sendWithRecv(s, str(transaction_argument_map))
        return t
    core.send(s, str(transaction_argument_map))
    return None

# Transaction 1: Add a new book
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
@click.option("--isbn", prompt="Enter the book's ISBN", type=str)
def t1(title, fn, ln, price, isbn):
    ts = time.time()
    first_hop_param = [1, ts, title, fn, ln, price, isbn]
    second_hop_param = [2, ts, title, fn, ln, price, isbn]

    latency = two_hop_operation(1, first_hop_param, second_hop_param)
    return latency

# Transaction 2: Update book price
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
def t2(title, price):
    ts = time.time()
    first_hop_param = [1, ts, title, price]
    second_hop_param = [2, ts, title, price]
    latency = two_hop_operation(2, first_hop_param, second_hop_param)
    return latency

# Transaction 3: Retrieve author information
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
def t3(fn, ln):
    ts = time.time()
    first_hop_param = [1, ts, fn, ln]
    latency = one_hop_operation(3, first_hop_param)
    return latency

# Transaction 4: Update author description
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--desc", prompt="Enter the author description", type=str)
def t4(fn, ln, desc):
    ts = time.time()
    first_hop_param = [1, ts, fn, ln, desc]
    latency = one_hop_operation(4, first_hop_param)
    return latency

# Transaction 5: Record a sale
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--quantity", prompt="Enter the quantity of books purchased", type=int)
def t5(title, quantity):
    ts = time.time()
    first_hop_param = [1, ts, title, quantity]
    second_hop_param = [2, ts, title, quantity]
    latency = two_hop_operation(5, first_hop_param, second_hop_param)
    return latency

# Transaction 6: Remove a sale record
@click.command()
@click.option("--saleid", prompt="Enter the sale record ID", type=str)
def t6(saleid):
    ts = time.time()
    first_hop_param = [1, ts, saleid]
    second_hop_param = [2, ts,  saleid]
    latency = two_hop_operation(6, first_hop_param, second_hop_param)
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
        while True:
            # read file line by line
            line = file.readline()
            print(line[:-1])
            mode = int(line[0])
            if mode == 1:
                inp = re.split('(--title|--fn|--ln|--price|--isbn)', line[:-1])[1:]
            elif mode == 2:
                inp = re.split('(--title|--price)', line[:-1])[1:]
            elif mode == 3:
                inp = re.split('(--fn|--ln)', line[:-1])[1:]
            elif mode == 4:
                inp = re.split('(--fn|--ln|--desc)', line[:-1])[1:]
            elif mode == 5:
                inp = re.split('(--title|--quantity)', line[:-1])[1:]
            elif mode == 6:
                inp = re.split('(--saleid)', line[:-1])[1:]
            elif mode == 7:
                return mode
            inp = [i.strip() for i in inp]
            options[mode](inp, standalone_mode=False)
        file.close()


if __name__ == '__main__':
    path = sys.argv[1]
    print(path)
    client_8080 = core.client(8080)
    print(client_8080)
    client_8085 = core.client(8085)
    print(client_8085)
    client_8090 = core.client(8090)
    print(client_8090)
    while True:
        inputMethod = 1
        latency_file = open("latency.txt", "a")
        # Alternatively, uncomment below to let user choose input Method in CLI
        # inputMethod = int(input())

        print("here")
        mode = getUserInput(inputMethod, path)
        latency_file.close()
        if mode == 7:
            client_8080.close()
            client_8085.close()
            client_8090.close()
            break
