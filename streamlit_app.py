from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.runnables.history import RunnableWithMessageHistory

import streamlit as st

st.set_page_config(page_title="LangChain: Chat with search", page_icon="🦜")
st.title("🦜 Code from AgentExecutor.ipynb")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

from langchain import hub

# Get the prompt to use - you can modify this!
prompt_for_agent = hub.pull("hwchase17/openai-functions-agent")

msgs = StreamlitChatMessageHistory()
 
if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

for idx, msg in enumerate(msgs.messages):
    with st.chat_message(msg.type):
        st.write(msg.content)

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=openai_api_key, streaming=True)
    tools = [DuckDuckGoSearchRun(name="Search")]

    chat_agent = create_tool_calling_agent(llm, tools, prompt_for_agent)
    executor = AgentExecutor(agent=chat_agent, tools=tools)
    executor_with_memory = RunnableWithMessageHistory(
        executor,
        lambda session_id: msgs,  # Always return the instance created earlier
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    with st.chat_message("assistant"):
        cfg = RunnableConfig()
        cfg["configurable"] = {"session_id": "any"}
        response = executor_with_memory.invoke({"input": prompt}, cfg)
        st.write(response["output"])
        st.page_link("http://www.google.com", label="Google", icon="🌎")
        st.page_link("http://www.yahoo.com", label="Yahoo", icon="🏠")