from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


st.title("🤖 Q&A Bot with Google Gemini")
st.text("Ask any question and get an answer from the Google Gemini model. Type 'exit', 'quit', or 'bye' to end the conversation.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

for message in st.session_state.conversation:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

query = st.chat_input("Ask anything:")
if query:
    st.session_state.conversation.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    response = llm.invoke(query)
    st.session_state.conversation.append({"role": "assistant", "content": response.content})
    st.chat_message("assistant").markdown(response.content)

# while True:
#   query = input("Ask a question: ")
#   if query.lower() in ["exit", "quit", "bye"]:
#     print("Goodbye!")
#     break

#   response = llm.invoke(query)
#   print("Answer:", response.content, "\n")