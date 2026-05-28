#  Mini-Ecommerce system
import os
import time


product=[
    ["Socks",1000,1000],
    ["Shoes",10000,200],
    ["T-shirts",6000,299],
    ["Track suit",10000,199],
    ["Toy car",150000,50]
]


# Defining an empty cart
cart=[]


# Showing products available
def view_prod():
    for index, p in enumerate(product):
        print (index + 1, p[0], "\tprice:", p[1], "\tQuantity:", p[2])


# Showing options available
def menu():
    print("-"*20)
    print("MINI ECCOMMERCE SHOP")
    print("-"*20)
    print("1 = View products")
    print("2 = Add product to a cart")
    print("3 = Complete a purchase")
    print("4 = Show cart")
    print("5 = Exit the system")
    print("-"*20)
    return


# Purchasing a product
def put_cart():
    for id ,p in enumerate(product):
        print(id, p[0])
    index = int(input("Please input the index of the product you want to buy: "))
    item = product[index]
    quantity = item[-1]
    qty = int(input(f"How many of {item[0]} would like to buy: "))
    if quantity > qty:
        total_price = item[1] * qty
        c = [item[0],qty,total_price]
        cart.append(c)
        print(f"{item[0]} has successfully been added to cart")
    else:
        print("There is not enough stock")


   


def purchase():
    money = int(input("Enter the amount of money you have: "))
    amount = 0
    for c in cart:
        amount += c[-1]
    if amount > money:
        print(f"The amount you entered is insufficient, you need {amount}")
    else:
        cart.clear()
        print("Purchase successful")


# Allowing user to see cart
def show_cart():
    if len(cart) <= 0:
        print("Cart is empty, add a product")
    for index, p in enumerate(cart):
        print (index + 1, p[0], "\tQuantity:", p[1], "\tTotal price:", p[2])


#  Exits mini_eccommerce store
def leave():
   print("Thank you for shopping in our store!!. BYE!!")
   exit()




# Clears terminal after an amount of seconds
def clear():
    input("Click on enter to continue: ")
    os.system("cls")






while True:
    clear()
    menu()
    choose=int(input("Please choose between 1, 2, 3, 4, 5: "))
    if choose == 1:
        view_prod()
    elif choose == 2:
        print("-"*20)
        put_cart()
    elif choose == 3:
        purchase()
    elif choose == 4:
        show_cart()
    elif choose == 5:
        print("-"*20)
        leave()
   