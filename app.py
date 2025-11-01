import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Modern Calculator",
    page_icon="🧮",
    layout="centered",
)

# -----------------------------
# Custom CSS for Better UI
# -----------------------------
st.markdown(
    """
    <style>
        .calculator-box {
            background: #ffffff10;
            padding: 25px;
            border-radius: 18px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid #ffffff20;
            max-width: 450px;
            margin: auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .stButton > button {
            width: 100%;
            height: 48px;
            border-radius: 12px;
            border: none;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
        }

        .calculate-btn {
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
        }

        .calculate-btn:hover {
            background: linear-gradient(135deg, #43A047, #1B5E20);
        }

        .result-box {
            padding: 20px;
            border-radius: 12px;
            background: #4caf5033;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        }

        .error-box {
            padding: 20px;
            border-radius: 12px;
            background: #ff525233;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# UI Layout
# -----------------------------
st.title("🧮 Modern Streamlit Calculator")
st.write("A clean, minimal and user-friendly calculator built with Streamlit.")

st.markdown('<div class="calculator-box">', unsafe_allow_html=True)

num1 = st.number_input("Enter first number", format="%.10f")
num2 = st.number_input("Enter second number", format="%.10f")

operation = st.selectbox(
    "Choose Operation",
    ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]
)

result, error = None, None

# -----------------------------
# Calculation Button
# -----------------------------
calc_col = st.columns([1])[0]
with calc_col:
    calc_btn = st.button("Calculate", key="calc_btn")

# -----------------------------
# Logic
# -----------------------------
if calc_btn:
    try:
        if operation == "Addition (+)":
            result = num1 + num2
        elif operation == "Subtraction (-)":
            result = num1 - num2
        elif operation == "Multiplication (×)":
            result = num1 * num2
        elif operation == "Division (÷)":
            if num2 == 0:
                error = "Cannot divide by zero."
            else:
                result = num1 / num2

    except Exception as e:
        error = f"Error: {e}"

# -----------------------------
# Output
# -----------------------------
if error:
    st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
elif result is not None:
    st.markdown(f'<div class="result-box">✅ Result: {result}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
