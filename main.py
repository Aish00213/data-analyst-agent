from agent.llm import call_llm
from agent.prompt import SYSTEM_PROMPT
from agent.parser import parse_response
from tools.file_reader import read_file
from tools.code_executor import execute_code
from tools.chart_generate import save_chart

FILENAME = "business-financial-data-december-2025-quarter.csv"
MAX_ITERATIONS = 10

def run_agent(user_query: str, messages: list = None):
    if messages is None:
        messages = []

    print(f"\n{'='*60}")
    print(f"Query: {user_query}")
    print(f"{'='*60}\n")

    messages.append({"role": "user", "content": user_query})

    for i in range(MAX_ITERATIONS):
        print(f"--- Iteration {i+1} ---")

        response = call_llm(messages, SYSTEM_PROMPT)
        print(f"LLM: {response}\n")

        messages.append({"role": "assistant", "content": response})

        parsed = parse_response(response)

        if parsed["tool"] is None:
            print("✅ Agent finished.")
            return messages  # ← return messages, not response

        if parsed["tool"] == "READ_FILE":
            print(f"🔧 Tool: READ_FILE — {FILENAME}")
            tool_output = read_file(FILENAME)

        elif parsed["tool"] == "EXECUTE_CODE":
            print(f"🔧 Tool: EXECUTE_CODE")
            tool_output = execute_code(parsed["code"], FILENAME)

        elif parsed["tool"] == "SAVE_CHART":
            fname = parsed.get("filename", "chart.png")
            print(f"🔧 Tool: SAVE_CHART — {fname}")
            tool_output = save_chart(fname)

        else:
            tool_output = "ERROR: Unknown tool called."

        print(f"Tool output:\n{tool_output}\n")

        messages.append({
            "role": "user",
            "content": f"Tool output:\n{tool_output}"
        })

    print("⚠️ Max iterations reached.")
    return messages  # ← also return messages here, not None


if __name__ == "__main__":
    print(f" Data Analyst Agent")
    print(f" File: {FILENAME}")
    print(f"Type 'exit' to quit.\n")

    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        history = run_agent(user_input, messages=history)