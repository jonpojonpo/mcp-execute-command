import asyncio
import pytest
from mcp_execute_command import MCPExecuteCommandServer

@pytest.mark.asyncio
async def test_initialize():
    server = MCPExecuteCommandServer()
    response = await server.handle_initialize({})
    
    assert response["serverInfo"]["name"] == "mcp-execute-command"
    assert response["serverInfo"]["version"] == "0.1.0"
    assert "tools" in response["capabilities"]
    assert "execute" in response["capabilities"]["tools"]

@pytest.mark.asyncio
async def test_execute_command():
    server = MCPExecuteCommandServer()
    
    # Test echo command
    response = await server.execute_command("echo test")
    assert response["success"] is True
    assert response["returncode"] == 0
    assert "test" in response["stdout"]
    assert not response["stderr"]
    
    # Test invalid command
    response = await server.execute_command("invalid_command_xyz")
    assert response["success"] is False
    assert response["returncode"] == -1
    assert "error" in response

@pytest.mark.asyncio
async def test_handle_request():
    server = MCPExecuteCommandServer()
    
    # Test initialize request
    response = await server.handle_request("initialize", {})
    assert response["serverInfo"]["name"] == "mcp-execute-command"
    
    # Test execute_command request
    response = await server.handle_request("execute_command", {"command": "echo test"})
    assert response["success"] is True
    assert "test" in response["stdout"]
    
    # Test invalid method
    with pytest.raises(ValueError):
        await server.handle_request("invalid_method", {})