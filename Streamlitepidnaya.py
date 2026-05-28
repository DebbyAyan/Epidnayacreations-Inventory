import pandas as pd
import datetime
import streamlit as st
from streamlit_option_menu import option_menu
st.title("Epidnayacreation Inventory")
st.subheader("Bag crafted to Perfection")
st.set_page_config(layout="centered")

if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "history" not in st.session_state:
    st.session_state.history = []

# Create an empty dictionary for the inventory
inventory = st.session_state.inventory
#Create a list of restock and sale
history = st.session_state.history


#add item function
def add_item(category, item, quantity, price):
    item = item.capitalize()

    if category not in inventory:
        inventory[category] = {}

    if item not in inventory[category]:
        inventory[category][item] = []

    for batch in inventory[category][item]:
        if batch["price"] == price:
            batch["quantity"] += quantity
            break
    else:
        inventory[category][item].append({
            "price": price,
            "quantity": quantity
        })
    
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    history.append({
        "type": "New Items",
        "category": category,
        "item": item,
        "quantity": quantity,
        "price": price,
        "date": date
    })      

    st.success(f"{quantity} {item}(s) at ₦{price} added successfully.")

#remove item(sales) function
def remove_item(category, item, quantity, price):
    item = item.capitalize()
    if not category or not item or not quantity or not price:
        st.info("Please fill in all details.")
        return

    if category in inventory and item in inventory[category]:
            for batch in inventory[category][item]:
                if batch["price"] == price:
                    if batch["quantity"] >= quantity:
                        batch["quantity"] -= quantity
                        st.success(f"{quantity} {item}(s) at ₦{price} removed successfully.")
                        
                        date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                        history.append({
                            "type": "Sold Items",
                            "category": category,
                            "item": item,
                            "quantity": quantity,
                            "price": price,
                            "date": date
                        })
                        break      
                    else:
                        st.error("Not enough stock")
                        return
            
        

#View by category
def view_category(category):
    category_data = []
    if not category:
        st.info("Please select a category to view.")
        return
    
    if category in inventory:
        for item in inventory[category]:
            for batch in inventory[category][item]:
                quantity = batch["quantity"]
                price = batch["price"]
                total = quantity * price
                if total == 0:
                    continue

                category_data.append({
                    "Item": item,
                    "Price": price,
                    "Quantity": quantity,
                    "Total Value": total
                })

        if category_data:
            df = pd.DataFrame(category_data)
            st.dataframe(df)
            st.info(f"Total Value: ₦{df['Total Value'].sum():,.2f}")
    else:
        st.warning(f"No items found in {category}")

#View by item
def view_item(item):
    item_data = []
    if not item:
        st.info("Please select an item to view.")
        return
    for category in inventory:
        if item in inventory[category]:
            for batch in inventory[category][item]:
                quantity = batch["quantity"]
                price = batch["price"]
                total = quantity * price
                if total == 0:
                    continue


                item_data.append({
                    "Item": item,
                    "Price": price,
                    "Quantity": quantity,
                    "Total Value": total
                })
    if item_data:
        df = pd.DataFrame(item_data)
        st.dataframe(df)
        st.info(f"Total Value: ₦{df['Total Value'].sum():,.2f}")

#delete item from inventory
def delete_item(category, item):
    if category in inventory and item in inventory[category]:
        del inventory[category][item]
    else:
        st.info(f"{item} not found")

    
    
        

#sidebar menu
with st.sidebar:
  selected=option_menu(
    menu_title= "Menu",
    options = ["View Inventory", "View Category", "View Item", "Add Item", "Remove Item(Sale)", "Delete Item", "View History"],
    default_index= 0,
  )

#View Inventory
if selected == "View Inventory":
    st.header("📦 Full Inventory")
   
    if not inventory:
        st.warning("Inventory is empty")
    
    else:
        inventory_data = []
        
        for category in inventory:
            for item in inventory[category]:
                for batch in inventory[category][item]:
                    quantity = batch["quantity"]
                    price = batch["price"]
                    total = quantity * price

                    inventory_data.append({
                        "Category": category,                
                        "Item": item,
                        "Price": price,
                        "Quantity": quantity,
                        "Total Value": total
                    })

        df = pd.DataFrame(inventory_data)
        st.dataframe(df)
        st.info(f"Total Inventory Value: ₦{df['Total Value'].sum():,.2f}")

        st.divider()
        
        if "show_clear_confirm" not in st.session_state:
            st.session_state.show_clear_confirm = False
 
        if st.button("Clear Entire Inventory", type="primary"):
            st.session_state.show_clear_confirm = True
 
        if st.session_state.show_clear_confirm:
            st.warning("Are you sure you want to delete the **entire inventory**? This cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete Everything"):
                    st.session_state.inventory.clear()
                    st.session_state.show_clear_confirm = False
                    st.success("Entire inventory deleted.")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_clear_confirm = False
                    st.rerun()
 
if selected == "View Category":
    st.header("View Items by Category")

    category = st.selectbox("Select category", options=("Bag", "Material"), index=None, placeholder="Select Category")

    view_category(category)

if selected == "View Item":
   st.header("Items")

   all_items = set()
   
   for category in inventory:
        for item in inventory[category]:
            all_items.add(item)

   item = st.selectbox(
       "Select item you want to check", 
       options=list(all_items),
       index=None,
       placeholder= "Select item"
   )

   view_item(item)


#add item streamlit
if selected == "Add Item":
   st.header("Purchases")
    
   category = st.selectbox("Select Category", options=["Bag", "Material"], index=None, placeholder= "Select Category")
   item = st.text_input("What item do you want to add?")
   quantity = st.number_input("Enter Quantity", min_value=0.1, step=0.1)
   price = st.number_input("Enter Price per item/Yard", min_value=0)

   if st.button("Add Item"):
      if not category or item.strip() == "" or price == 0 or quantity == 0:
         st.error("Please fill in all details.")
      else:
          add_item(category, item, quantity, price) 

#Streamlit code for remove
if selected == "Remove Item(Sale)":
    st.header("Sales")  
    
    all_itemss = set()

    for cat in inventory:
        for itm in inventory[cat]:
            all_itemss.add(itm)

    category = st.selectbox("Select Category", ["Bag", "Material"])
    item_in_cat = list(inventory.get(category, {}).keys()) if category in inventory else []
    item = st.selectbox("What item do you want to remove?", options=item_in_cat, index=None, placeholder= "Select Item to remove")
    prices = []
    if category in inventory and item in inventory[category]:
        prices = [
        batch["price"]
        for batch in inventory[category][item]
        ]
    price = st.selectbox("Select Price", options=prices, index=None, placeholder= "Select Price")
    quantity = st.number_input("Enter Quantity", min_value=0.1, step=0.1)
   
    if st.button("Remove Item"):
        if item.strip() == "":
            st.error("Please enter item name.")
        else:
          remove_item(category, item, quantity, price) 

if selected == "Delete Item":
    st.header("Delete Item")
    all_items = set()
    for category in inventory:
        for item in inventory[category]:
            all_items.add(item)
    itemtodelete = st.selectbox("What item do you want to permanently delete", options=list(all_items), index=None, placeholder= "Select item")

    if "show_confirm" not in st.session_state:
        st.session_state.show_confirm = False

    if st.button("Delete"):
        st.session_state.show_confirm = True

    if st.session_state.show_confirm:
        st.warning("Are you sure you want to delete this?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Delete"):
                if itemtodelete:
                    for category in list(inventory.keys()):
                        if itemtodelete in inventory[category]:
                            del inventory[category][itemtodelete]
                            break
                    st.success(f"{itemtodelete} deleted successfully.")
                st.session_state.show_confirm = False
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.show_confirm = False
                st.rerun()



if selected == "View History":
    st.header("History")
    if not history:
         st.warning("No transactions yet.")
    else:
         df_history = pd.DataFrame(history)
         st.dataframe(df_history)
