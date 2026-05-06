# Data Analyst Agent

An autonomous AI agent that analyzes data files using natural language.
Built with Python, Groq (LLaMA 3.3 70B), FastAPI, and Streamlit.
Built the agent loop from scratch without frameworks to deeply understand how agents work; the same patterns LangChain and LlamaIndex use internally.

## What it does
- Load any CSV or Excel file
- Ask questions in plain English
- Agent writes and executes Python/pandas code automatically
- Self-corrects on errors and retries
- Generates and saves matplotlib charts
- Remembers context across follow-up questions

## Stack
- LLM: Groq API (llama-3.3-70b-versatile)
- Backend: FastAPI
- Frontend: Streamlit
- Data: pandas, matplotlib

## How to run
1. Add your Groq API key to `.env`
2. Start the API: `uvicorn api:app --reload`
3. Start the UI: `streamlit run app.py`
4. Upload a CSV and start asking questions