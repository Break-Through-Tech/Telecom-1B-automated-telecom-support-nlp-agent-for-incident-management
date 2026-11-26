import streamlit as st

from agent import get_agent

st.set_page_config(page_title="TelcoTriage: Automated Support NLP Agent", page_icon="🤖")
st.title("TelcoTriage")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

with st.bottom:
    with st.form("chat_composer", clear_on_submit=True):
        prompt_column, submit_column = st.columns([0.88, 0.12], vertical_alignment="bottom")
        with prompt_column:
            prompt = st.text_area(
                "Message",
                placeholder="Ask the agent a question...",
                height=100,
                label_visibility="collapsed",
            )
        with submit_column:
            submitted = st.form_submit_button(
                "▶",
                type="primary",
                help="Run agent",
                use_container_width=True,
            )

if submitted and prompt.strip():
    st.session_state.messages.append({"role": "user", "content": prompt.strip()})
    try:
        with st.spinner("The agent is thinking…"):
            result = get_agent().run(prompt.strip())
        st.session_state.messages.append({"role": "assistant", "content": str(result)})
    except Exception as exc:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    f"The agent could not complete the request: {exc}\n\n"
                ),
            }
        )
    st.rerun()
