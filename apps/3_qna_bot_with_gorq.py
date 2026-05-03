from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

llm = ChatGroq(model="llama-3.3-70b-versatile",streaming=True)
serach = GoogleSerperAPIWrapper()
tools = [serach.run]

if "memory" not in st.session_state:
  st.session_state.memory = MemorySaver()
  st.session_state.history = []

agent = create_agent(
  model = llm,
  tools = tools,
  checkpointer=st.session_state.memory,
  system_prompt="You are a helpful assistant that answers questions based on the information you find on the web. Use the provided tools to search for information and provide accurate answers to the user's questions."
)

# web interface
st.subheader("QnA Bot with Groq and Google Search")

for message in st.session_state.history:
  if message["role"] == "user":
    st.chat_message("user").markdown(message["content"])
  else:
    st.chat_message("assistant").markdown(message["content"])

query = st.chat_input("Tell me something:")

if query: 
  st.chat_message("user").markdown(query)
  st.session_state.history.append({"role": "user", "content": query})

  response = agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    {"configurable": {"thread_id": "1"}},
    stream_mode="messages"
  )

  ai_container = st.chat_message("assistant")
  with ai_container:
     space = st.empty()
     message = ""
     for chunk in response:
       message = message + chunk[0].content
       space.write(message)

     st.session_state.history.append({"role": "assistant", "content": message})

  # answer = response["messages"][-1].content
  
  # st.chat_message("assistant").markdown(answer)

