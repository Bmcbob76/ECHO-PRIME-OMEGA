/**
 * ECHO VS Code API Extension - Main Entry Point
 * Commander Bobby Don McWilliams II - Authority Level 11.0
 * 
 * Provides REST API server for programmatic VS Code control
 * Part of ECHO_XV4 Unified Developer API System
 */

import * as vscode from 'vscode';
import { ApiServer } from './api_server';
import { CommandBridge } from './command_bridge';

let apiServer: ApiServer | null = null;
let commandBridge: CommandBridge | null = null;
let statusBarItem: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
    console.log('ECHO VS Code API Extension - Activating...');
    
    // Initialize command bridge
    commandBridge = new CommandBridge(context);
    
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'echo.getApiStatus';
    context.subscriptions.push(statusBarItem);
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.startApiServer', async () => {
            await startApiServer(context);
        })
    );
    
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.stopApiServer', async () => {
            await stopApiServer();
        })
    );
    
    context.subscriptions.push(
        vscode.commands.registerCommand('echo.getApiStatus', async () => {
            showApiStatus();
        })
    );
    
    // Auto-start if configured
    const config = vscode.workspace.getConfiguration('echo');
    if (config.get<boolean>('autoStart', true)) {
        startApiServer(context);
    } else {
        updateStatusBar('ECHO API: Stopped', '$(circle-slash)');
    }
    
    console.log('ECHO VS Code API Extension - Activated');
}

async function startApiServer(context: vscode.ExtensionContext) {
    if (apiServer) {
        vscode.window.showWarningMessage('ECHO API Server already running');
        return;
    }
    
    try {
        const config = vscode.workspace.getConfiguration('echo');
        const port = config.get<number>('apiPort', 9001);
        
        apiServer = new ApiServer(port, commandBridge!);
        await apiServer.start();
        
        updateStatusBar(`ECHO API: Running (${port})`, '$(check)');
        vscode.window.showInformationMessage(`ECHO API Server started on port ${port}`);
        
        console.log(`ECHO API Server started successfully on port ${port}`);
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Failed to start ECHO API Server: ${errorMessage}`);
        updateStatusBar('ECHO API: Error', '$(error)');
        apiServer = null;
    }
}

async function stopApiServer() {
    if (!apiServer) {
        vscode.window.showWarningMessage('ECHO API Server not running');
        return;
    }
    
    try {
        await apiServer.stop();
        apiServer = null;
        updateStatusBar('ECHO API: Stopped', '$(circle-slash)');
        vscode.window.showInformationMessage('ECHO API Server stopped');
        console.log('ECHO API Server stopped');
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Failed to stop ECHO API Server: ${errorMessage}`);
    }
}

function showApiStatus() {
    if (apiServer && apiServer.isRunning()) {
        const port = apiServer.getPort();
        vscode.window.showInformationMessage(
            `ECHO API Server is running on port ${port}`,
            'Stop Server'
        ).then(selection => {
            if (selection === 'Stop Server') {
                stopApiServer();
            }
        });
    } else {
        vscode.window.showInformationMessage(
            'ECHO API Server is not running',
            'Start Server'
        ).then(selection => {
            if (selection === 'Start Server') {
                vscode.commands.executeCommand('echo.startApiServer');
            }
        });
    }
}

function updateStatusBar(text: string, icon: string) {
    statusBarItem.text = `${icon} ${text}`;
    statusBarItem.show();
}

export function deactivate() {
    console.log('ECHO VS Code API Extension - Deactivating...');
    if (apiServer) {
        apiServer.stop();
    }
    console.log('ECHO VS Code API Extension - Deactivated');
}
