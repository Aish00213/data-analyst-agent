import pandas as pd
import sys
import io
import traceback
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools.chart_generate import save_chart

# inside execute_code(), add to exec_globals:
exec_globals = {
    "pd": pd,
    "os": os,
    "plt": plt,
    "matplotlib": matplotlib,
}

DATA_DIR = "data"

def execute_code(code: str, filename: str = None) -> str:
    """
    Executes Python code in a controlled environment.
    If a filename is given, loads it as `df` before running the code.
    Returns stdout output or a formatted error message.
    """

    # --- Build the execution environment ---
    exec_globals = {
        "pd": pd,
        "os": os,
    }

    # If a file is loaded, make `df` available in the environment
    if filename:
        filepath = os.path.join(DATA_DIR, filename)
        ext = filename.lower().split(".")[-1]
        try:
            if ext == "csv":
                df = pd.read_csv(filepath)
            elif ext in ("xlsx", "xls"):
                df = pd.read_excel(filepath)
            exec_globals["df"] = df
        except Exception as e:
            return f"ERROR loading dataframe: {str(e)}"

    # --- Capture stdout (so print() output is returned as a string) ---
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()

    try:
        exec(code, exec_globals)
        output = captured.getvalue()
        return output if output.strip() else "Code executed successfully. No output was printed."

    except Exception:
        # Extract only the last 2 lines — the error type and message
        full_traceback = traceback.format_exc()
        lines = full_traceback.strip().splitlines()
        short_error = "\n".join(lines[-2:])  # e.g. "KeyError: 'nonexistent_column'"
        return f"ERROR:\n{short_error}"

    finally:
        # Always restore stdout, even if exec() crashed
        sys.stdout = old_stdout