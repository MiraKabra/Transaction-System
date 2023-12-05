import click
import re
# Prompts for user arguments for a given transaction one by one

# Transaction 1: Add a new book
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
@click.option("--isbn", prompt="Enter the book's ISBN", type=str)
def t1(title, fn, ln, price, isbn):
    param = [title, fn, ln, price, isbn]
    print(param)
    return param

# Transaction 2: Update book price
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
def t2(title, price):
    param = [title, price]
    print(param)
    return param

# Transaction 3: Retrieve author information
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
def t3(fn, ln):
    param = [fn, ln]
    print(param)
    return param

# Transaction 4: Update author description
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--desc", prompt="Enter the author description", type=str)
def t4(fn, ln, desc):
    param = [fn, ln, desc]
    print(param)
    return param

# Transaction 5: Record a sale
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--quantity", prompt="Enter the quantity of books purchased", type=int)
def t5(title, quantity):
    param = [title, quantity]
    print(param)
    return param

# Transaction 6: Remove a sale record
@click.command()
@click.option("--saleid", prompt="Enter the sale record ID", type=str)
def t6(saleid):
    param = [saleid]
    print(param)
    return param

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
    while True:
        path = 'input.txt'
        inputMethod = 1
        # Alternatively, uncomment below to let user choose input Method in CLI
        # inputMethod = int(input())
        mode = getUserInput(inputMethod, path)
        if mode == 7:
            break
