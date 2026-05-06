import streamlit as st
import uuid
import os
import time
from main import run_agent, FILENAME

st.set_page_config(page_title="Data Analyst Agent", page_icon="🤖", layout="wide")
st.title("🤖 Data Analyst Agent")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "charts" not in st.session_state:
    st.session_state.charts = []
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

# Sidebar
with st.sidebar:
    st.header("📂 Upload Data File")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        dest = os.path.join("data", uploaded_file.name)
        with open(dest, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.current_filename = uploaded_file.name
        st.success(f"✅ {uploaded_file.name} uploaded!")

    st.divider()
    st.caption(f"Session: {st.session_state.session_id[:8]}...")
    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.charts = []
        st.session_state.agent_history = []
        st.session_state.session_start_time = time.time()
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Display charts from this session
for chart_path in st.session_state.charts:
    if os.path.exists(chart_path):
        st.image(chart_path)

# Chat input
if prompt := st.chat_input("Ask something about your data..."):
    if "current_filename" not in st.session_state:
        st.warning("⚠️ Please upload a data file first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Agent is thinking..."):
                # Call run_agent directly — no API needed
                history = run_agent(
                    prompt,
                    messages=st.session_state.agent_history,
                    filename=st.session_state.current_filename
                )
                st.session_state.agent_history = history

                # Extract last assistant message
                assistant_msgs = [m for m in history if m["role"] == "assistant"]
                answer = assistant_msgs[-1]["content"] if assistant_msgs else "No response."

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Pick up new charts
                if os.path.exists("outputs"):
                    charts = [
                        os.path.join("outputs", f)
                        for f in os.listdir("outputs")
                        if f.endswith(".png") and
                        os.path.getmtime(os.path.join("outputs", f)) > st.session_state.session_start_time
                    ]
                    for chart in sorted(charts, key=os.path.getmtime):
                        if chart not in st.session_state.charts:
                            st.session_state.charts.append(chart)
                            st.image(chart)
                            