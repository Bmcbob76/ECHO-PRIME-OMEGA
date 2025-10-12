# ECHO VS Code API Extension
**Commander Bobby Don McWilliams II - Authority Level 11.0**

## Overview

VS Code extension that provides a REST API server for programmatic control of VS Code editor operations. Part of the ECHO_XV4 Unified Developer API System.

## Features

- ✅ REST API server on port 9001
- ✅ Open/close files programmatically
- ✅ Edit text at specific positions
- ✅ Run VS Code commands
- ✅ Control selections and cursor
- ✅ Execute terminal commands
- ✅ Workspace file operations
- ✅ Find and replace across files
- ✅ Document formatting
- ✅ Auto-start on VS Code launch

## Installation

### 1. Install Dependencies

```bash
cd E:\ECHO_XV4\MLS\servers\vscode_api_extension
npm install
```

### 2. Compile TypeScript

```bash
npm run compile
```

### 3. Install Extension

```bash
# Package the extension
npm run package

# Install in VS Code
code --install-extension echo-vscode-api-1.0.0.vsix
```

OR manually:
1. Press `F1` in VS Code
2. Type "Extensions: Install from VSIX"
3. Select `echo-vscode-api-1.0.0.vsix`

### 4. Reload VS Code

Press `Ctrl+Shift+P` and run "Developer: Reload Window"

## Configuration

Open VS Code Settings (`Ctrl+,`) and configure:

```json
{
    "echo.apiPort": 9001,
    "echo.autoStart": true,
    "echo.enableLogging": true,
    "echo.allowedOrigins": [
        "http://localhost:9000",
        "http://localhost:8343"
    ]
}
```

## Usage

### Start API Server

The server starts automatically if `echo.autoStart` is `true`.

Manual control:
- Press `Ctrl+Shift+P`
- Run "ECHO: Start API Server"

### Check Status

Click the ECHO icon in the status bar (bottom right) to see server status.

### Stop Server

- Press `Ctrl+Shift+P`
- Run "ECHO: Stop API Server"

## API Endpoints

### Health Check
```
GET http://localhost:9001/health
```

### List All Endpoints
```
GET http://localhost:9001/api/endpoints
```

### File Operations

#### Open File
```
POST http://localhost:9001/vscode/open_file
{
    "filePath": "E:\\path\\to\\file.ts",
    "viewColumn": 1
}
```

#### Close File
```
POST http://localhost:9001/vscode/close_file
{
    "filePath": "E:\\path\\to\\file.ts"
}
```

#### Save File
```
POST http://localhost:9001/vscode/save_file
{
    "filePath": "E:\\path\\to\\file.ts"
}
```

### Text Editing

#### Edit Text
```
POST http://localhost:9001/vscode/edit_text
{
    "filePath": "E:\\path\\to\\file.ts",
    "line": 10,
    "character": 5,
    "text": "new text here",
    "endLine": 10,
    "endCharacter": 20
}
```

#### Get Text
```
POST http://localhost:9001/vscode/get_text
{
    "filePath": "E:\\path\\to\\file.ts",
    "startLine": 0,
    "endLine": 10
}
```

### Selection Operations

#### Get Selection
```
GET http://localhost:9001/vscode/get_selection
```

#### Set Selection
```
POST http://localhost:9001/vscode/set_selection
{
    "startLine": 5,
    "startCharacter": 0,
    "endLine": 10,
    "endCharacter": 20
}
```

### Commands

#### Run VS Code Command
```
POST http://localhost:9001/vscode/run_command
{
    "command": "editor.action.formatDocument",
    "args": []
}
```

### Find & Replace

```
POST http://localhost:9001/vscode/find_replace
{
    "find": "oldText",
    "replace": "newText",
    "filePath": "E:\\path\\to\\file.ts",
    "isRegex": false
}
```

### Terminal Operations

```
POST http://localhost:9001/vscode/terminal_command
{
    "command": "npm test",
    "terminalName": "Test Terminal"
}
```

### Workspace Operations

#### List Files
```
GET http://localhost:9001/vscode/workspace_files?pattern=**/*.ts
```

#### Get Active File Info
```
GET http://localhost:9001/vscode/active_file
```

### Document Operations

#### Format Document
```
POST http://localhost:9001/vscode/format_document
{
    "filePath": "E:\\path\\to\\file.ts"
}
```

## Example Usage (Python)

```python
import requests

# Open a file
response = requests.post('http://localhost:9001/vscode/open_file', json={
    'filePath': 'E:\\\\ECHO_XV4\\\\server.py'
})

# Edit text at line 10
response = requests.post('http://localhost:9001/vscode/edit_text', json={
    'filePath': 'E:\\\\ECHO_XV4\\\\server.py',
    'line': 10,
    'character': 0,
    'text': 'print("Hello from ECHO API")\n'
})

# Save the file
response = requests.post('http://localhost:9001/vscode/save_file', json={
    'filePath': 'E:\\\\ECHO_XV4\\\\server.py'
})

# Run tests in terminal
response = requests.post('http://localhost:9001/vscode/terminal_command', json={
    'command': 'python -m pytest'
})
```

## Development

### Watch Mode

```bash
npm run watch
```

This will automatically recompile TypeScript on file changes.

### Debugging

1. Open the extension folder in VS Code
2. Press `F5` to launch Extension Development Host
3. The extension will run in debug mode

## Architecture

```
Extension Host (VS Code Process)
├── extension.ts           - Extension entry point
├── api_server.ts          - Express.js REST API
└── command_bridge.ts      - VS Code API bridge
```

## Integration with Unified Developer API

This extension is part of the ECHO_XV4 Unified Developer API System:

```
Unified API (Port 9000)
  ↓
VS Code API Extension (Port 9001) ← You are here
  ↓
VS Code API Calls
```

## Troubleshooting

### Server Won't Start

Check if port 9001 is already in use:
```bash
netstat -ano | findstr :9001
```

Change port in settings if needed.

### Extension Not Loading

1. Check VS Code Developer Tools (`Ctrl+Shift+I`)
2. Look for errors in Console tab
3. Ensure TypeScript compiled successfully

### Commands Not Working

1. Check if server is running (status bar icon)
2. Verify file paths use double backslashes (`\\\\`)
3. Check CORS origins in settings

## Security

- CORS is configured to only allow specific origins
- Default allowed: localhost:9000, localhost:8343
- Modify `echo.allowedOrigins` in settings to change

## License

MIT - ECHO_XV4 System

## Author

Commander Bobby Don McWilliams II  
Authority Level: 11.0  
ECHO_XV4 Production System

---

**Status:** Ready for installation  
**Port:** 9001  
**Auto-start:** Enabled  
**Integration:** ECHO Unified Developer API
