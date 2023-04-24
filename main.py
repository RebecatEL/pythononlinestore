# 1 - Online store

import sqlite3
import sys

# Create database & record
    # Product info: product id, product name, product price, product category
conn = sqlite3.connect('store.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price NUMERIC NOT NULL, 
    category TEXT NOT NULL)
""")
#cur.execute("""
# INSERT INTO products(id, name, price, category) VALUES (1,'Harry Potter',10.0,'Book'),
# (2,'Python Intro',20.5,'Book'),(3,'Data Structure',35.6,'Book')
# """)
conn.commit()

cur.execute("SELECT * FROM products")
resAll = cur.fetchall()


# Shopping cart item
    # Object-oriented approch
class cartItem:
    def __init__(self, id, name, price, category, numPurchase):
        self.id = int(id)
        self.name = name
        self.price = float(price)
        self.category = category
        self.numPurchase = int(numPurchase)

    def __repr__(self):
        return '%-5i|%-20s|%-10.2f|%-11s|%-6i' \
            % (self.id, self.name, self.price, self.category, self.numPurchase)


# cart_item[id, name, price, catagory, no. of purchase]
# initial data
cart_list = []
initial_item = cartItem(1, 'Harry Potter', 10, 'Book', 5)
cart_list.append(initial_item)


def menu():
    print("Menu:" '\n'
          "1. View products" '\n'
          "2. View shopping cart" '\n'
          "3. Exit")
    choice = input("Please input your option number 1-3: ")
    chk_choice = check_choice(choice)
    while chk_choice:
        choice = int(choice)
        match choice:
            case 1:
                # view products
                products()
                return
            case 2:
                # view shopping cart
                cart()
                return
            case 3:
                sys.exit()
    while not chk_choice:
        print("Invalid option. You must enter number between 1-3.")
        choice = input("Please enter the number of option: ")
        chk_choice = check_choice(choice)


# Check menu choice
def check_choice(choice):
    try:
        if 1 <= int(choice) <= 3:
            return True
        else:
            return False
    except ValueError:
        return False


# View products function
def products():
    print("View Products")
    print("- Bulk discount (quality >= 10): purchase and receive a discount of 5% off for that item!")
    print("- Combo discount: purchase 'Python Intro' and 'Data Structure' together, receive 10% off!")
    print("-- Shipping fee of $9.99 if the order value is less than $75 and taxes (13%) --")
    # list products
    global resAll
    print("id   |Name                |Price     |Category")
    for row in resAll:
        print("%-5i|%-20s|%-10.2f|%-11s" % (row[0], row[1], row[2], row[3]))
    # Ask user to input id & no. of the items added
    while True:
        prod_choice = input("Please input the id of the product you want to purchase or type 'cancel' to back to menu: ")
        prod_choice_check = prod_id_check(prod_choice)
        if prod_choice_check == 1:  # if 'cancel'
            return
        while prod_choice_check == 2:  # if product id exist
            prod_choice_num = input("Please input the number of the product you want to purchase: ")
            prod_num_chk = prod_num_check(prod_choice_num)  # True / False
            if prod_num_chk:
                temp_name = ''
                temp_price = 0.00
                temp_cat = ''
                for row in resAll:
                    if row[0] == int(prod_choice):
                        temp_name = row[1]
                        temp_price = float(row[2])
                        temp_cat = row[3]
                temp_item = cartItem(int(prod_choice), temp_name, temp_price, temp_cat, int(prod_choice_num))
                cart_list.append(temp_item)
                print('Successfully added item to shopping cart!')
                return
            else:
                print('Please input number!')
        if prod_choice_check == 3:
            print('Please input valid id!')
        if prod_choice_check == 4:
            print('Please input id in number!')


def prod_id_check(choice):
    if choice.lower() == 'cancel':
        return 1
    global resAll
    try:
        choice = int(choice)
        for row in resAll:
            if row[0] == int(choice):
                return 2
        else:
            return 3
    except ValueError:
        return 4


def prod_num_check(choice):
    try:
        if int(choice):
            return True
    except ValueError:
        return False


# View Shopping cart
def cart():
    sub_total = 0.00
    shipping = 0.00
    tax = 0.13
    print("--- Shopping cart ---")
    print("id   |Name                |Price     |Category   |Number")
    for row in cart_list:
        print(repr(row))
        sub_total += row.price * row.numPurchase
    print("")
    discount = round(cal_discount(),2)
    temp_total = sub_total - discount
    print("Subtotal: " + str(sub_total))
    print("Discount: " + str(discount))
    if temp_total < 75.00:
        shipping = 9.99
    print("Shipping fee: " + str(shipping))
    print("Tax (13%): " + str(round(sub_total*tax,2)))
    print("---------")
    total = round(temp_total + shipping + (sub_total*tax),2)
    print("Total: " + str(total))
    print("")
    print("Do you want to checkout now?")
    checkout_choice = input("Input 'checkout' to checkout / 'back' to go back to menu: ")
    while not checkout_choice.lower() == 'checkout' and not checkout_choice.lower() == 'back':
        print("Invalid input. Please input again!")
        checkout_choice = input("Input 'checkout' to checkout / 'back' to go back to menu: ")
    if checkout_choice.lower() == 'checkout':
        s = '--- Receipt --- \n'
        s += "id   |Name                |Price     |Category   |Number \n"
        for row in cart_list:
            s += repr(row) + "\n"
        s += "\nTotal: " + str(total)
        s += "\nThank you!"
        with open('receipt.txt', 'w+') as file:
            file.write(s)
    if checkout_choice.lower() == 'back':
        return


def cal_discount():
    # return a discount back to cart(), then calculate final total = total - discount - combo_dis
    dis = 0.00
    combo = 0
    combo_dis = 0.00
    for row in cart_list:
        # Bulk discount
        if row.numPurchase >= 10:
            dis += row.price * 0.05
        # Combo discount
        if row.id == 2 or row.id == 3: # Combo discount for 'Python Intro' + 'Data Structure'
            combo += 1
            combo_dis += row.price * 0.1
        if combo == 2:
            dis += combo_dis
    return dis


# Program start here
if __name__ == '__main__':
    print("=== Welcome to online store ===")
    while True:
        menu()

