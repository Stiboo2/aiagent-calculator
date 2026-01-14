# functions/get_file_content.py
import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    """Read a file safely within the working directory."""
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: "{file_path}" is outside the working directory'
        
        # Check if file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a file'
        
        # Read file
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        
        # Add truncation notice if needed
        if len(content) >= MAX_CHARS:
            content += f'\n[... File "{file_path}" truncated at {MAX_CHARS} characters ...]'
        
        return content
        
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" as text (binary file?)'
    except PermissionError:
        return f'Error: Permission denied to read "{file_path}"'
    except Exception as e:
        return f'Error reading "{file_path}": {str(e)}'