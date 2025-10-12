/**
 * ECHO VS Code API Server
 * REST API server for programmatic VS Code control
 * Commander Bobby Don McWilliams II - Authority Level 11.0
 */

import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import * as http from 'http';
import * as vscode from 'vscode';
import { CommandBridge } from './command_bridge';

export class ApiServer {
    private app: express.Application;
    private server: http.Server | null = null;
    private port: number;
    private commandBridge: CommandBridge;
    private running: boolean = false;

    constructor(port: number, commandBridge: CommandBridge) {
        this.port = port;
        this.commandBridge = commandBridge;
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
    }

    private setupMiddleware() {
        // CORS configuration
        const config = vscode.workspace.getConfiguration('echo');
        const allowedOrigins = config.get<string[]>('allowedOrigins', [
            'http://localhost:9000',
            'http://localhost:8343'
        ]);

        this.app.use(cors({
            origin: allowedOrigins,
            methods: ['GET', 'POST', 'PUT', 'DELETE'],
            credentials: true
        }));

        this.app.use(bodyParser.json());
        this.app.use(bodyParser.urlencoded({ extended: true }));

        // Request logging
        this.app.use((req, res, next) => {
            console.log(`[ECHO API] ${req.method} ${req.path}`);
            next();
        });
    }

    private setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'OK',
                service: 'ECHO VS Code API',
                port: this.port,
                uptime: process.uptime(),
                authority_level: '11.0',
                timestamp: new Date().toISOString()
            });
        });

        // Get all available endpoints
        this.app.get('/api/endpoints', (req, res) => {
            res.json({
                endpoints: [
                    { path: '/health', method: 'GET', description: 'Health check' },
                    { path: '/api/endpoints', method: 'GET', description: 'List all endpoints' },
                    { path: '/vscode/open_file', method: 'POST', description: 'Open file in editor' },
                    { path: '/vscode/close_file', method: 'POST', description: 'Close file' },
                    { path: '/vscode/edit_text', method: 'POST', description: 'Edit text at position' },
                    { path: '/vscode/get_text', method: 'POST', description: 'Get text from file' },
                    { path: '/vscode/run_command', method: 'POST', description: 'Execute VS Code command' },
                    { path: '/vscode/get_selection', method: 'GET', description: 'Get current selection' },
                    { path: '/vscode/set_selection', method: 'POST', description: 'Set selection' },
                    { path: '/vscode/find_replace', method: 'POST', description: 'Find and replace' },
                    { path: '/vscode/terminal_command', method: 'POST', description: 'Run terminal command' },
                    { path: '/vscode/workspace_files', method: 'GET', description: 'List workspace files' },
                    { path: '/vscode/active_file', method: 'GET', description: 'Get active file info' },
                    { path: '/vscode/save_file', method: 'POST', description: 'Save file' },
                    { path: '/vscode/format_document', method: 'POST', description: 'Format document' }
                ]
            });
        });

        // File operations
        this.app.post('/vscode/open_file', async (req, res) => {
            try {
                const { filePath, viewColumn } = req.body;
                const result = await this.commandBridge.openFile(filePath, viewColumn);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        this.app.post('/vscode/close_file', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.closeFile(filePath);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        this.app.post('/vscode/save_file', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.saveFile(filePath);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Text editing
        this.app.post('/vscode/edit_text', async (req, res) => {
            try {
                const { filePath, line, character, text, endLine, endCharacter } = req.body;
                const result = await this.commandBridge.editText(
                    filePath, line, character, text, endLine, endCharacter
                );
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        this.app.post('/vscode/get_text', async (req, res) => {
            try {
                const { filePath, startLine, endLine } = req.body;
                const result = await this.commandBridge.getText(filePath, startLine, endLine);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Selection operations
        this.app.get('/vscode/get_selection', async (req, res) => {
            try {
                const result = await this.commandBridge.getSelection();
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        this.app.post('/vscode/set_selection', async (req, res) => {
            try {
                const { startLine, startCharacter, endLine, endCharacter } = req.body;
                const result = await this.commandBridge.setSelection(
                    startLine, startCharacter, endLine, endCharacter
                );
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Command execution
        this.app.post('/vscode/run_command', async (req, res) => {
            try {
                const { command, args } = req.body;
                const result = await this.commandBridge.runCommand(command, args);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Find and replace
        this.app.post('/vscode/find_replace', async (req, res) => {
            try {
                const { find, replace, filePath, isRegex } = req.body;
                const result = await this.commandBridge.findReplace(find, replace, filePath, isRegex);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Terminal operations
        this.app.post('/vscode/terminal_command', async (req, res) => {
            try {
                const { command, terminalName } = req.body;
                const result = await this.commandBridge.runTerminalCommand(command, terminalName);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Workspace operations
        this.app.get('/vscode/workspace_files', async (req, res) => {
            try {
                const { pattern } = req.query;
                const result = await this.commandBridge.getWorkspaceFiles(pattern as string);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        this.app.get('/vscode/active_file', async (req, res) => {
            try {
                const result = await this.commandBridge.getActiveFileInfo();
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Format document
        this.app.post('/vscode/format_document', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.formatDocument(filePath);
                res.json({ success: true, data: result });
            } catch (error) {
                this.handleError(res, error);
            }
        });

        // Error handling middleware
        this.app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
            console.error('[ECHO API] Error:', err);
            res.status(500).json({
                success: false,
                error: err.message || 'Internal server error',
                authority_level: '11.0'
            });
        });
    }

    private handleError(res: express.Response, error: any) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error('[ECHO API] Error:', errorMessage);
        res.status(500).json({
            success: false,
            error: errorMessage
        });
    }

    async start(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.server = this.app.listen(this.port, () => {
                    this.running = true;
                    console.log(`[ECHO API] Server started on port ${this.port}`);
                    resolve();
                });

                this.server.on('error', (error: any) => {
                    this.running = false;
                    reject(error);
                });
            } catch (error) {
                this.running = false;
                reject(error);
            }
        });
    }

    async stop(): Promise<void> {
        return new Promise((resolve) => {
            if (this.server) {
                this.server.close(() => {
                    this.running = false;
                    console.log('[ECHO API] Server stopped');
                    resolve();
                });
            } else {
                this.running = false;
                resolve();
            }
        });
    }

    isRunning(): boolean {
        return this.running;
    }

    getPort(): number {
        return this.port;
    }
}
