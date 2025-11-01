# StreamLit-Calculator

A small, friendly calculator web app built with Streamlit.

Features
- Safe expression evaluation using Python's AST (supports +, -, *, /, %, **, parentheses)
- Two modes: Basic (two-number operations) and Advanced (free-form expressions)
- Calculation history (recent first) stored in session state
- Easy copy of results and small UI improvements for accessibility

Quick start
1. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

Notes
- The app uses a restricted evaluator to prevent arbitrary code execution; only arithmetic expressions are allowed.
- History is kept in the user's Streamlit session and is limited to recent entries.

If you'd like more features (themes, keyboard shortcuts, persisting history to disk), I can add them next.
