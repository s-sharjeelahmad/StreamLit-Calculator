import ast
import operator as op
import time
import json
from functools import lru_cache

import streamlit as st


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Modern Calculator", page_icon="🧮", layout="centered")


# -----------------------------
# Safe expression evaluation (AST-based)
# Supports + - * / ** % and parentheses; prevents arbitrary code execution
# -----------------------------

# supported operators mapping
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.Num):  # python <3.8 compatibility
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            # guard division by zero
            if op_type is ast.Div and right == 0:
                raise ZeroDivisionError("division by zero")
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")
    raise ValueError(f"Unsupported expression: {type(node)}")


@lru_cache(maxsize=256)
def safe_eval(expression: str):
    """Safely evaluate a simple arithmetic expression and return a float/int result.

    Raises ValueError or ZeroDivisionError on invalid input.
    """
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")
    if len(expr) > 300:
        raise ValueError("Expression too long")
    # parse AST
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid expression syntax") from e
    # count nodes to avoid very deep/complex expressions
    node_count = sum(1 for _ in ast.walk(parsed))
    if node_count > 200:
        raise ValueError("Expression too complex")
    return _eval_ast(parsed)


# -----------------------------
# Helper: format result
# -----------------------------


def fmt_res(value):
    if isinstance(value, float):
        # show up to 10 significant digits, strip trailing zeros
        return f"{value:.10g}"
    return str(value)


# -----------------------------
# App UI and logic
# -----------------------------

st.title("🧮 Modern Streamlit Calculator")
st.write("Fast, safe and accessible calculator. Enter an expression or use the basic mode.")


if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {expr, result, time}


def add_to_history(expr, result):
    st.session_state.history.insert(0, {"expr": expr, "result": fmt_res(result), "time": time.time()})
    # keep history bounded
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]


with st.form(key="calc_form"):
    mode = st.radio("Mode", ["Basic (two numbers)", "Advanced (expression)"], index=1)

    result = None
    error = None

    if mode.startswith("Basic"):
        c1, c2 = st.columns(2)
        with c1:
            a = st.number_input("First number", key="a", format="%.6f")
        with c2:
            b = st.number_input("Second number", key="b", format="%.6f")

        op_choice = st.selectbox("Operation", ["+", "-", "*", "/", "%", "**"], index=0)

        submit = st.form_submit_button("Calculate")
        if submit:
            try:
                expr = f"({a}){op_choice}({b})"
                result = safe_eval(expr)
                add_to_history(expr, result)
            except Exception as e:
                error = str(e)

    else:  # Advanced expression
        expr = st.text_input("Expression", value="2+2*3", placeholder="e.g. (12.5 + 3) / 4 - 2**3")
        submit = st.form_submit_button("Evaluate")
        if submit:
            try:
                result = safe_eval(expr)
                add_to_history(expr, result)
            except Exception as e:
                error = str(e)

# show result / error
if error:
    st.error(f"{error}")
elif result is not None:
    st.success(f"Result: {fmt_res(result)}")
    # show a copyable field and a small copy button
    st.text_input("Copy result", value=fmt_res(result), key="copy_result", help="Use Ctrl+C to copy")
    # small HTML copy button using components (progressive enhancement)
    try:
        import streamlit.components.v1 as components

        js_result = json.dumps(fmt_res(result))
        components.html(
            f"""
            <button style="padding:8px 14px;border-radius:8px;background:#4CAF50;color:white;border:none;cursor:pointer;"
            onclick="navigator.clipboard.writeText({js_result}).then(()=>{{ this.innerText='Copied'; }})">Copy</button>
            """,
            height=50,
        )
    except Exception:
        pass

# history and controls
with st.expander("History (recent first)"):
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["time"]))
            st.markdown(f"**{i+1}.** `{item['expr']}` → `{item['result']}`  \n_{ts}_")
    else:
        st.info("No history yet — your recent calculations will appear here.")

    cols = st.columns([1, 1])
    if cols[0].button("Clear history"):
        st.session_state.history = []
        st.experimental_rerun()

    if cols[1].button("Copy last result"):
        if st.session_state.history:
            st.session_state.copy_result = st.session_state.history[0]["result"]
            st.success("Last result copied to the copy field above — use Ctrl+C to copy to clipboard.")
        else:
            st.warning("No result to copy")


# footer small notes
st.markdown(
    "---\n"
    "Built with Streamlit. Expression evaluation is restricted to arithmetic operators for safety."
)

