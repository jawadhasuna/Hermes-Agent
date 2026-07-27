import os
import subprocess
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

llm = ChatOllama(model="hermes3:8b", temperature=0)

@tool
def read_file(filepath: str) -> str:
    """Read and return the contents of a Python file."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a Python file, overwriting it."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def run_python(filepath: str) -> str:
    """Run a Python script and return its output or error."""
    try:
        result = subprocess.run(
            ["python", filepath],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return f"Success! Output:\n{result.stdout}"
        else:
            return f"Error occurred:\n{result.stderr}"
    except Exception as e:
        return f"Error running script: {e}"

tools = [read_file, write_file, run_python]

agent = create_agent(llm, tools)


if __name__ == "__main__":
    task = input("What should the coding assistant do?\n> ")
    result = agent.invoke({"messages": [("user", task)]})
for msg in result["messages"]:
    print(f"\n[{msg.type}]: {msg.content}")