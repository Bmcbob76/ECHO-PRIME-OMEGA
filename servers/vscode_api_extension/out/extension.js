"use strict";
/**
 * ECHO VS Code API Extension - Main Entry Point
 * Commander Bobby Don McWilliams II - Authority Level 11.0
 *
 * Provides REST API server for programmatic VS Code control
 * Part of ECHO_XV4 Unified Developer API System
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const api_server_1 = require("./api_server");
const command_bridge_1 = require("./command_bridge");
let apiServer = null;
let commandBridge = null;
let statusBarItem;
function activate(context) {
    console.log('ECHO VS Code API Extension - Activating...');
    // Initialize command bridge
    commandBridge = new command_bridge_1.CommandBridge(context);
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'echo.getApiStatus';
    context.subscriptions.push(statusBarItem);
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('echo.startApiServer', async () => {
        await startApiServer(context);
    }));
    context.subscriptions.push(vscode.commands.registerCommand('echo.stopApiServer', async () => {
        await stopApiServer();
    }));
    context.subscriptions.push(vscode.commands.registerCommand('echo.getApiStatus', async () => {
        showApiStatus();
    }));
    // Auto-start if configured
    const config = vscode.workspace.getConfiguration('echo');
    if (config.get('autoStart', true)) {
        startApiServer(context);
    }
    else {
        updateStatusBar('ECHO API: Stopped', '$(circle-slash)');
    }
    console.log('ECHO VS Code API Extension - Activated');
}
async function startApiServer(context) {
    if (apiServer) {
        vscode.window.showWarningMessage('ECHO API Server already running');
        return;
    }
    try {
        const config = vscode.workspace.getConfiguration('echo');
        const port = config.get('apiPort', 9001);
        apiServer = new api_server_1.ApiServer(port, commandBridge);
        await apiServer.start();
        updateStatusBar(`ECHO API: Running (${port})`, '$(check)');
        vscode.window.showInformationMessage(`ECHO API Server started on port ${port}`);
        console.log(`ECHO API Server started successfully on port ${port}`);
    }
    catch (error) {
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
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Failed to stop ECHO API Server: ${errorMessage}`);
    }
}
function showApiStatus() {
    if (apiServer && apiServer.isRunning()) {
        const port = apiServer.getPort();
        vscode.window.showInformationMessage(`ECHO API Server is running on port ${port}`, 'Stop Server').then(selection => {
            if (selection === 'Stop Server') {
                stopApiServer();
            }
        });
    }
    else {
        vscode.window.showInformationMessage('ECHO API Server is not running', 'Start Server').then(selection => {
            if (selection === 'Start Server') {
                vscode.commands.executeCommand('echo.startApiServer');
            }
        });
    }
}
function updateStatusBar(text, icon) {
    statusBarItem.text = `${icon} ${text}`;
    statusBarItem.show();
}
function deactivate() {
    console.log('ECHO VS Code API Extension - Deactivating...');
    if (apiServer) {
        apiServer.stop();
    }
    console.log('ECHO VS Code API Extension - Deactivated');
}
//# sourceMappingURL=extension.js.map