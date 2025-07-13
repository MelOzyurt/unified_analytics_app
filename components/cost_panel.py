# components/cost_panel.py

import streamlit as st
from config.pricing_config import calculate_price

def show_cost_panel(analysis_type: str):
    with st.expander("💰 Pricing & Balance", expanded=True):
        st.subheader("Analysis Cost Summary")

        if analysis_type:
            cost = calculate_price(analysis_type)
            balance = st.session_state.get("balance", 0.0)

            st.write(f"🧠 **Selected Analysis**: `{analysis_type}`")
            st.write(f"💵 **Estimated Cost**: `${cost:.2f}`")
            st.write(f"💼 **Your Balance**: `${balance:.2f}`")

            if balance >= cost:
                st.success("✅ You have enough balance to proceed.")
            else:
                st.error("❌ Insufficient balance. Please top up.")

        else:
            st.info("Select an analysis type to see the cost.")
