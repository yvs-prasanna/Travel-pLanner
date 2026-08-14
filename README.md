# JavaScript → Python Model Project

This project demonstrates the architecture:

Browser UI
   ↓
JavaScript fetch()
   ↓
Python FastAPI endpoint
   ↓
Python model
   ↓
JSON response
   ↓
JavaScript displays the result

## Structure

python-js-project/
├── frontend/
│   └── js/
│       ├── index.html
│       └── index.css
├── backend/
│   ├── main.py
│   └── requirements.txt
└── README.md

## 1. Install Python dependencies

Open a terminal in the `backend` folder:

```powershell
pip install -r requirements.txt
```

## 2. Start the Python backend

From the `backend` folder:

```powershell
python -m uvicorn main:app --reload --port 8000
```

The API will run at:

http://127.0.0.1:8000

## 3. Open the frontend

Open:

```text
frontend/js/index.html
```

Or from PowerShell, inside `frontend/js`:

```powershell
Start-Process ".\index.html"
```

## Important

JavaScript running in a browser cannot directly execute an arbitrary Python file.

Instead, JavaScript sends an HTTP request to a Python backend. The Python backend executes the model and sends the result back as JSON.

For example:

JS:
POST /predict
{
    "user_input": "Plan a trip to Hyderabad"
}

Python:
runs the model

Python response:
{
    "result": "..."
}

JS:
displays the result.

## Adding Gemini / LangChain

Put your actual model code inside:

```python
def run_model(user_input: str):
    ...
```

For example, this function can call your LangChain + Google Gemini implementation.
Keep API keys in environment variables rather than putting them in JavaScript.
