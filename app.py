import streamlit as st
from bank_backend import Bank

st.set_page_config(page_title="Neo Bank", layout="wide")

# ----------- SESSION -----------
if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

if "show_pin" not in st.session_state:
    st.session_state.show_pin = False

# ----------- CSS -----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #020617, #0ea5e9);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.card {
    background: rgba(255,255,255,0.07);
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
}
.title {
    text-align:center;
    font-size: 42px;
    color: white;
    font-weight: bold;
}
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown("<div class='title'>💳 Neo Bank</div>", unsafe_allow_html=True)

# ----------- NAVBAR -----------
menu = [
    "🏠 Dashboard",
    "➕ Create",
    "💰 Deposit",
    "💸 Withdraw",
    "📄 Details",
    "📘 Passbook",
    "❌ Delete"
]

choice = st.radio("", menu, index=menu.index(st.session_state.page), horizontal=True)
st.session_state.page = choice

# ----------- DASHBOARD (PRO UI) -----------
if choice == "🏠 Dashboard":
    st.subheader("📊 Overview")

    # 🔥 TOP STATS
    col1, col2, col3 = st.columns(3)

    total_users = len(Bank.data)

    col1.metric("👥 Total Users", total_users)
    col2.metric("🏦 Bank Status", "Active")
    col3.metric("🔐 Security", "Protected")

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 MAIN GRID
    left, right = st.columns([2, 1])

    # -------- LEFT SIDE --------
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("💰 Check Your Balance")

        acc = st.text_input("Enter Account Number", key="db1")

        if st.button("View Balance"):
            st.session_state.show_pin = True

        if st.session_state.show_pin:
            pin = st.text_input("Enter PIN", type="password", key="db2")

            if st.button("Verify PIN"):
                user = Bank.find_user(acc.strip(), pin)

                if user:
                    st.success(f"💰 Your Balance: ₹{user['balance']}")
                else:
                    st.error("Invalid Account Number or PIN")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- RIGHT SIDE --------
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("⚡ Quick Actions")

        if st.button("➕ Create Account"):
            st.session_state.page = "➕ Create"

        if st.button("💰 Deposit"):
            st.session_state.page = "💰 Deposit"

        if st.button("💸 Withdraw"):
            st.session_state.page = "💸 Withdraw"

        if st.button("📘 Passbook"):
            st.session_state.page = "📘 Passbook"

        st.markdown("</div>", unsafe_allow_html=True)

    # 🔥 BOTTOM SECTION
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🏦 About Neo Bank")

    st.write("🚀 Fast • 🔐 Secure • 💳 Digital Banking Experience")
    st.write("✔ Create account instantly")
    st.write("✔ Deposit & Withdraw easily")
    st.write("✔ Track transactions in Passbook")

    st.markdown("</div>", unsafe_allow_html=True)

   

# ----------- CREATE -----------
elif choice == "➕ Create":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Create Account")

    name = st.text_input("Name", key="c1")
    age = st.number_input("Age", min_value=1, key="c2")
    email = st.text_input("Email", key="c3")
    pin = st.text_input("PIN", type="password", key="c4")

    if st.button("Create Account"):
        result = Bank.create_account(name, age, email, pin)
        if isinstance(result, dict):
            st.success(f"Account Created 🎉\nAccount No: {result['accountNo']}")
        else:
            st.error(result)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DEPOSIT -----------
elif choice == "💰 Deposit":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Deposit Money")

    acc = st.text_input("Account No", key="d1")
    pin = st.text_input("PIN", type="password", key="d2")
    amount = st.number_input("Amount", key="d3")

    if st.button("Deposit"):
        msg = Bank.deposit(acc.strip(), pin, amount)
        st.success(msg) if "successful" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- WITHDRAW -----------
elif choice == "💸 Withdraw":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Withdraw Money")

    acc = st.text_input("Account No", key="w1")
    pin = st.text_input("PIN", type="password", key="w2")
    amount = st.number_input("Amount", key="w3")

    if st.button("Withdraw"):
        msg = Bank.withdraw(acc.strip(), pin, amount)
        st.success(msg) if "successful" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DETAILS -----------
elif choice == "📄 Details":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Account Details")

    acc = st.text_input("Account No", key="s1")
    pin = st.text_input("PIN", type="password", key="s2")

    if st.button("Check Details"):
        user = Bank.find_user(acc.strip(), pin)
        if user:
            st.write("👤 Name:", user["name"])
            st.write("📧 Email:", user["Email"])
        else:
            st.error("User not found")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- PASSBOOK -----------
elif choice == "📘 Passbook":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Passbook")

    email = st.text_input("Email", key="p1")
    pin = st.text_input("PIN", type="password", key="p2")

    if st.button("View Passbook"):
        user = Bank.get_passbook(email, pin)

        if user:
            st.success("Account Found")

            st.write("👤 Name:", user["name"])
            st.write("🏦 Account No:", user["accountNo"])
            st.write("💰 Balance:", f"₹{user['balance']}")

            st.write("### Transactions")

            if user["transactions"]:
                for t in user["transactions"]:
                    if t["type"] == "Deposit":
                        st.success(f"🟢 +₹{t['amount']} ({t['time']})")
                    else:
                        st.error(f"🔴 -₹{t['amount']} ({t['time']})")
            else:
                st.info("No transactions")

        else:
            st.error("Invalid details")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DELETE -----------
elif choice == "❌ Delete":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Delete Account")

    acc = st.text_input("Account No", key="del1")
    pin = st.text_input("PIN", type="password", key="del2")

    if st.button("Delete Account"):
        msg = Bank.delete(acc.strip(), pin)
        st.success(msg) if "deleted" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)