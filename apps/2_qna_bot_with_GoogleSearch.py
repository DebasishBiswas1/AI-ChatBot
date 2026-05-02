from dotenv import load_dotenv
# import streamlit as st
load_dotenv()
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
llm = ChatGroq(model="llama-3.3-70b-versatile")
search = GoogleSerperAPIWrapper()


agent = create_agent(model = llm,
                     tools = [search.run],
                     system_prompt="You are a agent and can search for any question from google.")

while True:
  query = input("Ask a question: ")
  if query.lower() in ["exit", "quit", "bye"]:
    print("Goodbye!")
    break

  response = agent.invoke({"messages": [{"role": "user", "content": query}]})
  print("Answer:", response["messages"][-1].content, "\n")


