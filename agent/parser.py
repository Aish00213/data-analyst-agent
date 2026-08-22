import re

def parse_response(response: str) -> dict:
    # READ_FILE takes priority — always do this before writing code
    if "TOOL: READ_FILE" in response:
        filename_match = re.search(r"FILENAME:\s*(.*)", response)
        return {
            "tool": "READ_FILE",
            "filename": filename_match.group(1).strip() if filename_match else ""
        }

    # EXECUTE_CODE — extract the first code block only
    if "TOOL: EXECUTE_CODE" in response:
        code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if code_match:
            return {
                "tool": "EXECUTE_CODE",
                "code": code_match.group(1).strip()
            }

    if "TOOL: SAVE_CHART" in response:
        filename_match = re.search(r"FILENAME:\s*(.+)", response)
        if filename_match:
            return {
                "tool": "SAVE_CHART",
                "filename": filename_match.group(1).strip()
            }

    return {"tool": None}
    
