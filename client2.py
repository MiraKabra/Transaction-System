import argparse
# Prompts for all user arguments for a given transaction at once

def t1():
    print("Please input information in the following format: \n"
          "--title BOOK_TITLE --fn AUTHOR_FIRST_NAME --ln AUTHOR_LAST_NAME --price BOOK_PRICE --isbn BOOK_ISBN")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--title', type=str, nargs='+', required=True, help='Book Title')
    parser.add_argument('--fn', type=str, required=True, help='Author\'s first name')
    parser.add_argument('--ln', type=str, required=True, help='Author\'s last name')
    parser.add_argument('--price', type=int, required=True, help='Book price')
    parser.add_argument('--isbn', type=str, required=True, help='Book ISBN')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [' '.join(args.title), args.fn, args.ln, args.price, args.isbn]
    print(params)
    return params

# Transaction 2: Update book price
def t2():
    print("Please input information in the following format: \n"
          "--title BOOK_TITLE --price BOOK_PRICE")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--title', type=str, nargs='+', required=True, help='Book Title')
    parser.add_argument('--price', type=int, required=True, help='Book price')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [' '.join(args.title), args.price]
    print(params)
    return params

# Transaction 3: Retrieve author information
def t3():
    print("Please input information in the following format: \n"
          "--fn AUTHOR_FIRST_NAME --ln AUTHOR_LAST_NAME")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--fn', type=str, required=True, help='Author\'s first name')
    parser.add_argument('--ln', type=str, required=True, help='Author\'s last name')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [args.fn, args.ln]
    print(params)
    return params

# Transaction 4: Update author description
def t4():
    print("Please input information in the following format: \n"
          "--fn AUTHOR_FIRST_NAME --ln AUTHOR_LAST_NAME --desc AUTHOR_DESCRIPTION")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--fn', type=str, required=True, help='Author\'s first name')
    parser.add_argument('--ln', type=str, required=True, help='Author\'s last name')
    parser.add_argument('--desc', type=int, nargs='+', required=True, help='Author description')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [args.fn, args.ln, ' '.join(args.desc)]
    print(params)
    return params

# Transaction 5: Record a sale
def t5():
    print("Please input information in the following format: \n"
          "--title BOOK_TITLE --q BOOK_QUANTITY")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--title', type=str, nargs='+', required=True, help='Book Title')
    parser.add_argument('--q', type=int, required=True, help='Purchased book quantity')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [' '.join(args.title), args.q]
    print(params)
    return params

# Transaction 6: Remove a sale record
def t6():
    print("Please input information in the following format: \n"
          "--sale SALE_ID")
    parser = argparse.ArgumentParser()
    inp = input()
    parser.add_argument('--sale', type=str, required=True, help='Sale ID')
    while True:
        try:
            args = parser.parse_args(inp.split())
            break
        except:
            print("Invalid Input")
            inp = input()
    params = [args.sale]
    print(params)
    return params

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
        options[mode]()
        return mode


if __name__ == '__main__':
    while True:
        mode = getUserInput()
        if mode == 7:
            break

