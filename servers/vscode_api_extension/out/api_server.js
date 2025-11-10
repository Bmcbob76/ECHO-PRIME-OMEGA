"use strict";
/**
 * ECHO VS Code API Server
 * REST API server for programmatic VS Code control
 * Commander Bobby Don McWilliams II - Authority Level 11.0
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiServer = void 0;
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const body_parser_1 = __importDefault(require("body-parser"));
const vscode = __importStar(require("vscode"));
class ApiServer {
    constructor(port, commandBridge) {
        this.server = null;
        this.running = false;
        this.port = port;
        this.commandBridge = commandBridge;
        this.app = (0, express_1.default)();
        this.setupMiddleware();
        this.setupRoutes();
    }
    setupMiddleware() {
        // CORS configuration
        const config = vscode.workspace.getConfiguration('echo');
        const allowedOrigins = config.get('allowedOrigins', [
            'http://localhost:9000',
            'http://localhost:8343'
        ]);
        this.app.use((0, cors_1.default)({
            origin: allowedOrigins,
            methods: ['GET', 'POST', 'PUT', 'DELETE'],
            credentials: true
        }));
        this.app.use(body_parser_1.default.json());
        this.app.use(body_parser_1.default.urlencoded({ extended: true }));
        // Request logging
        this.app.use((req, res, next) => {
            console.log(`[ECHO API] ${req.method} ${req.path}`);
            next();
        });
    }
    setupRoutes() {
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
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        this.app.post('/vscode/close_file', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.closeFile(filePath);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        this.app.post('/vscode/save_file', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.saveFile(filePath);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Text editing
        this.app.post('/vscode/edit_text', async (req, res) => {
            try {
                const { filePath, line, character, text, endLine, endCharacter } = req.body;
                const result = await this.commandBridge.editText(filePath, line, character, text, endLine, endCharacter);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        this.app.post('/vscode/get_text', async (req, res) => {
            try {
                const { filePath, startLine, endLine } = req.body;
                const result = await this.commandBridge.getText(filePath, startLine, endLine);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Selection operations
        this.app.get('/vscode/get_selection', async (req, res) => {
            try {
                const result = await this.commandBridge.getSelection();
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        this.app.post('/vscode/set_selection', async (req, res) => {
            try {
                const { startLine, startCharacter, endLine, endCharacter } = req.body;
                const result = await this.commandBridge.setSelection(startLine, startCharacter, endLine, endCharacter);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Command execution
        this.app.post('/vscode/run_command', async (req, res) => {
            try {
                const { command, args } = req.body;
                const result = await this.commandBridge.runCommand(command, args);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Find and replace
        this.app.post('/vscode/find_replace', async (req, res) => {
            try {
                const { find, replace, filePath, isRegex } = req.body;
                const result = await this.commandBridge.findReplace(find, replace, filePath, isRegex);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Terminal operations
        this.app.post('/vscode/terminal_command', async (req, res) => {
            try {
                const { command, terminalName } = req.body;
                const result = await this.commandBridge.runTerminalCommand(command, terminalName);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Workspace operations
        this.app.get('/vscode/workspace_files', async (req, res) => {
            try {
                const { pattern } = req.query;
                const result = await this.commandBridge.getWorkspaceFiles(pattern);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        this.app.get('/vscode/active_file', async (req, res) => {
            try {
                const result = await this.commandBridge.getActiveFileInfo();
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Format document
        this.app.post('/vscode/format_document', async (req, res) => {
            try {
                const { filePath } = req.body;
                const result = await this.commandBridge.formatDocument(filePath);
                res.json({ success: true, data: result });
            }
            catch (error) {
                this.handleError(res, error);
            }
        });
        // Error handling middleware
        this.app.use((err, req, res, next) => {
            console.error('[ECHO API] Error:', err);
            res.status(500).json({
                success: false,
                error: err.message || 'Internal server error',
                authority_level: '11.0'
            });
        });
    }
    handleError(res, error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error('[ECHO API] Error:', errorMessage);
        res.status(500).json({
            success: false,
            error: errorMessage
        });
    }
    async start() {
        return new Promise((resolve, reject) => {
            try {
                this.server = this.app.listen(this.port, () => {
                    this.running = true;
                    console.log(`[ECHO API] Server started on port ${this.port}`);
                    resolve();
                });
                this.server.on('error', (error) => {
                    this.running = false;
                    reject(error);
                });
            }
            catch (error) {
                this.running = false;
                reject(error);
            }
        });
    }
    async stop() {
        return new Promise((resolve) => {
            if (this.server) {
                this.server.close(() => {
                    this.running = false;
                    console.log('[ECHO API] Server stopped');
                    resolve();
                });
            }
            else {
                this.running = false;
                resolve();
            }
        });
    }
    isRunning() {
        return this.running;
    }
    getPort() {
        return this.port;
    }
}
exports.ApiServer = ApiServer;
//# sourceMappingURL=api_server.js.map