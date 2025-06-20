import streamlit as st

st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")

st.title("🤖 Chatbot UI")
st.write("Ask me anything!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input from user
user_input = st.text_input("You:", key="input")

# Simple rule-based response
def get_bot_response(message):
    message = message.lower()
    if "hello" in message:
        return "Hi there! How can I help you?"
    elif "bye" in message:
        return "Goodbye! 👋"
    elif "name" in message:
        return "I'm a simple chatbot built with Streamlit."
    else:
        return "I'm not sure how to respond to that. Try asking something else."

# Add message to history and display
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    response = get_bot_response(user_input)
    st.session_state.chat_history.append(("bot", response))

# Show the chat
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
