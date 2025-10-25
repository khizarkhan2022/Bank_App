import streamlit as st

# =============== BANK SYSTEM =================
# Use Streamlit session_state to store data persistently
if "accounts" not in st.session_state:
    st.session_state["accounts"] = []
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

accounts = st.session_state["accounts"]

# ---------- FUNCTIONS ----------
def create_account(name, pin, account_number, balance):
    for acc in accounts:
        if acc["account_number"] == account_number:
            st.error("Account number already exists!")
            return
    serial_number = len(accounts) + 1
    account = {
        "serial_number": serial_number,
        "name": name,
        "pin": pin,
        "account_number": account_number,
        "balance": balance
    }
    accounts.append(account)
    st.success(f"Account Created Successfully! Serial No: {serial_number}")

def find_account(name, pin):
    for i in accounts:
        if i["name"].lower() == name.lower() and i["pin"] == pin:
            return i
    return None

def find_with_name(name):
    for i in accounts:
        if i["name"].lower() == name.lower():
            st.info(f"Account Found: {i}")
            return
    st.error("Account Not Found!")

def deposit_amount(name, amount):
    for i in accounts:
        if i["name"].lower() == name.lower():
            i["balance"] += amount
            st.success(f"💰 Deposit Successful! New Balance: PKR {i['balance']}")
            return
    st.error("Account Not Found.")

def withdraw_amount(name, pin, amount):
    for i in accounts:
        if i["name"].lower() == name.lower() and i["pin"] == pin:
            if amount > i["balance"]:
                st.error(" Insufficient Balance.")
                return
            i["balance"] -= amount
            st.success(f"Withdraw Successful! Remaining Balance: PKR {i['balance']}")
            return
    st.error("Account Not Found.")

def transfer_amount(sender_name, sender_pin, receiver_ac, amount):
    sender = None
    receiver = None
    for i in accounts:
        if i["name"].lower() == sender_name.lower() and i["pin"] == sender_pin:
            sender = i
        if i["account_number"] == receiver_ac:
            receiver = i
    if not sender:
        st.error("Sender account not found.")
        return
    if not receiver:
        st.error("Receiver account not found.")
        return
    if amount > sender["balance"]:
        st.error("Insufficient Balance for Transfer.")
    else:
        sender["balance"] -= amount
        receiver["balance"] += amount
        st.success(f"Transfer Successful! Remaining Balance: PKR {sender['balance']}")

def login(name, pin):
    user = find_account(name, pin)
    if user:
        st.session_state["logged_in_user"] = user
        st.success(f" Login Successful! Welcome, {user['name']}.")
    else:
        st.error("Invalid name or PIN.")

def logout():
    if st.session_state["logged_in_user"]:
        st.info(f"{st.session_state['logged_in_user']['name']} has logged out.")
        st.session_state["logged_in_user"] = None
    else:
        st.warning("No user is currently logged in.")

# =============== STREAMLIT UI ===============
st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox("Choose Action", 
                            ["Create Account", "Login", "Check Balance", 
                             "Deposit", "Withdraw", "Transfer", 
                             "Find Account", "Logout"])

if menu == "Create Account":
    name = st.text_input("Enter Name")
    pin = st.number_input("Enter PIN", step=1, format="%d")
    account_number = st.number_input("Enter Account Number", step=1, format="%d")
    balance = st.number_input("Enter Opening Balance", step=100.0)
    if st.button("Create Account"):
        create_account(name, pin, account_number, balance)

elif menu == "Login":
    name = st.text_input("Enter Name")
    pin = st.number_input("Enter PIN", step=1, format="%d")
    if st.button("Login"):
        login(name, pin)

elif menu == "Check Balance":
    user = st.session_state["logged_in_user"]
    if user:
        st.info(f"💰 Your Balance is: PKR {user['balance']}")
    else:
        st.warning("Please login first.")

elif menu == "Deposit":
    user = st.session_state["logged_in_user"]
    if user:
        amount = st.number_input("Enter Deposit Amount", step=100.0)
        if st.button("Deposit"):
            deposit_amount(user["name"], amount)
    else:
        st.warning("Please login first.")

elif menu == "Withdraw":
    user = st.session_state["logged_in_user"]
    if user:
        amount = st.number_input("Enter Withdraw Amount", step=100.0)
        if st.button("Withdraw"):
            withdraw_amount(user["name"], user["pin"], amount)
    else:
        st.warning("Please login first.")

elif menu == "Transfer":
    user = st.session_state["logged_in_user"]
    if user:
        receiver = st.number_input("Enter Receiver Account Number", step=1, format="%d")
        amount = st.number_input("Enter Amount to Transfer", step=100.0)
        if st.button("Transfer"):
            transfer_amount(user["name"], user["pin"], receiver, amount)
    else:
        st.warning("Please login first.")

elif menu == "Find Account":
    name = st.text_input("Enter Name to Search")
    if st.button("Search"):
        find_with_name(name)

elif menu == "Logout":
    logout()
