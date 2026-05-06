import streamlit as st
import requests
import uuid
import os

API_URL = "http://127.0.0.1:8000"

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
    import time
    st.session_state.session_start_time = time.time()

# Sidebar — file upload
with st.sidebar:
    st.header("📂 Upload Data File")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded_file:
        response = requests.post(
            f"{API_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "text/csv")}
        )
        if response.status_code == 200:
            st.success(f"✅ {uploaded_file.name} uploaded!")
            st.session_state.filename = uploaded_file.name
        else:
            st.error("Upload failed")

    st.divider()
    st.caption(f"Session: {st.session_state.session_id[:8]}...")
    if st.button("🔄 New Session"):
        import time
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.charts = []
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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent is thinking... (may take a few seconds)"):
            response = requests.post(
                f"{API_URL}/query",
                json={
                    "session_id": st.session_state.session_id,
                    "query": prompt
                }
            )
            if response.status_code == 200:
                answer = response.json()["response"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Only pick up charts created after this session started
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
            else:
                st.error("⚠️ API error — is the FastAPI server running?")