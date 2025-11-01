import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮")

st.title("🧮 Simple Streamlit Calculator")

# Inputs
num1 = st.number_input("Enter first number:", format="%.10f")
num2 = st.number_input("Enter second number:", format="%.10f")

operation = st.selectbox(
    "Select Operation:",
    ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]
)

# Process result
result = None
error = None

if st.button("Calculate"):
    try:
        if operation == "Addition (+)":
            result = num1 + num2

        elif operation == "Subtraction (-)":
            result = num1 - num2

        elif operation == "Multiplication (×)":
            result = num1 * num2

        elif operation == "Division (÷)":
            if num2 == 0:
                error = "❌ Cannot divide by zero."
            else:
                result = num1 / num2

    except Exception as e:
        error = f"❌ Error: {e}"

# Display output
if error:
    st.error(error)
elif result is not None:
    st.success(f"✅ Result: **{result}**")
