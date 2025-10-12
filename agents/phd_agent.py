"""
AUTONOMOUS PhD-LEVEL CODING AGENT
OpenAI Assistants API + Desktop Commander Integration
Commander Bobby Don McWilliams II

Features:
- Full filesystem access via Desktop Commander
- Windows API integration
- Autonomous debugging and diagnostics
- Self-healing code execution
- PhD-level programming expertise
"""
import os
import sys
import json
import time
import subprocess
from openai import OpenAI
from typing import Dict, List, Any, Optional
import ctypes
import win32api
import win32con
import win32process
import psutil

class DesktopCommanderTools:
    """Integration layer for Desktop Commander functionality"""
    
    def __init__(self, python_path: str = r"H:\Tools\python.exe"):
        self.python_path = python_path
        self.working_dir = os.getcwd()
    
    def read_file(self, path: str, offset: int = 0, length: int = 1000) -> Dict[str, Any]:
        """Read file with Desktop Commander efficiency"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                if offset < 0:
                    # Negative offset = read last N lines
                    result_lines = lines[offset:]
                else:
                    # Positive offset = read from line N
                    result_lines = lines[offset:offset + length]
                
                return {
                    "success": True,
                    "content": "".join(result_lines),
                    "total_lines": len(lines),
                    "lines_returned": len(result_lines)
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, path: str, content: str, mode: str = "rewrite") -> Dict[str, Any]:
        """Write file with chunking support"""
        try:
            write_mode = 'w' if mode == "rewrite" else 'a'
            with open(path, write_mode, encoding='utf-8') as f:
                f.write(content)
            
            line_count = len(content.split('\n'))
            return {
                "success": True,
                "lines_written": line_count,
                "mode": mode,
                "path": path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def edit_block(self, file_path: str, old_string: str, new_string: str) -> Dict[str, Any]:
        """Surgical file editing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.count(old_string) != 1:
                return {
                    "success": False,
                    "error": f"String appears {content.count(old_string)} times, need exactly 1"
                }
            
            new_content = content.replace(old_string, new_string, 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {"success": True, "edited": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute shell command with output capture"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_directory(self, path: str) -> Dict[str, Any]:
        """List directory contents with metadata"""
        try:
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                stats = os.stat(full_path)
                items.append({
                    "name": item,
                    "type": "DIR" if os.path.isdir(full_path) else "FILE",
                    "size": stats.st_size,
                    "modified": stats.st_mtime
                })
            
            return {"success": True, "items": items, "count": len(items)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_files(self, path: str, pattern: str, search_type: str = "files") -> Dict[str, Any]:
        """Search for files or content"""
        try:
            results = []
            if search_type == "files":
                # Search by filename
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if pattern.lower() in file.lower():
                            results.append(os.path.join(root, file))
            else:
                # Search content
                for root, dirs, files in os.walk(path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if pattern in content:
                                    results.append(file_path)
                        except:
                            continue
            
            return {"success": True, "results": results, "count": len(results)}
        except Exception as e:
            return {"success": False, "error": str(e)}

class WindowsAPITools:
    """Advanced Windows API integration"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Comprehensive system information"""
        return {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                part.mountpoint: {
                    "total": psutil.disk_usage(part.mountpoint).total,
                    "used": psutil.disk_usage(part.mountpoint).used,
                    "free": psutil.disk_usage(part.mountpoint).free,
                    "percent": psutil.disk_usage(part.mountpoint).percent
                }
                for part in psutil.disk_partitions() if 'cdrom' not in part.opts
            },
            "boot_time": psutil.boot_time()
        }
    
    @staticmethod
    def list_processes() -> List[Dict[str, Any]]:
        """List all running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes
    
    @staticmethod
    def kill_process(pid: int) -> Dict[str, Any]:
        """Terminate a process"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            return {"success": True, "pid": pid}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_window_list() -> List[Dict[str, Any]]:
        """Get list of all windows"""
        windows = []
        def callback(hwnd, _):
            if win32api.IsWindowVisible(hwnd):
                title = win32api.GetWindowText(hwnd)
                if title:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    windows.append({
                        "hwnd": hwnd,
                        "title": title,
                        "pid": pid
                    })
        win32api.EnumWindows(callback, None)
        return windows

class PhDCodingAgent:
    """
    PhD-Level Autonomous Coding Agent
    
    Capabilities:
    - Full filesystem access and manipulation
    - Windows API integration
    - Autonomous debugging and error correction
    - Self-diagnostic capabilities
    - Multi-threaded execution
    - Code generation and optimization
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.dc_tools = DesktopCommanderTools()
        self.win_tools = WindowsAPITools()
        self.assistant_id = None
        self.thread_id = None
        self.execution_history = []
        
        # PhD-level system prompt
        self.system_prompt = """You are a PhD-level autonomous coding agent with complete system access.

EXPERTISE AREAS:
- Software Architecture & Design Patterns
- Algorithm Optimization & Complexity Analysis
- Systems Programming (Windows API, filesystems, processes)
- Debugging & Diagnostics at assembly level
- Multi-threaded & Concurrent Programming
- Network Programming & Protocols
- Database Design & Optimization
- Machine Learning & AI Integration
- Security & Cryptography
- Performance Profiling & Optimization

CAPABILITIES:
1. Full filesystem read/write/edit access
2. Windows API control (processes, windows, system info)
3. Command execution with output capture
4. Autonomous error detection and self-correction
5. Code generation in any language
6. Real-time debugging and diagnostics

OPERATION MODE:
- Analyze problems deeply before acting
- Generate production-ready code (no stubs/mocks)
- Self-diagnose and fix errors autonomously
- Optimize every solution for performance
- Document complex logic inline
- Use surgical edits (edit_block) for existing code
- Never create backup/copy files (_v2, _fixed, etc)
- Execute with military efficiency

TOOLS AVAILABLE:
- read_file(path, offset, length): Read file content
- write_file(path, content, mode): Write/append to file
- edit_block(path, old_str, new_str): Surgical code editing
- execute_command(command, timeout): Run shell commands
- list_directory(path): Directory listing with metadata
- search_files(path, pattern, type): Search files/content
- get_system_info(): System diagnostics
- list_processes(): Running process list
- kill_process(pid): Terminate process
- get_window_list(): Active windows

PYTHON PATH: H:\\Tools\\python.exe (always use full path)

CORE PRINCIPLES:
1. Think algorithmically, act precisely
2. Optimize for O(1) when possible
3. Handle edge cases exhaustively
4. Write self-documenting code
5. Debug at root cause level
6. Autonomous error recovery

You have PhD-level expertise across all programming domains. Approach every task
with deep technical knowledge and systematic problem-solving."""

    def create_assistant(self) -> str:
        """Create OpenAI Assistant with full tool integration"""
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read file content with optional offset and length",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"},
                            "offset": {"type": "integer", "description": "Start line (0-based, negative for tail)"},
                            "length": {"type": "integer", "description": "Max lines to read"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write or append to file. Chunk large files into 25-30 line blocks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"},
                            "content": {"type": "string", "description": "Content to write"},
                            "mode": {"type": "string", "enum": ["rewrite", "append"], "description": "Write mode"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_block",
                    "description": "Surgical text replacement. Old string must appear exactly once.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "File to edit"},
                            "old_string": {"type": "string", "description": "Text to replace"},
                            "new_string": {"type": "string", "description": "Replacement text"}
                        },
                        "required": ["file_path", "old_string", "new_string"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_command",
                    "description": "Execute shell command with output capture",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "Shell command"},
                            "timeout": {"type": "integer", "description": "Timeout in seconds"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List directory contents with metadata",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Directory path"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for files by name or content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Root directory"},
                            "pattern": {"type": "string", "description": "Search pattern"},
                            "search_type": {"type": "string", "enum": ["files", "content"]}
                        },
                        "required": ["path", "pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Get comprehensive system diagnostics",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_processes",
                    "description": "List all running processes",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "kill_process",
                    "description": "Terminate a process by PID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pid": {"type": "integer", "description": "Process ID"}
                        },
                        "required": ["pid"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_window_list",
                    "description": "Get list of all active windows",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {"type": "code_interpreter"}
        ]
        
        assistant = self.client.beta.assistants.create(
            name="PhD Coding Agent",
            instructions=self.system_prompt,
            tools=tools,
            model="gpt-4-turbo-preview"
        )
        
        self.assistant_id = assistant.id
        print(f"✅ Assistant created: {self.assistant_id}")
        return assistant.id
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute tool calls with error handling"""
        try:
            if tool_name == "read_file":
                return self.dc_tools.read_file(**arguments)
            elif tool_name == "write_file":
                return self.dc_tools.write_file(**arguments)
            elif tool_name == "edit_block":
                return self.dc_tools.edit_block(**arguments)
            elif tool_name == "execute_command":
                return self.dc_tools.execute_command(**arguments)
            elif tool_name == "list_directory":
                return self.dc_tools.list_directory(**arguments)
            elif tool_name == "search_files":
                return self.dc_tools.search_files(**arguments)
            elif tool_name == "get_system_info":
                return self.win_tools.get_system_info()
            elif tool_name == "list_processes":
                return self.win_tools.list_processes()
            elif tool_name == "kill_process":
                return self.win_tools.kill_process(**arguments)
            elif tool_name == "get_window_list":
                return self.win_tools.get_window_list()
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_thread(self) -> str:
        """Create conversation thread"""
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        return thread.id
    
    def send_message(self, content: str) -> str:
        """Send message and execute autonomously"""
        if not self.thread_id:
            self.create_thread()
        
        # Add message to thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=content
        )
        
        # Create run
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        
        print(f"🚀 Executing task: {content[:60]}...")
        return self.execute_run(run.id)
    
    def execute_run(self, run_id: str) -> str:
        """Autonomous execution loop with tool handling"""
        max_iterations = 50  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Check run status
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id
            )
            
            status = run.status
            print(f"  [{iteration}] Status: {status}")
            
            if status == "completed":
                # Get final response
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id,
                    order="desc",
                    limit=1
                )
                response = messages.data[0].content[0].text.value
                print(f"✅ Completed in {iteration} iterations")
                return response
            
            elif status == "requires_action":
                # Handle tool calls autonomously
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                
                for tool_call in tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    print(f"  🔧 Executing: {func_name}({args})")
                    result = self.execute_tool(func_name, args)
                    
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })
                    
                    # Log execution
                    self.execution_history.append({
                        "iteration": iteration,
                        "tool": func_name,
                        "args": args,
                        "result": result
                    })
                
                # Submit tool outputs
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run_id,
                    tool_outputs=tool_outputs
                )
            
            elif status in ["failed", "cancelled", "expired"]:
                print(f"❌ Run {status}: {run.last_error}")
                return f"Error: {status}"
            
            # Wait before checking again
            time.sleep(1)
        
        print(f"⚠️ Max iterations ({max_iterations}) reached")
        return "Task incomplete - max iterations reached"
    
    def autonomous_task(self, task_description: str) -> Dict[str, Any]:
        """Execute task with full autonomy and diagnostics"""
        start_time = time.time()
        
        print("=" * 70)
        print("AUTONOMOUS EXECUTION MODE")
        print("=" * 70)
        
        response = self.send_message(task_description)
        
        elapsed = time.time() - start_time
        
        print(f"\n⏱️ Execution time: {elapsed:.2f}s")
        print(f"🔧 Tools called: {len(self.execution_history)}")
        
        return {
            "response": response,
            "execution_time": elapsed,
            "tools_used": len(self.execution_history),
            "history": self.execution_history
        }
    
    def save_execution_log(self, filepath: str = "E:\\ECHO_XV4\\MLS\\agents\\execution_log.json"):
        """Save execution history"""
        with open(filepath, 'w') as f:
            json.dump({
                "assistant_id": self.assistant_id,
                "thread_id": self.thread_id,
                "history": self.execution_history
            }, f, indent=2)
        print(f"💾 Log saved: {filepath}")

def main():
    """Main execution interface"""
    print("=" * 70)
    print("PhD-LEVEL AUTONOMOUS CODING AGENT")
    print("Commander Bobby Don McWilliams II")
    print("=" * 70)
    print()
    
    # Load API key from keychain
    keychain_path = r"E:\ECHO_XV4\CONFIG\echo_x_complete_api_keychain.env"
    if os.path.exists(keychain_path):
        print("🔐 Loading API keys from keychain...")
        with open(keychain_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Keychain loaded")
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in keychain!")
        sys.exit(1)
    
    # Initialize agent
    print("🤖 Initializing PhD Agent...")
    agent = PhDCodingAgent()
    agent.create_assistant()
    agent.create_thread()
    print()
    
    # Interactive loop
    print("💬 Enter tasks for autonomous execution")
    print("Commands: 'quit' to exit, 'log' to save execution history")
    print("-" * 70)
    print()
    
    while True:
        try:
            task = input("📋 Task: ").strip()
            
            if not task:
                continue
            
            if task.lower() == 'quit':
                print("👋 Shutting down agent...")
                agent.save_execution_log()
                break
            
            if task.lower() == 'log':
                agent.save_execution_log()
                continue
            
            # Execute task
            print()
            result = agent.autonomous_task(task)
            print()
            print("📤 RESPONSE:")
            print("-" * 70)
            print(result['response'])
            print("-" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted")
            agent.save_execution_log()
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()
