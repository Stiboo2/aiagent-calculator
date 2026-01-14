# functions/run_python_file.py
import os
import sys
import subprocess
import shlex

def run_python_file(working_directory: str, file_path: str, args: str = "") -> str:
    """Run a Python file with optional arguments."""
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: "{file_path}" is outside the working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" is not a file'

        # Build command
        cmd = [sys.executable, abs_file_path]
        if args:
            cmd.extend(shlex.split(args))
        
        # Run the script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )
        
        # Format output
        output = f"Exit code: {result.returncode}\n"
        if result.stdout:
            output += f"Stdout:\n{result.stdout}\n"
        if result.stderr:
            output += f"Stderr:\n{result.stderr}"
        
        return output.strip()
    except subprocess.TimeoutExpired:
        return "Error: Script timed out after 30 seconds"
    except Exception as e:
        return f"Exception running script: {str(e)}"