# functions/write_file.py
import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write content to a file in the working directory."""
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: "{file_path}" is outside the working directory'

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
        # Write file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}"'
    except PermissionError:
        return f'Error: Permission denied to write to "{file_path}"'
    except Exception as e:
        return f'Error writing to "{file_path}": {str(e)}'