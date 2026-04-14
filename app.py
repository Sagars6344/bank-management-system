import streamlit as st
from bank_backend import Bank

st.set_page_config(page_title="Neo Bank", layout="wide")

# ----------- CSS GOD MODE -----------
st.markdown("""
<style>

/* Background Animation */
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

/* Glass Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
    transition: 0.4s;
}
.card:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px #22c55e;
}

/* Neon Buttons */
.stButton>button {
    background: linear-gradient(45deg,#22c55e,#4ade80);
    border-radius: 12px;
    color: white;
    font-size: 18px;
    padding: 10px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 20px #22c55e;
}

/* Title Glow */
.title {
    font-size: 50px;
    text-align:center;
    font-weight: bold;
    color: white;
    text-shadow: 0 0 20px #22c55e;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
}

/* Inputs */
input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown("<div class='title'>💳 Neo Bank UI</div>", unsafe_allow_html=True)
st.markdown("### 🚀 Futuristic Banking Experience")

# ----------- SIDEBAR -----------
menu = ["🏠 Dashboard", "➕ Create", "💰 Deposit", "💸 Withdraw", "📄 Details", "❌ Delete"]
choice = st.sidebar.radio("Navigation", menu)

# ----------- DASHBOARD -----------
if choice == "🏠 Dashboard":
    st.subheader("📊 Overview")

    total_users = len(Bank.data)
    total_balance = sum([u["balance"] for u in Bank.data])

    col1, col2 = st.columns(2)
    col1.metric("👥 Total Users", total_users)
    col2.metric("💰 Total Bank Balance", f"₹{total_balance}")

# ----------- CREATE -----------
elif choice == "➕ Create":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
        st.spinner("Creating account...")
        result = Bank.create_account(name, age, email, pin)

        if isinstance(result, dict):
            st.success("Account Created 🎉")
            st.balloons()
        else:
            st.error(result)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DEPOSIT -----------
elif choice == "💰 Deposit":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount")

    if st.button("Deposit"):
        msg = Bank.deposit(acc.strip(), pin, amount)
        st.success(msg) if "successful" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- WITHDRAW -----------
elif choice == "💸 Withdraw":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount")

    if st.button("Withdraw"):
        msg = Bank.withdraw(acc.strip(), pin, amount)
        st.success(msg) if "successful" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DETAILS -----------
elif choice == "📄 Details":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        user = Bank.find_user(acc.strip(), pin)
        if user:
            st.metric("Balance", f"₹{user['balance']}")
            st.json(user)
        else:
            st.error("User not found")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------- DELETE -----------
elif choice == "❌ Delete":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        msg = Bank.delete(acc.strip(), pin)
        st.success(msg) if "deleted" in msg else st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)