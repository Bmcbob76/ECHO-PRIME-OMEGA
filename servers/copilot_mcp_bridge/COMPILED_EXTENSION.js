/**
 * ECHO COPILOT BRIDGE - Fixed Pre-compiled Extension
 * Authority Level: 11.0
 * Commander: Bobby Don McWilliams II
 * 
 * Connects to Desktop Commander MCP server and exposes ALL tools to GitHub Copilot
 */

const vscode = require('vscode');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

let mcpProcess = null;
let mcpTools = [];
let isConnected = false;
let statusBarItem = null;

async function activate(context) {
    console.log('🚀 ECHO Copilot Bridge activating...');

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = '$(pulse) ECHO Initializing...';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands FIRST
    registerCommands(context);

    // Auto-connect on activation
    try {
        await connectToMcpServer(context);
    } catch (error) {
        console.error('❌ Auto-connect failed:', error);
        statusBarItem.text = '$(error) ECHO Failed';
        statusBarItem.tooltip = `ECHO connection failed: ${error.message}`;

        const outputChannel = vscode.window.createOutputChannel('ECHO Bridge Debug');
        outputChannel.appendLine('='.repeat(70));
        outputChannel.appendLine('ECHO COPILOT BRIDGE - CONNECTION ERROR');
        outputChannel.appendLine('='.repeat(70));
        outputChannel.appendLine(`Error: ${error.message}`);
        outputChannel.appendLine(`Stack: ${error.stack}`);
        outputChannel.appendLine('');
        outputChannel.appendLine('Troubleshooting:');
        outputChannel.appendLine('1. Start MCP server: node "E:\\ECHO_XV4\\CLAUDE_EXT_BACKUP\\ant.dir.gh.wonderwhy-er.desktopcommandermcp\\dist\\index.js"');
        outputChannel.appendLine('2. Or use Python fallback: python "E:\\ECHO_XV4\\MLS\\servers\\desktop_commander_server.py"');
        outputChannel.appendLine('3. Then run: ECHO: Connect to ECHO Servers');
        outputChannel.show();

        vscode.window.showWarningMessage(
            'ECHO Bridge could not auto-connect. Check Output > ECHO Bridge Debug for details.',
            'Open Logs'
        ).then(selection => {
            if (selection === 'Open Logs') {
                outputChannel.show();
            }
        });
    }
}

function registerCommands(context) {
    console.log('📝 Registering ECHO commands...');

    // Connect command
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.copilot.connect', async () => {
            try {
                statusBarItem.text = '$(sync~spin) ECHO Connecting...';
                await connectToMcpServer(context);
                vscode.window.showInformationMessage(`✅ ECHO Connected with ${mcpTools.length} tools`);
            } catch (error) {
                statusBarItem.text = '$(error) ECHO Failed';
                vscode.window.showErrorMessage(`❌ Connection failed: ${error.message}`);
            }
        })
    );

    // Disconnect command
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.copilot.disconnect', () => {
            disconnectMcpServer();
            statusBarItem.text = '$(circle-slash) ECHO Disconnected';
            vscode.window.showInformationMessage('ECHO Bridge disconnected');
        })
    );

    // Status command
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.copilot.status', () => {
            const status = isConnected ? 'Connected' : 'Disconnected';
            const toolCount = mcpTools.length;
            const message = `ECHO Status: ${status}, Tools: ${toolCount}`;

            vscode.window.showInformationMessage(message);
            console.log(message);

            if (mcpTools.length > 0) {
                console.log('Available tools:', mcpTools.map(t => t.name).join(', '));
            }
        })
    );

    // List tools command
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.copilot.listTools', () => {
            const panel = vscode.window.createWebviewPanel(
                'echoTools',
                'ECHO Tools',
                vscode.ViewColumn.One,
                {}
            );

            panel.webview.html = generateToolsHtml();
        })
    );

    console.log('✅ ECHO commands registered successfully');
}

async function connectToMcpServer(context) {
    console.log('🔌 Connecting to MCP server...');

    // Find MCP server path
    const platform = os.platform();
    let serverPath = null;
    let command = 'node';

    if (platform === 'win32') {
        // Try Node.js server first
        const nodePath = 'E:\\ECHO_XV4\\CLAUDE_EXT_BACKUP\\ant.dir.gh.wonderwhy-er.desktopcommandermcp\\dist\\index.js';
        const pythonPath = 'E:\\ECHO_XV4\\MLS\\servers\\desktop_commander_server.py';

        if (fs.existsSync(nodePath)) {
            serverPath = nodePath;
            command = 'node';
            console.log('✅ Using Node.js MCP server');
        } else if (fs.existsSync(pythonPath)) {
            serverPath = pythonPath;
            command = 'python';
            console.log('✅ Using Python MCP server');
        }
    }

    if (!serverPath) {
        throw new Error('No MCP server found. Please ensure Desktop Commander is installed.');
    }

    // Start MCP server
    await startMcpServer(command, serverPath);

    // Get tools from server
    const tools = await getMcpTools();
    console.log(`📋 Received ${tools.length} tools from MCP server`);

    if (tools.length === 0) {
        throw new Error('No tools received from MCP server');
    }

    // Register each tool with Copilot
    for (const tool of tools) {
        registerToolWithCopilot(tool, context);
    }

    console.log(`✅ ECHO Copilot Bridge activated with ${tools.length} tools`);
    statusBarItem.text = `$(zap) ECHO Connected (${tools.length} tools)`;
    statusBarItem.tooltip = `ECHO Bridge connected with ${tools.length} tools available`;
    isConnected = true;
}

function disconnectMcpServer() {
    if (mcpProcess) {
        mcpProcess.kill();
        mcpProcess = null;
    }
    isConnected = false;
    mcpTools = [];
    console.log('ECHO Bridge disconnected');
}

async function startMcpServer(command, serverPath) {
    return new Promise((resolve, reject) => {
        console.log(`🔌 Starting MCP server: ${command} ${serverPath}`);

        mcpProcess = spawn(command, [serverPath], {
            stdio: ['pipe', 'pipe', 'pipe']
        });

        mcpProcess.stdout.on('data', (data) => {
            console.log(`MCP stdout: ${data}`);
        });

        mcpProcess.stderr.on('data', (data) => {
            console.error(`MCP stderr: ${data}`);
        });

        mcpProcess.on('error', (error) => {
            console.error(`MCP process error: ${error}`);
            reject(error);
        });

        mcpProcess.on('exit', (code) => {
            console.log(`MCP process exited with code: ${code}`);
            isConnected = false;
            if (statusBarItem) {
                statusBarItem.text = '$(error) ECHO Disconnected';
            }
        });

        // Give server time to start
        setTimeout(() => {
            if (mcpProcess && !mcpProcess.killed) {
                resolve();
            } else {
                reject(new Error('MCP server failed to start'));
            }
        }, 2000);
    });
}

async function getMcpTools() {
    return new Promise((resolve, reject) => {
        if (!mcpProcess) {
            reject(new Error('MCP process not started'));
            return;
        }

        const request = {
            jsonrpc: '2.0',
            id: 1,
            method: 'tools/list',
            params: {}
        };

        let responseData = '';

        const responseHandler = (data) => {
            responseData += data.toString();

            try {
                const lines = responseData.split('\n');
                for (const line of lines) {
                    if (line.trim()) {
                        const response = JSON.parse(line);
                        if (response.id === 1 && response.result && response.result.tools) {
                            mcpProcess.stdout.removeListener('data', responseHandler);
                            mcpTools = response.result.tools;
                            resolve(response.result.tools);
                            return;
                        }
                    }
                }
            } catch (error) {
                // Still collecting data, continue
            }
        };

        mcpProcess.stdout.on('data', responseHandler);

        // Send request
        mcpProcess.stdin.write(JSON.stringify(request) + '\n');

        // Timeout after 10 seconds
        setTimeout(() => {
            mcpProcess.stdout.removeListener('data', responseHandler);
            reject(new Error('Timeout waiting for tools list'));
        }, 10000);
    });
}

function registerToolWithCopilot(tool, context) {
    try {
        console.log(`🔧 Registering tool: ${tool.name}`);

        const toolDefinition = {
            name: tool.name,
            description: tool.description || `ECHO tool: ${tool.name}`,
            parametersSchema: tool.inputSchema || { type: 'object', properties: {} }
        };

        const toolHandler = async (request, token) => {
            try {
                console.log(`🔧 Executing tool: ${tool.name}`);

                const result = await callMcpTool(tool.name, request.parameters || {});

                return new vscode.LanguageModelToolResult([
                    new vscode.LanguageModelTextPart(
                        typeof result === 'string' ? result : JSON.stringify(result, null, 2)
                    )
                ]);

            } catch (error) {
                console.error(`❌ Tool execution failed: ${tool.name}`, error);
                return new vscode.LanguageModelToolResult([
                    new vscode.LanguageModelTextPart(`Error executing ${tool.name}: ${error.message}`)
                ]);
            }
        };

        const disposable = vscode.lm.registerTool(toolDefinition, toolHandler);
        context.subscriptions.push(disposable);

        console.log(`✅ Registered tool: ${tool.name}`);

    } catch (error) {
        console.error(`❌ Failed to register tool ${tool.name}:`, error);
    }
}

async function callMcpTool(toolName, parameters) {
    return new Promise((resolve, reject) => {
        if (!mcpProcess) {
            reject(new Error('MCP process not started'));
            return;
        }

        const request = {
            jsonrpc: '2.0',
            id: Date.now(),
            method: 'tools/call',
            params: {
                name: toolName,
                arguments: parameters
            }
        };

        let responseData = '';

        const responseHandler = (data) => {
            responseData += data.toString();

            try {
                const lines = responseData.split('\n');
                for (const line of lines) {
                    if (line.trim()) {
                        const response = JSON.parse(line);
                        if (response.id === request.id) {
                            mcpProcess.stdout.removeListener('data', responseHandler);

                            if (response.error) {
                                reject(new Error(response.error.message));
                            } else {
                                resolve(response.result);
                            }
                            return;
                        }
                    }
                }
            } catch (error) {
                // Still collecting data
            }
        };

        mcpProcess.stdout.on('data', responseHandler);

        // Send request
        mcpProcess.stdin.write(JSON.stringify(request) + '\n');

        // Timeout after 30 seconds
        setTimeout(() => {
            mcpProcess.stdout.removeListener('data', responseHandler);
            reject(new Error(`Timeout executing tool: ${toolName}`));
        }, 30000);
    });
}

function generateToolsHtml() {
    const toolsList = mcpTools.map(tool => `
        <div style="margin: 10px 0; padding: 10px; background: #252526; border-left: 3px solid #007acc;">
            <h3 style="color: #dcdcaa; margin: 0;">${tool.name}</h3>
            <p style="color: #9cdcfe; margin: 5px 0;">${tool.description || 'No description'}</p>
        </div>
    `).join('');

    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #1e1e1e; color: #d4d4d4; }
        h1 { color: #4ec9b0; }
    </style>
</head>
<body>
    <h1>🎖️ ECHO Tools Available to Copilot</h1>
    <p>Total: ${mcpTools.length} tools</p>
    ${toolsList}
</body>
</html>`;
}

function deactivate() {
    console.log('🛑 ECHO Copilot Bridge deactivating...');
    disconnectMcpServer();
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};