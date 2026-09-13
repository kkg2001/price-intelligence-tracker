import os

import requests
import streamlit as st

from database import get_all_products

API_URL = os.getenv("PRICE_INTELLIGENCE_API_URL","http://127.0.0.1:8000")

st.set_page_config(
    page_title="Price Intelligence Assistant",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Price Intelligence Assistant")

st.write("Ask questions about product prices, price trends, ""buy recommendations, and product suitability.")


@st.cache_data
def load_products():

    return get_all_products()

products = load_products()

if not products:

    st.error("No products found in the database.")
    st.stop()

# Product selection
product_options = {
    product["product_name"]: product["product_id"]
    for product in products
}


selected_product_name = st.selectbox(
    "Select a product",
    list(product_options.keys())
)


selected_product_id = product_options[
    selected_product_name
]


selected_product = next(
    product
    for product in products
    if product["product_id"] == selected_product_id
)


st.caption(
    f"Current price: "
    f"₹{selected_product['current_price']:,.0f}"
)

# User question
question = st.text_area(
    "What would you like to know?",
    placeholder=(
        "Example: Should I buy this product now?"
    ),
    height=100
)


# Ask Assistant
if st.button("Ask Assistant",type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        payload = {
            "product_id": selected_product_id,
            "question": question.strip()
        }
        endpoint = (f"{API_URL}/api/v1/query")
        with st.spinner("Analyzing product information..."):
            try:
                response = requests.post(
                    endpoint,
                    json=payload,
                    timeout=120
                )

                # Raise exception for HTTP 4xx/5xx
                response.raise_for_status()

                result = response.json()

                # Display final answer only
                st.subheader("Recommendation")
                st.write(result["answer"])

                # Developer details
                with st.expander("Agent execution details"):
                    st.write(f"LLM calls: "f"{result['llm_calls']}")

                    st.write(f"Tool calls: "f"{result['tool_calls']}")

                    st.write("Tools used: " + ", ".join(result["tools_used"]))

                    st.write(f"Status: "f"{result['status']}")

            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the FastAPI backend. ""Make sure the API server is running.")

            except requests.exceptions.Timeout:
                st.error("The request timed out." "Please try again.")

            except requests.exceptions.HTTPError:
                try:
                    error_detail = response.json()

                except Exception:
                    error_detail = response.text

                st.error(
                    f"API error: {error_detail}"
                )

            except Exception as error:
                st.error(f"Unexpected error: {error}")