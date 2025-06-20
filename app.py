
import streamlit as st
import requests, json

# ---------- Config ----------
OLLAMA_URL = "http://localhost:11434/api/chat"   # adjust if Ollama runs elsewhere
MODEL       = "llama3"                           # pick any model you have pulled
# -----------------------------

st.set_page_config(page_title="Ollama + Streamlit Chatbot", page_icon="💬")
st.title("💬 Ollama Chatbot (Streamlit)")

# Initialize chat history in Streamlit session state
if "history" not in st.session_state:
    st.session_state["history"] = []   # list of {"role": "...", "content": "..."}

# --- sidebar controls (optional) ---
with st.sidebar:
    st.markdown("### Settings")
    MODEL = st.text_input("Model name", value=MODEL)

# --- main UI ---
prompt = st.text_input("You:", key="user_input", placeholder="Ask me anything…")
send_clicked = st.button("Send", key="send_btn")

def stream_from_ollama(prompt, history):
    """Generator that yields tokens from Ollama’s streaming endpoint"""
    payload = {
        "model": MODEL,
        "messages": history + [{"role": "user", "content": prompt}],
        "stream": True
    }
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=0) as resp:
        for line in resp.iter_lines():
            if line and line.startswith(b"data: "):
                data = json.loads(line[6:])
                yield data.get("message", {}).get("content", "")

if send_clicked and prompt:
    # Store user message
    st.session_state["history"].append({"role": "user", "content": prompt})

    # Placeholder that will grow as we receive tokens
    response_box = st.empty()
    full_response = ""

    # Stream tokens
    for token in stream_from_ollama(prompt, st.session_state["history"]):
        full_response += token
        response_box.markdown(full_response + "▌")   # typing cursor

    # Finalise
    response_box.markdown(full_response)
    st.session_state["history"].append({"role": "assistant", "content": full_response})
