# main_simple.py
import os
import sys

def get_files_info(working_directory: str) -> str:
    """Simple file lister without dependencies."""
    try:
        items = os.listdir(working_directory)
        if not items:
            return "Directory is empty"
        
        result = []
        for item in items:
            item_path = os.path.join(working_directory, item)
            if os.path.isdir(item_path):
                result.append(f"[DIR]  {item}/")
            else:
                size = os.path.getsize(item_path)
                result.append(f"[FILE] {item} ({size} bytes)")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python main_simple.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    working_dir = os.path.join(os.getcwd(), "calculator")
    
    if not os.path.exists(working_dir):
        os.makedirs(working_dir, exist_ok=True)
        if verbose:
            print(f"Created directory: {working_dir}")
    
    if verbose:
        print(f"Working directory: {working_dir}")
        print(f"Prompt: {prompt}")
    
    # Simple command parsing
    if "list" in prompt.lower() and any(word in prompt.lower() for word in ["files", "folder", "directory"]):
        result = get_files_info(working_dir)
        print(f"\nFiles in '{working_dir}':")
        print(result)
    else:
        print(f"Prompt: {prompt}")
        print("I can help list files in the calculator folder.")
        print("Try: 'List files in calculator folder'")

if __name__ == "__main__":
    main()