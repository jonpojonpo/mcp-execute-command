# MCP Execute Command Server

An implementation of the Model Context Protocol (MCP) server for executing commands across different platforms.

## Features

- Cross-platform command execution
- Support for both shell and direct command execution
- Configurable working directory
- Comprehensive error handling and reporting

## Installation

```bash
pip install mcp-execute-command
```

## Usage

### As a Library

```python
from mcp_execute_command import MCPExecuteCommandServer

server = MCPExecuteCommandServer()
asyncio.run(server.start())
```

### Command Line

```bash
python -m mcp_execute_command
```

## Protocol Implementation

This server implements the MCP protocol with the following capabilities:

- Tool: `execute_command`
  - Version: 1.0
  - Methods:
    - `execute_command`: Execute a command and return results

### Request Format

```json
{
    "jsonrpc": "2.0",
    "method": "execute_command",
    "params": {
        "command": "echo 'hello world'",
        "shell": false,
        "cwd": "/optional/working/directory"
    },
    "id": 1
}
```

### Response Format

```json
{
    "jsonrpc": "2.0",
    "result": {
        "success": true,
        "returncode": 0,
        "stdout": "hello world\n",
        "stderr": ""
    },
    "id": 1
}
```

## License

MIT License