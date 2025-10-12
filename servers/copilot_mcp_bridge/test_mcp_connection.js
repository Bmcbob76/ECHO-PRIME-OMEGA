/**
 * Test Desktop Commander MCP Connection
 * Verifies tools can be fetched
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';

async function testConnection() {
    console.log('🧪 Testing Desktop Commander MCP Connection...\n');
    
    const serverPath = 'E:\\ECHO_XV4\\CLAUDE_EXT_BACKUP\\ant.dir.gh.wonderwhy-er.desktopcommandermcp\\dist\\index.js';
    
    console.log(`📍 Server path: ${serverPath}`);
    console.log(`🚀 Spawning MCP server...\n`);
    
    try {
        // Spawn the server
        const serverProcess = spawn('node', [serverPath], {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        // Create transport
        const transport = new StdioClientTransport({
            command: 'node',
            args: [serverPath]
        });
        
        // Create client
        const client = new Client({
            name: 'test-client',
            version: '1.0.0'
        }, {
            capabilities: {}
        });
        
        console.log('🔌 Connecting to MCP server...');
        await client.connect(transport);
        console.log('✅ Connected!\n');
        
        console.log('📡 Requesting tools list...');
        const response = await client.request(
            { method: 'tools/list' },
            {}
        );
        
        console.log('\n📦 Raw response:', JSON.stringify(response, null, 2));
        
        const tools = response.result?.tools || response.tools || [];
        
        console.log(`\n✅ Found ${tools.length} tools:`);
        tools.forEach((tool, i) => {
            console.log(`   ${i + 1}. ${tool.name}`);
        });
        
        await client.close();
        serverProcess.kill();
        
        console.log('\n🎉 Test PASSED! MCP connection working.');
        
    } catch (error) {
        console.error('\n❌ Test FAILED!');
        console.error('Error:', error.message);
        console.error('\nStack:', error.stack);
        process.exit(1);
    }
}

testConnection();
