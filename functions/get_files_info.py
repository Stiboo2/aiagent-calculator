# functions/get_files_info.py
import os

def get_files_info(working_directory: str) -> str:
    """List files and directories in the working directory."""
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
        return f"Error listing directory: {e}"