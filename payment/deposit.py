import streamlit as st
import stripe

# Stripe ayarları
stripe_secret = st.secrets["stripe"]["secret_key"]
stripe_publishable = st.secrets["stripe"]["publishable_key"]

# Fiyat planı (USD cinsinden örnek)
DEPOSIT_AMOUNTS = [5, 10, 20, 50, 100]  # Dolar

# Kullanıcı bakiyesini session'da saklıyoruz
def get_balance():
    return st.session_state.get("balance", 0.0)

def update_balance(amount):
    st.session_state["balance"] = get_balance() + amount


def deposit_ui():
    st.subheader("💳 Deposit to Your Account")

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_amount = st.selectbox("Choose deposit amount (USD)", DEPOSIT_AMOUNTS)
    with col2:
        st.markdown(f"### 💰 Amount: ${selected_amount}")

    st.markdown("---")

    if "payment_success" not in st.session_state:
        st.session_state["payment_success"] = False

    # Stripe Checkout
    if st.button("💸 Deposit via Stripe"):
        try:
            # Stripe ödeme linki oluştur
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Credit Top-Up",
                        },
                        "unit_amount": selected_amount * 100,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=st.secrets["SUCCESS_URL"],
                cancel_url=st.secrets["CANCEL_URL"],
            )

            st.success("✅ Redirecting to payment page...")
            st.markdown(f"[👉 Click here to pay]({session.url})", unsafe_allow_html=True)
            st.stop()

        except Exception as e:
            st.error(f"❌ Payment error: {e}")

    # Başarılı ödeme sonrası manual tetikleme (örnek amaçlı)
    if st.button("✅ I completed the payment"):
        update_balance(selected_amount)
        st.session_state["payment_success"] = True
        st.success(f"✅ ${selected_amount} added to your account!")

    # Güncel bakiye gösterimi
    st.markdown("---")
    st.markdown(f"### 💼 Current Balance: **${get_balance():.2f}**")

