print("\nWelcome to the Epidnayacreations!")
print("\nBags crafted to Perfection!")

# Create an empty dictionary for the inventory
inventory = {}
#Create a list of restock and sale
history = []


import csv
from datetime import datetime

#Add Stock
def add(inventory):
    category = input("Enter Category (Bag/Material) of what you want to add: ").capitalize()
    item = input("Enter the item you want to add: ").capitalize()
    quantity = float(input("Enter quantity: "))
    price = float(input("Enter price per item: "))

    if category not in inventory:
        inventory[category] = {}

    if item in inventory[category]:
        inventory[category][item]["quantity"] += quantity
        inventory[category][item]["price"] = price

    else:
        inventory[category][item] = {
            "quantity": quantity,
            "price": price
        }

    date = datetime.now().strftime("%Y-%M-%d")

    history.append({
        "type": "New Items",
        "category": category,
        "item": item,
        "quantity": quantity,
        "price": price,
        "date": date
    })
    print(f"{item}, added successfully under {category}. Current stock available: {inventory[category][item]['quantity']}")   

#Remove Stock (Sale)
def remove(inventory):
    category = input("Enter Category (Bag/Material) of what you want to remove: ").capitalize()
    item = input("Enter the item you want to remove: ").capitalize()
    quantity = float(input("Enter quantity: "))

    if category in inventory and item in inventory[category]:
            if inventory[category][item]["quantity"] >= quantity:
                inventory[category][item]["quantity"] -= quantity
                print(f"{item}, removed successfully. Current stock available: {inventory[category][item]['quantity']}") 
                date = datetime.now().strftime("%Y-%m-%d")
                history.append({
                    "type": "Sale",
                    "category": category,
                    "item": item,
                    "quantity": quantity,
                    "price": inventory[category][item]["price"],
                    "date": date
                })  
            else:
                print(f"Not enough {item} available to remove. Current stock available: {inventory[category][item]['quantity']}")
        
    else:
        print(f"{item} not found in inventory{category}.")
    


#Check Balance of an item
def view_item(inventory):
    category = input("Enter Category (Bag/Material) of what you want to check: ").capitalize()
    item = input("Enter the item you want to check: ").capitalize()

    if category in inventory and item in inventory[category]:
        print(f"\nItem: {item}")
        print(f"\nQuantity: {inventory[category][item]['quantity']}")
        print(f"\nPrice: {inventory[category][item]['price']}")

    else:
        print(f"{item} not available")

#View full inevntory
def view(inventory):
    if not inventory:
        print(f"Inventory is empty")
        return
    total_bag_value = 0
    total_material_value = 0

    # View Bags
    if "Bag" in inventory:
        print("\n=== BAGS ===")
        for item in inventory["Bag"]:
            print(f"Item: {item}, Quantity: {inventory['Bag'][item]['quantity']}, Price: {inventory['Bag'][item]['price']}")
            QuantityB = inventory['Bag'][item]['quantity']
            Price = inventory['Bag'][item]['price']
            total_bag_value += QuantityB * Price
        print(f"Total value of Bags: {total_bag_value}")
    else:
        print("\nNo Bags available.")

    # View Materials
    if "Material" in inventory:
        print("\n=== MATERIALS ===")
        for item in inventory["Material"]:
            print(f"Item: {item}, Quantity: {inventory['Material'][item]['quantity']}, Price: {inventory['Material'][item]['price']}")
            QuantityM = inventory['Material'][item]['quantity']
            Price = inventory['Material'][item]['price']
            total_material_value += QuantityM * Price
        print(f"Total value of Materials: {total_material_value}")
    else:
        print("\nNo Materials available.")        

#delete item in inventory
def delete_item(inventory):
    category = input("Enter Category (Bag/Material) of what you want to check: ").capitalize()
    item = input("Enter the item you want to delete: ").capitalize()

    if category in inventory and item in inventory[category]:
        del inventory[category][item]
        print(f"{item} deleted successfully from {category}.")
    else:
        print(f"{item} not found")

def view_category(inventory):
    category = input("Enter category: ").capitalize()

    if category in inventory:
        print(f"\nCategory: {category}")
        for item in inventory[category]:
            print(f"Item: {item}, Quantity: {inventory[category][item]['quantity']}, Price: {inventory[category][item]['price']}")
    else:
        print("Category not found.")

def view_history(history):
    if not history:
        print("No transactions yet.")
        return

    print("\n=== TRANSACTION HISTORY ===")
    for record in history:
        print(f"{record['date']} | {record['type']} | {record['category']} | {record['item']} | Qty: {record['quantity']} | Price: {record['price']}")



restart = "yes"

while restart.lower() == "yes":

    print("\n......INVENTORY MENU........")
    print("\nWhat would you like to do today?")
    print("\n1. View Inventory")
    print("\n2. View Inventory per Catgeory")
    print("\n3. View Item in a Category")
    print("\n4. Add Item to a Category")
    print("\n5. Remove Item Quantity (Sales) ")
    print("\n6. Delete Item from Category")
    print("\n7. Transaction history")
    print("\n8. Exit")

    try:
        choice = int(input("Pick an option of what you want to do: "))
    except ValueError:
        print("Please enter a number.")
        continue

    if choice == 1:
        view(inventory)
    elif choice == 2:
        view_category(inventory)
    elif choice == 3:
        view_item(inventory)
    elif choice == 4:
        add(inventory)
    elif choice == 5:
        remove(inventory)
    elif choice == 6:
        delete_item(inventory)
    elif choice == 7:
        view_history(history)
    elif choice == 8:
        print("Goodbye!")
    else:
        print("Invalid Choice")

    restart = input("\nDo you want to perform another task? (yes/no): ")

print("Bye! See You Next Time.")

