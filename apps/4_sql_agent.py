from dotenv import load_dotenv
load_dotenv()

# from langchain_community import tools
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
llm = ChatGroq(model="llama-3.3-70b-versatile",streaming=True)
db = SQLDatabase.from_uri("sqlite:///tasks.db")


db.run("""

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
       """)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
agent = create_agent(
  model = llm,
  tools = tools,
  checkpointer=MemorySaver(),
  system_prompt="You are a helpful assistant that manages a task list. Use the provided tools to add, update, and query tasks in the database."
)