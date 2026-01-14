# test_agent_workflow.py
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# --- 1️⃣ Set working directory ---
WORK_DIR = r"C:\project\aiagent_calculator\calculator"
os.chdir(WORK_DIR)  # Ensure all relative paths are from the working directory

# --- 2️⃣ Load environment ---
load_dotenv(".env")

# --- 3️⃣ System prompt ---
system_prompt = """
You are a helpful AI coding agent.

You can perform the following operations:
- List files and directories
- Read the content of a file
- Write to a file (create or update)
- Run a Python file with optional arguments

All paths are relative to the working directory.
"""

# --- 4️⃣ Initialize Ollama LLM ---
model = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3.2",
    temperature=0.5,
    num_predict=1024,
    system_prompt=system_prompt
)

# --- 5️⃣ Setup tools ---
tools = [get_files_info, get_file_content, write_file, run_python_file]

# --- 6️⃣ Initialize agent ---
agent = initialize_agent(
    tools=tools,
    llm=model,
    agent="zero-shot-react-description",
    verbose=True
)

# --- 7️⃣ Multi-step prompt ---
prompt = """
List all files in the working directory.

"""

# --- 8️⃣ Run agent ---
result = agent.run(prompt)

# --- 9️⃣ Print result ---
print("=== Agent Output ===")
print(result)
