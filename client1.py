import click
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
    return

# Transaction 2: Update book price
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--price", prompt="Enter the book price", type=int)
def t2(title, price):
    param = [title, price]
    print(param)

# Transaction 3: Retrieve author information
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
def t3(fn, ln):
    param = [fn, ln]
    print(param)

# Transaction 4: Update author description
@click.command()
@click.option("--fn", prompt="Enter the author's first name", type=str)
@click.option("--ln", prompt="Enter the author's last name", type=str)
@click.option("--desc", prompt="Enter the author description", type=str)
def t4(fn, ln, desc):
    param = [fn, ln, desc]
    print(param)

# Transaction 5: Record a sale
@click.command()
@click.option("--title", prompt="Enter the book title", type=str)
@click.option("--quantity", prompt="Enter the quantity of books purchased", type=int)
def t5(title, quantity):
    param = [title, quantity]
    print(param)

# Transaction 6: Remove a sale record
@click.command()
@click.option("--saleID", prompt="Enter the sale record ID", type=str)
def t6(saleID):
    param = [saleID]
    print(param)
    return

def getUserInput():
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
    options = {1: t1, 2: t2, 3: t3, 4: t4, 5: t5, 6: t6}
    if mode == 7:
        return mode
    else:
        options[mode](standalone_mode = False)
        return mode


if __name__ == '__main__':
    while True:
        mode = getUserInput()
        if mode == 7:
            break

