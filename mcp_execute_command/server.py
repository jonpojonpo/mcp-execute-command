import asyncio
import json
import platform
import shlex
import subprocess
from typing import Dict, List, Optional

class MCPExecuteCommandServer:
    def __init__(self, name: str = "mcp-execute-command", version: str = "0.1.0"):
        self.name = name
        self.version = version
        self._process = None
    
    async def handle_initialize(self, params: Dict) -> Dict:
        """Handle initialization request from client"""
        return {
            "serverInfo": {
                "name": self.name,
                "version": self.version
            },
            "capabilities": {
                "tools": {
                    "execute": {
                        "version": "1.0",
                        "commands": ["execute_command"]
                    }
                }
            }
        }
    
    async def execute_command(self, command: str, shell: bool = False, cwd: Optional[str] = None) -> Dict:
        """Execute a command and return the result"""
        try:
            # Split command if not using shell
            if not shell and platform.system() != "Windows":
                command = shlex.split(command)
            
            # Run command
            proc = await asyncio.create_subprocess_exec(
                *command if not shell else command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=shell,
                cwd=cwd
            )
            
            stdout, stderr = await proc.communicate()
            
            return {
                "success": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }

    async def handle_request(self, method: str, params: Dict) -> Dict:
        """Handle incoming requests"""
        if method == "initialize":
            return await self.handle_initialize(params)
        elif method == "execute_command":
            command = params.get("command")
            shell = params.get("shell", False)
            cwd = params.get("cwd")
            if not command:
                raise ValueError("Command parameter is required")
            return await self.execute_command(command, shell, cwd)
        else:
            raise ValueError(f"Unknown method: {method}")

    async def start(self):
        """Start the server using stdio transport"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, input)
                request = json.loads(line)
                
                response = await self.handle_request(
                    request["method"],
                    request.get("params", {})
                )
                
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": response
                }))
                
            except EOFError:
                break
            except Exception as e:
                print(json.dumps({
                    "jsonrpc": "2.0", 
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }))

def main():
    server = MCPExecuteCommandServer()
    asyncio.run(server.start())

if __name__ == "__main__":
    main()