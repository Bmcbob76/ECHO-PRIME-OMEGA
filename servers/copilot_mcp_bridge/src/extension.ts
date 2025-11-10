/**
 * ECHO Ultimate Unified MCP Bridge Extension
 * Full GitHub Copilot Integration via Language Model Tools API
 * Commander Bobby Don McWilliams II - Authority Level 11.0
 */

import * as vscode from 'vscode';
import { spawn, ChildProcess } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface MCPTool {
    name: string;
    description: string;
    inputSchema: any;
}

let mcpServerProcess: ChildProcess | null = null;
let outputChannel: vscode.OutputChannel;
let statusBarItem: vscode.StatusBarItem;
let availableTools: MCPTool[] = [];
let mcpInitialized = false;
let requestIdCounter = 0;
let registeredTools: vscode.Disposable[] = [];
let isStarting = false; // Prevent concurrent starts

// Buffer for MCP responses
let mcpResponseBuffer = '';

export async function activate(context: vscode.ExtensionContext) {
    console.log('🔥 ECHO Ultimate Unified MCP Bridge activating...');
    
    // Create output channel
    outputChannel = vscode.window.createOutputChannel('ECHO MCP Bridge');
    context.subscriptions.push(outputChannel);
    
    // Create status bar
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "$(loading~spin) ECHO MCP Starting...";
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    
    // Start MCP server
    await startMCPServer();
    
    // Wait for server initialization
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Initialize MCP connection
    if (mcpServerProcess) {
        await initializeMCP();
        await loadTools();
        await registerLanguageModelTools();
    }
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.restartMCPServer', async () => {
            await restartMCPServer();
        })
    );
    
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.stopMCPServer', () => {
            stopMCPServer();
        })
    );
    
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.showMCPLogs', () => {
            outputChannel.show();
        })
    );
    
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.checkMCPHealth', async () => {
            const health = await checkServerHealth();
            vscode.window.showInformationMessage(`MCP Server: ${health ? '✅ Healthy' : '❌ Not responding'}`);
        })
    );
    
    // Register Chat Participant
    const echoParticipant = vscode.chat.createChatParticipant('echo', async (request, context, stream, token) => {
        await handleChatRequest(request, stream, token);
        return {};
    });
    
    echoParticipant.iconPath = vscode.Uri.file(path.join(context.extensionPath, 'icon.png'));
    context.subscriptions.push(echoParticipant);
    
    outputChannel.appendLine('🔥 ECHO Ultimate Unified MCP Bridge activated');
    outputChannel.appendLine(`   Available tools: ${availableTools.length}`);
    outputChannel.appendLine(`   Registered with Copilot: ${registeredTools.length}`);
    outputChannel.appendLine(`   Chat Participant: @echo registered`);
}

export function deactivate() {
    console.log('🔥 ECHO Ultimate Unified MCP Bridge deactivating...');
    stopMCPServer();
}

// ============================================================================
// CHAT PARTICIPANT HANDLER
// ============================================================================

async function handleChatRequest(
    request: vscode.ChatRequest,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
): Promise<void> {
    const userMessage = request.prompt.trim();
    
    outputChannel.appendLine(`\n💬 Chat request: ${userMessage}`);
    
    // Check if server is ready
    if (!mcpServerProcess || !mcpInitialized || availableTools.length === 0) {
        stream.markdown('❌ **ECHO MCP Server not ready**\n\nPlease wait for server initialization or run "ECHO: Restart MCP Server"');
        return;
    }
    
    // Parse command
    const commandPattern = /^(list|read|write|execute|exec|run)\s+(.+)$/i;
    const match = userMessage.match(commandPattern);
    
    if (!match) {
        stream.markdown('**ECHO Commander - Available Commands:**\n\n' +
            '- `@echo list <path>` - List directory contents\n' +
            '- `@echo read <file>` - Read file contents\n' +
            '- `@echo write <file> <content>` - Write to file\n' +
            '- `@echo execute <command>` - Execute shell command\n\n' +
            `**Status:** ${availableTools.length} tools available`);
        return;
    }
    
    const [, command, args] = match;
    const cmd = command.toLowerCase();
    
    try {
        let toolName: string;
        let toolArgs: any;
        
        switch (cmd) {
            case 'list':
                toolName = 'list_directory';
                toolArgs = { path: args };
                stream.markdown(`**📁 Listing:** \`${args}\`\n\n`);
                break;
                
            case 'read':
                toolName = 'read_file';
                toolArgs = { path: args };
                stream.markdown(`**📄 Reading:** \`${args}\`\n\n`);
                break;
                
            case 'write':
                const writeMatch = args.match(/^(\S+)\s+(.+)$/);
                if (!writeMatch) {
                    stream.markdown('❌ **Invalid syntax**\n\nUsage: `@echo write <file> <content>`');
                    return;
                }
                toolName = 'write_file';
                toolArgs = { path: writeMatch[1], content: writeMatch[2] };
                stream.markdown(`**✍️ Writing:** \`${writeMatch[1]}\`\n\n`);
                break;
                
            case 'execute':
            case 'exec':
            case 'run':
                toolName = 'execute_command';
                toolArgs = { command: args };
                stream.markdown(`**⚡ Executing:** \`${args}\`\n\n`);
                break;
                
            default:
                stream.markdown(`❌ Unknown command: \`${cmd}\``);
                return;
        }
        
        // Call MCP tool
        outputChannel.appendLine(`   Calling tool: ${toolName}`);
        outputChannel.appendLine(`   Args: ${JSON.stringify(toolArgs)}`);
        
        const result = await callMCPTool(toolName, toolArgs);
        
        if (result.success) {
            stream.markdown(`\`\`\`\n${result.content}\n\`\`\`\n\n✅ Success`);
        } else {
            stream.markdown(`❌ **Error:** ${result.error}`);
        }
        
    } catch (error: any) {
        stream.markdown(`❌ **Exception:** ${error.message}`);
        outputChannel.appendLine(`   Exception: ${error.message}`);
    }
}

// ============================================================================
// LANGUAGE MODEL TOOLS REGISTRATION
// ============================================================================

async function registerLanguageModelTools() {
    outputChannel.appendLine('\n🔧 Registering tools with Language Model API...');
    
    if (availableTools.length === 0) {
        outputChannel.appendLine('⚠️  No tools available to register!');
        statusBarItem.text = `$(warning) ECHO MCP (0 tools)`;
        return;
    }
    
    // Dispose previous registrations
    registeredTools.forEach(d => d.dispose());
    registeredTools = [];
    
    for (const tool of availableTools) {
        try {
            outputChannel.appendLine(`   Registering: echo_${tool.name}`);
            
            const disposable = vscode.lm.registerTool(
                `echo_${tool.name}`,
                {
                    invoke: async (input: any, _token: vscode.CancellationToken) => {
                        outputChannel.appendLine(`\n🔧 Tool called: ${tool.name}`);
                        outputChannel.appendLine(`   Input: ${JSON.stringify(input)}`);
                        
                        try {
                            const result = await callMCPTool(tool.name, input);
                            
                            if (result.success) {
                                outputChannel.appendLine(`   ✅ Success`);
                                return new vscode.LanguageModelToolResult([
                                    new vscode.LanguageModelTextPart(result.content || 'Success')
                                ]);
                            } else {
                                outputChannel.appendLine(`   ❌ Error: ${result.error}`);
                                throw new Error(result.error || 'Tool execution failed');
                            }
                        } catch (error: any) {
                            outputChannel.appendLine(`   ❌ Exception: ${error.message}`);
                            throw error;
                        }
                    }
                }
            );
            
            registeredTools.push(disposable);
            outputChannel.appendLine(`   ✅ Registered: echo_${tool.name}`);
            
        } catch (error: any) {
            outputChannel.appendLine(`   ❌ Failed to register ${tool.name}: ${error.message}`);
            outputChannel.appendLine(`      Stack: ${error.stack}`);
        }
    }
    
    statusBarItem.text = `$(check) ECHO MCP (${registeredTools.length} tools)`;
    outputChannel.appendLine(`\n✅ Registered ${registeredTools.length}/${availableTools.length} tools with Copilot`);
}

async function callMCPTool(toolName: string, args: any): Promise<{success: boolean, content?: string, error?: string}> {
    try {
        const response = await sendMCPRequest('tools/call', {
            name: toolName,
            arguments: args
        });
        
        if (response.result) {
            return {
                success: true,
                content: JSON.stringify(response.result.content || response.result, null, 2)
            };
        } else if (response.error) {
            return {
                success: false,
                error: response.error.message || 'Unknown error'
            };
        }
        
        return { success: false, error: 'Invalid response' };
        
    } catch (error: any) {
        return { success: false, error: error.message };
    }
}

// ============================================================================
// MCP SERVER COMMUNICATION
// ============================================================================

async function sendMCPRequest(method: string, params?: any): Promise<any> {
    return new Promise((resolve, reject) => {
        if (!mcpServerProcess || !mcpServerProcess.stdin) {
            reject(new Error('MCP server not running'));
            return;
        }
        
        const requestId = ++requestIdCounter;
        const request = {
            jsonrpc: '2.0',
            id: requestId,
            method: method,
            params: params || {}
        };
        
        outputChannel.appendLine(`→ MCP Request: ${JSON.stringify(request)}`);
        
        // Set up one-time response handler
        const responseHandler = (data: Buffer) => {
            const text = data.toString();
            mcpResponseBuffer += text;
            
            // Try to parse complete JSON-RPC responses
            const lines = mcpResponseBuffer.split('\n');
            for (let i = 0; i < lines.length - 1; i++) {
                const line = lines[i].trim();
                if (line && line.startsWith('{')) {
                    try {
                        const response = JSON.parse(line);
                        if (response.id === requestId) {
                            outputChannel.appendLine(`← MCP Response: ${JSON.stringify(response)}`);
                            mcpServerProcess?.stdout?.removeListener('data', responseHandler);
                            resolve(response);
                            mcpResponseBuffer = lines.slice(i + 1).join('\n');
                            return;
                        }
                    } catch (e) {
                        // Not complete JSON yet
                    }
                }
            }
        };
        
        mcpServerProcess.stdout?.on('data', responseHandler);
        
        // Send request
        mcpServerProcess.stdin.write(JSON.stringify(request) + '\n');
        
        // Timeout after 10 seconds
        setTimeout(() => {
            mcpServerProcess?.stdout?.removeListener('data', responseHandler);
            reject(new Error('MCP request timeout'));
        }, 10000);
    });
}

async function initializeMCP(): Promise<void> {
    try {
        const response = await sendMCPRequest('initialize', {
            protocolVersion: '2024-11-05',
            capabilities: {},
            clientInfo: {
                name: 'echo-copilot-bridge',
                version: '2.0.0'
            }
        });
        
        if (response.result) {
            mcpInitialized = true;
            outputChannel.appendLine('✅ MCP initialized');
        }
    } catch (error: any) {
        outputChannel.appendLine(`❌ MCP initialization failed: ${error.message}`);
    }
}

async function loadTools(): Promise<void> {
    try {
        const response = await sendMCPRequest('tools/list');
        
        if (response.result && response.result.tools) {
            availableTools = response.result.tools;
            outputChannel.appendLine(`✅ Loaded ${availableTools.length} tools from MCP server`);
            availableTools.forEach(tool => {
                outputChannel.appendLine(`   - ${tool.name}: ${tool.description}`);
            });
            statusBarItem.text = `$(loading~spin) ECHO MCP Registering...`;
            statusBarItem.tooltip = `Desktop Commander MCP\n${availableTools.length} tools loading...`;
        } else {
            outputChannel.appendLine(`⚠️  No tools returned from MCP server`);
        }
    } catch (error: any) {
        outputChannel.appendLine(`❌ Failed to load tools: ${error.message}`);
        statusBarItem.text = `$(error) ECHO MCP Error`;
    }
}
// ============================================================================
// MCP SERVER MANAGEMENT
// ============================================================================

async function startMCPServer(): Promise<void> {
    if (mcpServerProcess) {
        outputChannel.appendLine('⚠️  MCP server already running');
        return;
    }
    
    if (isStarting) {
        outputChannel.appendLine('⚠️  MCP server start already in progress');
        return;
    }
    
    isStarting = true;
    
    const config = vscode.workspace.getConfiguration('echo.mcp');
    const serverPath = config.get<string>('serverPath') || 
                      'E:\\ECHO_XV4\\CLAUDE_EXT_BACKUP\\ant.dir.gh.wonderwhy-er.desktopcommandermcp\\dist\\index.js';
    const nodePath = config.get<string>('nodePath') || 'node';
    
    outputChannel.appendLine('🚀 Starting Desktop Commander MCP Server...');
    outputChannel.appendLine(`   Server: ${serverPath}`);
    outputChannel.appendLine(`   Node: ${nodePath}`);
    
    // Check if server file exists
    if (!fs.existsSync(serverPath)) {
        vscode.window.showErrorMessage(`MCP Server not found: ${serverPath}`);
        statusBarItem.text = "$(error) ECHO MCP Error";
        isStarting = false;
        return;
    }
    
    // Spawn Node process
    try {
        mcpServerProcess = spawn(nodePath, [serverPath], {
            cwd: path.dirname(serverPath),
            env: {
                ...process.env,
                NODE_ENV: 'production'
            }
        });
        
        // Handle stdout (non-JSON output)
        mcpServerProcess.stdout?.on('data', (data: Buffer) => {
            const text = data.toString();
            if (!text.startsWith('{')) {
                outputChannel.append(text);
                
                if (text.includes('Desktop Commander MCP STDIO Server starting')) {
                    statusBarItem.text = "$(sync~spin) ECHO MCP Loading...";
                }
            }
        });
        
        // Handle stderr
        mcpServerProcess.stderr?.on('data', (data: Buffer) => {
            outputChannel.append(`[ERROR] ${data.toString()}`);
        });
        
        // Handle exit
        mcpServerProcess.on('exit', (code) => {
            outputChannel.appendLine(`\n🔥 MCP Server exited with code ${code}`);
            mcpServerProcess = null;
            mcpInitialized = false;
            availableTools = [];
            isStarting = false;
            statusBarItem.text = "$(error) ECHO MCP Stopped";
            
            if (code !== 0) {
                vscode.window.showErrorMessage(`ECHO MCP Server crashed (exit code ${code}) - Auto-restart DISABLED`);
                outputChannel.appendLine(`⚠️ Auto-restart disabled to prevent crash loop`);
            }
        });
        
        outputChannel.appendLine('✅ MCP Server process started');
        isStarting = false;
        
    } catch (error: any) {
        outputChannel.appendLine(`❌ Failed to start MCP server: ${error.message}`);
        vscode.window.showErrorMessage(`Failed to start MCP server: ${error.message}`);
        statusBarItem.text = "$(error) ECHO MCP Error";
        isStarting = false;
    }
}

function stopMCPServer(): void {
    if (mcpServerProcess) {
        outputChannel.appendLine('🛑 Stopping MCP Server...');
        mcpServerProcess.kill();
        mcpServerProcess = null;
        mcpInitialized = false;
        availableTools = [];
        isStarting = false;
        statusBarItem.text = "$(circle-slash) ECHO MCP Stopped";
    }
}

async function restartMCPServer(): Promise<void> {
    outputChannel.appendLine('🔄 Restarting MCP Server...');
    stopMCPServer();
    await new Promise(resolve => setTimeout(resolve, 1000));
    await startMCPServer();
    await new Promise(resolve => setTimeout(resolve, 1000));
    if (mcpServerProcess) {
        await initializeMCP();
        await loadTools();
        await registerLanguageModelTools();
    }
}

async function checkServerHealth(): Promise<boolean> {
    if (!mcpServerProcess || !mcpInitialized) {
        return false;
    }
    
    try {
        const testResult = await callMCPTool('list_directory', { path: '.' });
        return testResult.success;
    } catch {
        return false;
    }
}
