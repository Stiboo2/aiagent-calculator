# agent_logic.py
import json
import re
from langchain_ollama import ChatOllama

def simple_agent(prompt: str, working_directory: str, tools: dict, verbose: bool = False):
    """A simple agent that interprets prompts and uses tools."""
    
    # Initialize LLM
    llm = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2",
        temperature=0.5,
        num_predict=1024
    )
    
    # Create the full prompt
    full_prompt = f"""You are a file system assistant. You have access to these tools:
    1. list_files - Lists files in the working directory
    2. read_file(file_path) - Reads content of a file
    3. write_file(file_path, content) - Writes content to a file
    4. run_python(file_path, args) - Runs a Python file
    
    Working directory: {working_directory}
    
    Current files in directory:
    {tools['list_files']()}
    
    When user asks for something, decide which tool to use and provide the arguments in JSON format.
    Respond ONLY with JSON in this format:
    {{
        "tool": "tool_name",
        "arguments": {{...}},
        "explanation": "brief explanation"
    }}
    
    If no tool is needed, respond with:
    {{
        "tool": null,
        "response": "your response here"
    }}
    
    Examples:
    - User: "List files" -> {{"tool": "list_files", "arguments": {{}}, "explanation": "User wants to see files"}}
    - User: "Read greeting.txt" -> {{"tool": "read_file", "arguments": {{"file_path": "greeting.txt"}}, "explanation": "User wants to read greeting.txt"}}
    - User: "Write test.txt Hello" -> {{"tool": "write_file", "arguments": {{"file_path": "test.txt", "content": "Hello"}}, "explanation": "User wants to write to test.txt"}}
    - User: "Run script.py" -> {{"tool": "run_python", "arguments": {{"file_path": "script.py"}}, "explanation": "User wants to run script.py"}}
    - User: "What files start with 'lorem'?" -> {{"tool": "list_files", "arguments": {{}}, "explanation": "Check all files to see which start with lorem"}}
    - User: "Show me .py files" -> {{"tool": "list_files", "arguments": {{}}, "explanation": "List all files and filter for .py extension"}}
    
    User question: {prompt}
    
    Respond with JSON only:"""
    
    try:
        # Get LLM decision
        response = llm.invoke(full_prompt)
        response_text = response.content
        
        if verbose:
            print(f"LLM Response: {response_text}")
        
        # Parse JSON response
        try:
            decision = json.loads(response_text.strip())
        except json.JSONDecodeError:
            # Try to extract JSON if it's embedded in text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                decision = json.loads(json_match.group())
            else:
                return f"Could not understand the request. LLM response: {response_text}"
        
        # Execute based on decision
        if decision.get("tool"):
            tool_name = decision["tool"]
            args = decision.get("arguments", {})
            
            if verbose:
                print(f"Using tool: {tool_name}")
                print(f"Arguments: {args}")
            
            # Tool execution
            if tool_name == "list_files":
                result = tools["list_files"]()
                # Apply filters based on prompt
                prompt_lower = prompt.lower()
                
                # Filter by file extension
                if ".py" in prompt_lower:
                    lines = result.split('\n')
                    filtered = [line for line in lines if ".py" in line and "[FILE]" in line]
                    return "\n".join(filtered) if filtered else "No .py files found"
                
                # Filter by filename pattern
                pattern_match = re.search(r"['\"]([^'\"]+)['\"]", prompt)
                if pattern_match:
                    pattern = pattern_match.group(1)
                    lines = result.split('\n')
                    filtered = [line for line in lines if f"[FILE] {pattern}" in line or f"[DIR] {pattern}" in line]
                    return "\n".join(filtered) if filtered else f"No files matching '{pattern}' found"
                
                return result
                
            elif tool_name == "read_file":
                return tools["read_file"](args.get("file_path", ""))
            elif tool_name == "write_file":
                return tools["write_file"](
                    args.get("file_path", ""),
                    args.get("content", "")
                )
            elif tool_name == "run_python":
                return tools["run_python"](
                    args.get("file_path", ""),
                    args.get("args", "")
                )
            else:
                return f"Unknown tool: {tool_name}"
        else:
            return decision.get("response", "No response from assistant")
            
    except Exception as e:
        return f"Error: {str(e)}"