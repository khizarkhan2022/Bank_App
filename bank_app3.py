import streamlit as st

# =============== BANK SYSTEM =================
if "accounts" not in st.session_state:
    st.session_state["accounts"] = []
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "account_created_message" not in st.session_state:
    st.session_state["account_created_message"] = False

accounts = st.session_state["accounts"]

# ---------- FUNCTIONS ----------
def create_account(name, pin, account_number, balance):
    for acc in accounts:
        if acc["account_number"] == account_number:
            st.error(" Account number already exists!")
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
    st.session_state["account_created_message"] = True


def find_account(name, pin):
    for acc in accounts:
        if acc["name"].lower() == name.lower() and acc["pin"] == pin:
            return acc
    return None


def deposit_amount(name, amount):
    for acc in accounts:
        if acc["name"].lower() == name.lower():
            acc["balance"] += amount
            st.success(f" Deposit Successful! New Balance: PKR {acc['balance']}")
            return
    st.error(" Account Not Found.")


def withdraw_amount(name, pin, amount):
    for acc in accounts:
        if acc["name"].lower() == name.lower() and acc["pin"] == pin:
            if amount > acc["balance"]:
                st.error(" Insufficient Balance.")
                return
            acc["balance"] -= amount
            st.success(f" Withdraw Successful! Remaining Balance: PKR {acc['balance']}")
            return
    st.error(" Account Not Found.")


def transfer_amount(sender_name, sender_pin, receiver_ac, amount):
    sender = None
    receiver = None
    for acc in accounts:
        if acc["name"].lower() == sender_name.lower() and acc["pin"] == sender_pin:
            sender = acc
        if acc["account_number"] == receiver_ac:
            receiver = acc

    if not sender:
        st.error(" Sender account not found.")
        return
    if not receiver:
        st.error(" Receiver account not found.")
        return
    if amount > sender["balance"]:
        st.error(" Insufficient Balance for Transfer.")
        return

    sender["balance"] -= amount
    receiver["balance"] += amount
    st.success(f" Transfer Successful! Remaining Balance: PKR {sender['balance']}")


def login(name, pin):
    user = find_account(name, pin)
    if user:
        st.session_state["logged_in_user"] = user
        st.success(f" Login Successful! Welcome, {user['name']}.")
        st.session_state["login_message"] = True
        st.rerun()
    else:
        st.error(" Invalid name or PIN.")


def logout():
    if st.session_state["logged_in_user"]:
        st.info(f"{st.session_state['logged_in_user']['name']} has logged out.")
        st.session_state["logged_in_user"] = None
        st.rerun()
    else:
        st.warning(" No user is currently logged in.")


# =============== STREAMLIT UI ===============
st.title("Simple Bank Management System")

# ---------- SIDEBAR MENU ----------
user = st.session_state["logged_in_user"]

if user:
    menu = st.sidebar.selectbox(
        "Choose Action",
        ["Welcome", "Deposit", "Withdraw", "Transfer", "Find Account", "Logout"]
    )
else:
    menu = st.sidebar.selectbox(
        "Choose Action",
        ["Create Account", "Login"]
    )

# ---------- CREATE ACCOUNT ----------
if menu == "Create Account":
    name = st.text_input("Enter Name", key="name_input")
    pin = st.number_input("Enter PIN", step=1, format="%d", key="pin_input")
    account_number = st.number_input("Enter Account Number", step=1, format="%d", key="account_input")
    balance = st.number_input("Enter Opening Balance", step=100.0, key="balance_input")

    if st.button("Create Account"):
        create_account(name, pin, account_number, balance)
        for key in ["name_input", "pin_input", "account_input", "balance_input"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # Show success message after rerun
    if st.session_state["account_created_message"]:
        st.success("🎉 Account Created Successfully!")
        st.session_state["account_created_message"] = False

# ---------- LOGIN ----------
elif menu == "Login":
    name = st.text_input("Enter Name")
    pin = st.number_input("Enter PIN", step=1, format="%d")
    if st.button("Login"):
        login(name, pin)
    
# ---------- WELCOME (AFTER LOGIN) ----------
elif menu == "Welcome":
    st.markdown(f"###  Welcome, **{user['name']}!**")
    st.info("You are now logged into your account.")

# ---------- DEPOSIT ----------
elif menu == "Deposit":
    amount = st.number_input("Enter Deposit Amount", step=100.0)
    if st.button("Deposit"):
        deposit_amount(user["name"], amount)

# ---------- WITHDRAW ----------
elif menu == "Withdraw":
    amount = st.number_input("Enter Withdraw Amount", step=100.0)
    if st.button("Withdraw"):
        withdraw_amount(user["name"], user["pin"], amount)

# ---------- TRANSFER ----------
elif menu == "Transfer":
    receiver = st.number_input("Enter Receiver Account Number", step=1, format="%d")
    amount = st.number_input("Enter Amount to Transfer", step=100.0)
    if st.button("Transfer"):
        transfer_amount(user["name"], user["pin"], receiver, amount)

# ---------- FIND ACCOUNT ----------
elif menu == "Find Account":
    search_name = st.text_input("Enter Name to Search")
    if st.button("Search"):
        found = False
        for acc in accounts:
            if acc["name"].lower() == search_name.lower():
                st.info(f"Account Found — {acc}")
                found = True
        if not found:
            st.error(" Account Not Found!")

# ---------- LOGOUT ----------
elif menu == "Logout":
    logout()
