/**
 * Test Desktop Commander MCP Server Response
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

async function testMCPServer() {
    console.log('🧪 Testing Desktop Commander MCP Server...\n');

    try {
        // Create client
        const client = new Client(
            {
                name: 'test-client',
                version: '1.0.0'
            },
            {
                capabilities: {
                    tools: {}
                }
            }
        );

        // Create transport
        const serverPath = 'E:\\ECHO_XV4\\MLS\\servers\\node_modules\\@wonderwhy-er\\desktop-commander\\dist\\index.js';
        console.log('📡 Server path:', serverPath);

        const transport = new StdioClientTransport({
            command: 'node.exe',
            args: [serverPath]
        });

        // Connect
        console.log('🔌 Connecting...');
        await client.connect(transport);
        console.log('✅ Connected!\n');

        // Request tools
        console.log('📋 Requesting tools list...');
        const result = await client.request(
            { method: 'tools/list' },
            {}
        );

        console.log('\n📊 Raw Result:');
        console.log('Type:', typeof result);
        console.log('Keys:', Object.keys(result));
        console.log('\nFull response:');
        console.log(JSON.stringify(result, null, 2));

        // Check if tools property exists
        if (result.tools) {
            console.log(`\n✅ Found ${result.tools.length} tools`);
            console.log('\nFirst 3 tools:');
            result.tools.slice(0, 3).forEach((tool, i) => {
                console.log(`  ${i + 1}. ${tool.name}`);
            });
        } else {
            console.log('\n❌ No tools property in response');
        }

        // Close
        await client.close();
        console.log('\n✅ Test complete');

    } catch (error) {
        console.error('\n❌ Test failed:');
        console.error('Name:', error.name);
        console.error('Message:', error.message);
        console.error('Stack:', error.stack);
    }
}

testMCPServer();
