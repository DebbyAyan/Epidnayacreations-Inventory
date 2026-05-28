import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Epidnayacreations Inventory System",
    page_icon="👜",
    layout="wide"
)

# Title
st.title("👜 Epidnayacreations Inventory System")
st.subheader("Bags Crafted to Perfection!")

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "history" not in st.session_state:
    st.session_state.history = []

inventory = st.session_state.inventory
history = st.session_state.history


# ---------------- FUNCTIONS ---------------- #

# Add Item
def add_item(category, item, quantity, price):
    category = category.capitalize()
    item = item.capitalize()

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

    date = datetime.now().strftime("%Y-%m-%d")

    history.append({
        "type": "New Item",
        "category": category,
        "item": item,
        "quantity": quantity,
        "price": price,
        "date": date
    })

    st.success(f"{item} added successfully under {category}.")


# Remove Item
def remove_item(category, item, quantity):
    category = category.capitalize()
    item = item.capitalize()

    if category in inventory and item in inventory[category]:

        if inventory[category][item]["quantity"] >= quantity:

            inventory[category][item]["quantity"] -= quantity

            date = datetime.now().strftime("%Y-%m-%d")

            history.append({
                "type": "Sale",
                "category": category,
                "item": item,
                "quantity": quantity,
                "price": inventory[category][item]["price"],
                "date": date
            })

            st.success(f"{quantity} {item}(s) removed successfully.")

        else:
            st.error("Not enough quantity available.")

    else:
        st.error("Item not found.")


# Delete Item
def delete_item(category, item):
    category = category.capitalize()
    item = item.capitalize()

    if category in inventory and item in inventory[category]:
        del inventory[category][item]
        st.success(f"{item} deleted successfully.")
    else:
        st.error("Item not found.")


# ---------------- SIDEBAR ---------------- #

menu = st.sidebar.selectbox(
    "Choose an Option",
    [
        "View Inventory",
        "View Inventory by Category",
        "View Single Item",
        "Add Item",
        "Remove Item (Sales)",
        "Delete Item",
        "Transaction History"
    ]
)


# ---------------- VIEW INVENTORY ---------------- #

if menu == "View Inventory":

    st.header("📦 Full Inventory")

    if not inventory:
        st.warning("Inventory is empty.")

    else:

        total_bag_value = 0
        total_material_value = 0

        # Bags
        if "Bag" in inventory:

            st.subheader("👜 Bags")

            bag_data = []

            for item in inventory["Bag"]:

                qty = inventory["Bag"][item]["quantity"]
                price = inventory["Bag"][item]["price"]
                value = qty * price

                total_bag_value += value

                bag_data.append({
                    "Item": item,
                    "Quantity": qty,
                    "Price": price,
                    "Total Value": value
                })

            st.dataframe(pd.DataFrame(bag_data))
            st.info(f"Total Bag Value: ₦{total_bag_value:,.2f}")

        else:
            st.warning("No Bags available.")

        # Materials
        if "Material" in inventory:

            st.subheader("🧵 Materials")

            material_data = []

            for item in inventory["Material"]:

                qty = inventory["Material"][item]["quantity"]
                price = inventory["Material"][item]["price"]
                value = qty * price

                total_material_value += value

                material_data.append({
                    "Item": item,
                    "Quantity": qty,
                    "Price": price,
                    "Total Value": value
                })

            st.dataframe(pd.DataFrame(material_data))
            st.info(f"Total Material Value: ₦{total_material_value:,.2f}")

        else:
            st.warning("No Materials available.")


# ---------------- VIEW CATEGORY ---------------- #

elif menu == "View Inventory by Category":

    st.header("📂 View Category")

    category = st.selectbox(
        "Select Category",
        ["Bag", "Material"]
    )

    if st.button("View Category"):

        if category in inventory:

            category_data = []

            for item in inventory[category]:

                category_data.append({
                    "Item": item,
                    "Quantity": inventory[category][item]["quantity"],
                    "Price": inventory[category][item]["price"]
                })

            st.dataframe(pd.DataFrame(category_data))

        else:
            st.warning("Category not found.")


# ---------------- VIEW SINGLE ITEM ---------------- #

elif menu == "View Single Item":

    st.header("🔍 View Item")

    category = st.selectbox(
        "Select Category",
        ["Bag", "Material"]
    )

    item = st.text_input("Enter Item Name")

    if st.button("Check Item"):

        item = item.capitalize()

        if category in inventory and item in inventory[category]:

            st.success("Item Found")

            st.write(f"### Item: {item}")
            st.write(f"Quantity: {inventory[category][item]['quantity']}")
            st.write(f"Price: ₦{inventory[category][item]['price']}")

        else:
            st.error("Item not available.")


# ---------------- ADD ITEM ---------------- #

elif menu == "Add Item":

    st.header("➕ Add Item")

    category = st.selectbox(
        "Select Category",
        ["Bag", "Material"]
    )

    item = st.text_input("Enter Item Name")

    quantity = st.number_input(
        "Enter Quantity",
        min_value=0.0,
        step=1.0
    )

    price = st.number_input(
        "Enter Price",
        min_value=0.0,
        step=100.0
    )

    if st.button("Add Item"):

        if item.strip() == "":
            st.error("Please enter item name.")

        else:
            add_item(category, item, quantity, price)


# ---------------- REMOVE ITEM ---------------- #

elif menu == "Remove Item (Sales)":

    st.header("➖ Remove Item / Sales")

    category = st.selectbox(
        "Select Category",
        ["Bag", "Material"]
    )

    item = st.text_input("Enter Item Name")

    quantity = st.number_input(
        "Enter Quantity to Remove",
        min_value=0.0,
        step=1.0
    )

    if st.button("Remove Item"):

        if item.strip() == "":
            st.error("Please enter item name.")

        else:
            remove_item(category, item, quantity)


# ---------------- DELETE ITEM ---------------- #

elif menu == "Delete Item":

    st.header("🗑 Delete Item")

    category = st.selectbox(
        "Select Category",
        ["Bag", "Material"]
    )

    item = st.text_input("Enter Item Name")

    if st.button("Delete Item"):

        if item.strip() == "":
            st.error("Please enter item name.")

        else:
            delete_item(category, item)


# ---------------- HISTORY ---------------- #

elif menu == "Transaction History":

    st.header("📜 Transaction History")

    if not history:
        st.warning("No transactions yet.")

    else:
        history_df = pd.DataFrame(history)
        st.dataframe(history_df)


# ---------------- FOOTER ---------------- #

st.sidebar.markdown("---")
st.sidebar.info("Epidnayacreations Inventory Management System")