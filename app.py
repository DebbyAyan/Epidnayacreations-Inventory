import streamlit as st

# ---------------- LOAD INVENTORY ----------------
def load_inventory():
    inventory = {}

    try:
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()

            if line != "":
                item, category, quantity = line.split(",")

                inventory[item] = {
                    "category": category,
                    "quantity": int(quantity)
                }

    except:
        pass

    return inventory


# ---------------- SAVE INVENTORY ----------------
def save_inventory(inventory):
    file = open("inventory.txt", "w")

    for item, details in inventory.items():
        line = item + "," + details["category"] + "," + str(details["quantity"]) + "\n"
        file.write(line)

    file.close()


# ---------------- LOAD DATA ----------------
inventory = load_inventory()

# ---------------- TITLE ----------------
st.title("Leather Business Inventory System")

# ---------------- MENU ----------------
menu = st.sidebar.selectbox(
    "Choose an option",
    [
        "Add Stock",
        "Remove Stock",
        "View Stock"
    ]
)

# ---------------- ADD STOCK ----------------
if menu == "Add Stock":

    st.header("Add Stock")

    item = st.text_input("Item Name")

    category = st.selectbox(
        "Category",
        ["Bag", "Material"]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Add Stock"):

        if item in inventory:
            inventory[item]["quantity"] += quantity

        else:
            inventory[item] = {
                "category": category,
                "quantity": quantity
            }

        save_inventory(inventory)

        st.success("Stock Added Successfully")


# ---------------- REMOVE STOCK ----------------
elif menu == "Remove Stock":

    st.header("Remove Stock")

    item = st.text_input("Item Name")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Remove Stock"):

        if item in inventory:

            if inventory[item]["quantity"] >= quantity:

                inventory[item]["quantity"] -= quantity

                save_inventory(inventory)

                st.success("Stock Removed")

            else:
                st.error("Not enough stock")

        else:
            st.error("Item not found")


# ---------------- VIEW STOCK ----------------
elif menu == "View Stock":

    st.header("Current Inventory")

    if inventory:

        for item, details in inventory.items():

            st.write(
                f"**{item}** | Category: {details['category']} | Quantity: {details['quantity']}"
            )

    else:
        st.warning("No stock available")