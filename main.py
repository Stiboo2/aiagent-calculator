# main.py - Refactored version
import os
import sys
from dotenv import load_dotenv

# Import configuration
from config import MAX_CHARS

# Import tool functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Import agent logic
from agent_logic import simple_agent

def main():
    # --- 1️⃣ Command-line args ---
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    prompt = sys.argv[1]
    verbose_flag = "--verbose" in sys.argv

    # --- 2️⃣ Load environment variables ---
    load_dotenv(".env")
    
    # --- 3️⃣ Set working directory ---
    working_directory = os.path.join(os.getcwd(), "calculator")
    ensure_directory_exists(working_directory, verbose_flag)
    
    if verbose_flag:
        print(f"Working directory: {working_directory}")
        print(f"Prompt: {prompt}")
        print("-" * 50)

    # --- 4️⃣ Setup tools dictionary ---
    tools = {
        "list_files": lambda: get_files_info(working_directory),
        "read_file": lambda file_path: get_file_content(working_directory, file_path),
        "write_file": lambda file_path, content: write_file(working_directory, file_path, content),
        "run_python": lambda file_path, args="": run_python_file(working_directory, file_path, args)
    }

    # --- 5️⃣ Fast paths for common commands ---
    if should_use_fast_path(prompt):
        handle_fast_path(prompt, working_directory, tools)
        return

    # --- 6️⃣ Use AI agent for complex commands ---
    print(f"Processing: {prompt}")
    if verbose_flag:
        print("Using AI agent...")
    
    result = simple_agent(prompt, working_directory, tools, verbose_flag)
    
    # --- 7️⃣ Display result ---
    print_result(result)

# --- Helper Functions ---

def print_usage():
    """Print usage instructions."""
    print("Usage: python main.py <prompt> [--verbose]")
    print("\nExamples:")
    print("  python main.py 'List files in calculator folder'")
    print("  python main.py 'Read greeting.txt' --verbose")
    print("  python main.py 'Write test.txt Hello World'")
    print("  python main.py 'Run script.py'")
    print("  python main.py 'What files start with lorem?'")
    print("  python main.py 'Show me all .py files'")

def ensure_directory_exists(directory: str, verbose: bool):
    """Ensure the working directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        if verbose:
            print(f"Created directory: {directory}")

def should_use_fast_path(prompt: str) -> bool:
    """Check if prompt should use fast path execution."""
    prompt_lower = prompt.lower()
    return (
        ("list" in prompt_lower and any(word in prompt_lower for word in ["files", "folder", "directory"])) or
        "read greeting" in prompt_lower or
        "read lorem" in prompt_lower
    )

def handle_fast_path(prompt: str, working_directory: str, tools: dict):
    """Handle common commands without AI agent."""
    prompt_lower = prompt.lower()
    
    if "list" in prompt_lower:
        result = tools["list_files"]()
        if ".py" in prompt_lower:
            lines = result.split('\n')
            filtered = [line for line in lines if ".py" in line and "[FILE]" in line]
            result = "\n".join(filtered) if filtered else "No .py files found"
        
        print(f"\nFiles in '{working_directory}':")
        print(result)
    
    elif "read greeting" in prompt_lower:
        result = tools["read_file"]("greeting.txt")
        print(f"\nContent of 'greeting.txt':")
        print(result)
    
    elif "read lorem" in prompt_lower:
        filename = "lorem2.txt" if "2" in prompt_lower else "lorem.txt"
        result = tools["read_file"](filename)
        print(f"\nContent of '{filename}':")
        print(result)

def print_result(result: str):
    """Print the result with formatting."""
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()