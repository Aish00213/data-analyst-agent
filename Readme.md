#  Data Analyst Agent

An AI-powered data analysis agent that lets users explore CSV and Excel files using natural language.

Instead of manually writing pandas code, users can ask questions in plain English. The agent generates Python code, executes it, analyzes the result, and can recover from execution errors by revising its approach.

The agent orchestration loop was implemented **without LangChain, LlamaIndex, or other agent frameworks** to understand the core mechanics of tool execution, iteration, error handling, and conversational context.

---

##  What It Does

Upload a CSV or Excel dataset and interact with it using natural language.

### Core capabilities

*  **CSV & Excel support** — Upload structured datasets directly
*  **Natural-language analysis** — Ask questions without writing pandas code
*  **Automatic Python generation** — The LLM generates pandas-based analysis code
*  **Code execution** — Generated Python code is executed against the uploaded dataset
*  **Error recovery** — Detects execution errors and retries with a corrected approach
*  **Visualization** — Generates and saves matplotlib charts when required
*  **Conversation context** — Supports follow-up questions using previous context
*  **API + UI** — FastAPI backend with a Streamlit interface

---

##  How the Agent Works

The project implements an iterative agent workflow:

```text
                    User Question
                          │
                          ▼
                   ┌─────────────┐
                   │     LLM     │
                   │ GPT-OSS 120B│
                   └──────┬──────┘
                          │
                          ▼
                  Generate Python
                  / pandas code
                          │
                          ▼
                ┌─────────────────┐
                │ Python Executor │
                └────────┬────────┘
                         │
                 ┌───────┴────────┐
                 │                │
              Success            Error
                 │                │
                 ▼                ▼
           Analyze result    Send error back
                 │            to the LLM
                 │                │
                 │                ▼
                 │          Generate corrected
                 │              code
                 │                │
                 └───────◄────────┘
                         │
                         ▼
                   Final Response
```

The key idea is an **iterative generate → execute → observe → retry loop** rather than a single LLM response.

---

##  Tech Stack

| Component     | Technology                 |
| ------------- | -------------------------- |
| LLM           | GPT-OSS 120B                |
| LLM Provider  | Groq API                   |
| Language      | Python                     |
| Data Analysis | Pandas                     |
| Visualization | Matplotlib                 |
| Backend       | FastAPI                    |
| Frontend      | Streamlit                  |
| Environment   | Python virtual environment |

---

##  Project Structure

```text
data-analyst-agent/
│
├── agent/
│   └── ...                 # Agent logic and orchestration
│
├── tools/
│   └── ...                 # Data analysis / execution tools
│
├── api.py                  # FastAPI backend
├── app_api_client.py       # Streamlit frontend (API mode — talks to api.py over HTTP)
├── main.py                 # Agent execution
├── streamlit_app.py        # Streamlit frontend (direct mode — calls the agent in-process)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aish00213/data-analyst-agent.git

cd data-analyst-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

**Never commit your API key to GitHub.**

Groq's free tier covers this project's usage — no paid plan required.

### 5. Run the app

You can run this project two ways:

#### Option 1: Direct mode (recommended, simplest)

Streamlit calls the agent directly — no separate backend needed.

```bash
streamlit run streamlit_app.py
```

#### Option 2: API mode

Runs a FastAPI backend that the Streamlit frontend calls over HTTP. Useful if you want to reuse the `/query` and `/upload` endpoints elsewhere (e.g. another frontend or service).

Terminal 1 — start the backend:

```bash
uvicorn api:app --reload
```

Terminal 2 — start the frontend:

```bash
streamlit run app_api_client.py
```

Open the Streamlit URL shown in your terminal and upload a CSV or Excel file.

---

##  Example Interaction

After uploading a dataset, users can ask questions such as:

```text
What are the top 10 products by revenue?
```

The agent can:

1. Interpret the question
2. Generate pandas/Python code
3. Execute the code
4. Inspect the result
5. Return the answer

For more complex requests, it can generate visualizations:

```text
Show me the monthly sales trend as a chart.
```

The agent generates the required analysis and matplotlib visualization automatically.

Follow-up questions can use previous conversational context:

```text
User: Which region has the highest revenue?

User: What about its monthly trend?
```

---

##  Error Recovery

One of the main goals of the project is to demonstrate an iterative agent workflow.

If generated Python code produces an execution error, the error is fed back into the reasoning loop so the agent can attempt to correct the generated code.

```text
Generate Code
      ↓
Execute Code
      ↓
   Error?
   ↙    ↘
 Yes      No
  ↓        ↓
Analyze   Return
 Error    Result
  ↓
Regenerate Code
  ↓
Execute Again
```

This makes the workflow more robust than simply generating code once and returning the result.

---

##  Why I Built This

Many agent frameworks make it easy to build an agent by abstracting away the underlying orchestration.

For this project, I deliberately implemented the core workflow myself to better understand:

* Agent orchestration
* LLM tool use
* Code generation
* Tool execution
* Error handling and retries
* Conversational state
* Iterative agent loops

The objective was not to recreate an LLM or an agent framework, but to understand the **engineering patterns behind an agentic application**.

---

##  Security Considerations

This application executes Python code generated by an LLM.

**Do not run the application against untrusted users or datasets in a production environment without implementing a secure sandbox.**

Potential production improvements include:

* Sandboxed code execution
* Container isolation
* Resource limits
* File validation
* Execution timeouts
* Restricted Python operations
* Authentication and authorization

This project is intended primarily as a learning and portfolio implementation.

---

##  Future Improvements

*  Secure sandboxed Python execution
*  Support for additional file formats
*  Improved chart generation
*  More robust code validation
*  Persistent conversation history
*  Dataset profiling before analysis
*  Streaming responses
*  Docker deployment
*  Automated tests
*  Production deployment

---

##  Author

**Aiswarya H**

AI/ML | Generative AI | Machine Learning | Deep Learning
