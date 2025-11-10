"use strict";
/**
 * ECHO VS Code Command Bridge
 * Bridges REST API commands to VS Code API
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandBridge = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
class CommandBridge {
    constructor(context) {
        this.context = context;
    }
    /**
     * Open a file in the editor
     */
    async openFile(filePath, viewColumn) {
        const uri = vscode.Uri.file(filePath);
        const column = viewColumn || vscode.ViewColumn.One;
        const document = await vscode.workspace.openTextDocument(uri);
        const editor = await vscode.window.showTextDocument(document, column);
        return {
            filePath: document.fileName,
            lineCount: document.lineCount,
            languageId: document.languageId,
            cursorPosition: {
                line: editor.selection.active.line,
                character: editor.selection.active.character
            }
        };
    }
    /**
     * Close a file
     */
    async closeFile(filePath) {
        const uri = vscode.Uri.file(filePath);
        // Find the text editor for this file
        const editors = vscode.window.visibleTextEditors;
        const targetEditor = editors.find(e => e.document.uri.fsPath === uri.fsPath);
        if (targetEditor) {
            await vscode.window.showTextDocument(targetEditor.document);
            await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
            return { closed: true, filePath };
        }
        return { closed: false, filePath, message: 'File not open' };
    }
    /**
     * Save a file
     */
    async saveFile(filePath) {
        if (filePath) {
            const uri = vscode.Uri.file(filePath);
            const document = await vscode.workspace.openTextDocument(uri);
            const saved = await document.save();
            return { saved, filePath: document.fileName };
        }
        else {
            // Save active file
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                throw new Error('No active editor');
            }
            const saved = await editor.document.save();
            return { saved, filePath: editor.document.fileName };
        }
    }
    /**
     * Edit text at a specific position
     */
    async editText(filePath, line, character, text, endLine, endCharacter) {
        const uri = vscode.Uri.file(filePath);
        const document = await vscode.workspace.openTextDocument(uri);
        const editor = await vscode.window.showTextDocument(document);
        const startPos = new vscode.Position(line, character);
        const endPos = endLine !== undefined && endCharacter !== undefined
            ? new vscode.Position(endLine, endCharacter)
            : startPos;
        const range = new vscode.Range(startPos, endPos);
        const success = await editor.edit(editBuilder => {
            editBuilder.replace(range, text);
        });
        return {
            success,
            filePath: document.fileName,
            startLine: line,
            startCharacter: character,
            endLine: endLine || line,
            endCharacter: endCharacter || character,
            textLength: text.length
        };
    }
    /**
     * Get text from a file
     */
    async getText(filePath, startLine, endLine) {
        const uri = vscode.Uri.file(filePath);
        const document = await vscode.workspace.openTextDocument(uri);
        if (startLine !== undefined && endLine !== undefined) {
            const start = new vscode.Position(startLine, 0);
            const end = new vscode.Position(endLine, document.lineAt(endLine).text.length);
            const range = new vscode.Range(start, end);
            const text = document.getText(range);
            return {
                text,
                startLine,
                endLine,
                lineCount: endLine - startLine + 1
            };
        }
        return {
            text: document.getText(),
            lineCount: document.lineCount,
            filePath: document.fileName
        };
    }
    /**
     * Get current selection
     */
    async getSelection() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            throw new Error('No active editor');
        }
        const selection = editor.selection;
        const text = editor.document.getText(selection);
        return {
            filePath: editor.document.fileName,
            text,
            start: {
                line: selection.start.line,
                character: selection.start.character
            },
            end: {
                line: selection.end.line,
                character: selection.end.character
            },
            isEmpty: selection.isEmpty
        };
    }
    /**
     * Set selection
     */
    async setSelection(startLine, startCharacter, endLine, endCharacter) {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            throw new Error('No active editor');
        }
        const start = new vscode.Position(startLine, startCharacter);
        const end = new vscode.Position(endLine, endCharacter);
        editor.selection = new vscode.Selection(start, end);
        editor.revealRange(new vscode.Range(start, end));
        return {
            filePath: editor.document.fileName,
            start: { line: startLine, character: startCharacter },
            end: { line: endLine, character: endCharacter }
        };
    }
    /**
     * Run a VS Code command
     */
    async runCommand(command, args) {
        try {
            const result = await vscode.commands.executeCommand(command, ...(args || []));
            return {
                command,
                executed: true,
                result: result || 'Command executed successfully'
            };
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            throw new Error(`Command execution failed: ${errorMessage}`);
        }
    }
    /**
     * Find and replace text
     */
    async findReplace(find, replace, filePath, isRegex = false) {
        let document;
        let editor;
        if (filePath) {
            const uri = vscode.Uri.file(filePath);
            document = await vscode.workspace.openTextDocument(uri);
            editor = await vscode.window.showTextDocument(document);
        }
        else {
            editor = vscode.window.activeTextEditor;
            if (!editor) {
                throw new Error('No active editor');
            }
            document = editor.document;
        }
        const text = document.getText();
        let newText;
        let replacementCount = 0;
        if (isRegex) {
            const regex = new RegExp(find, 'g');
            newText = text.replace(regex, (match) => {
                replacementCount++;
                return replace;
            });
        }
        else {
            const parts = text.split(find);
            replacementCount = parts.length - 1;
            newText = parts.join(replace);
        }
        if (replacementCount > 0) {
            await editor.edit(editBuilder => {
                const fullRange = new vscode.Range(document.positionAt(0), document.positionAt(text.length));
                editBuilder.replace(fullRange, newText);
            });
        }
        return {
            filePath: document.fileName,
            replacementCount,
            find,
            replace,
            isRegex
        };
    }
    /**
     * Run command in integrated terminal
     */
    async runTerminalCommand(command, terminalName) {
        let terminal;
        if (terminalName) {
            // Find existing terminal with name
            terminal = vscode.window.terminals.find(t => t.name === terminalName)
                || vscode.window.createTerminal(terminalName);
        }
        else {
            // Use active terminal or create new one
            terminal = vscode.window.activeTerminal
                || vscode.window.createTerminal('ECHO Terminal');
        }
        terminal.show();
        terminal.sendText(command);
        return {
            terminal: terminal.name,
            command,
            executed: true
        };
    }
    /**
     * Get workspace files
     */
    async getWorkspaceFiles(pattern) {
        const searchPattern = pattern || '**/*';
        const uris = await vscode.workspace.findFiles(searchPattern, '**/node_modules/**');
        const files = uris.map(uri => ({
            path: uri.fsPath,
            name: path.basename(uri.fsPath),
            relativePath: vscode.workspace.asRelativePath(uri)
        }));
        return {
            files,
            count: files.length,
            pattern: searchPattern
        };
    }
    /**
     * Get active file info
     */
    async getActiveFileInfo() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return { active: false, message: 'No active editor' };
        }
        const document = editor.document;
        return {
            active: true,
            filePath: document.fileName,
            fileName: path.basename(document.fileName),
            languageId: document.languageId,
            lineCount: document.lineCount,
            isDirty: document.isDirty,
            cursorPosition: {
                line: editor.selection.active.line,
                character: editor.selection.active.character
            },
            selection: {
                start: {
                    line: editor.selection.start.line,
                    character: editor.selection.start.character
                },
                end: {
                    line: editor.selection.end.line,
                    character: editor.selection.end.character
                },
                isEmpty: editor.selection.isEmpty
            }
        };
    }
    /**
     * Format document
     */
    async formatDocument(filePath) {
        let document;
        if (filePath) {
            const uri = vscode.Uri.file(filePath);
            document = await vscode.workspace.openTextDocument(uri);
            await vscode.window.showTextDocument(document);
        }
        else {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                throw new Error('No active editor');
            }
            document = editor.document;
        }
        await vscode.commands.executeCommand('editor.action.formatDocument');
        return {
            filePath: document.fileName,
            formatted: true
        };
    }
}
exports.CommandBridge = CommandBridge;
//# sourceMappingURL=command_bridge.js.map