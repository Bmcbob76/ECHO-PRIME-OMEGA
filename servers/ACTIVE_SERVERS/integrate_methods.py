# Integrate window control methods into bridge file

# Read methods file
with open(r'E:\ECHO_XV4\MLS\servers\windows_control_methods.py', 'r', encoding='utf-8') as f:
    methods = f.read()

# Read bridge file  
with open(r'E:\ECHO_XV4\MLS\servers\windows_api_mcp_bridge.py', 'r', encoding='utf-8') as f:
    bridge = f.read()

# Find where window_list ends
marker = '"count": len(windows)\n                }'

# Extract remaining methods (from window_find onwards)
find_start = methods.find('elif name == "window_find"')

if find_start > 0:
    remaining = methods[find_start:]
    
    # Insert after window_list  
    if marker in bridge:
        bridge = bridge.replace(marker, marker + '\n            \n' + remaining)
        
        # Write back
        with open(r'E:\ECHO_XV4\MLS\servers\windows_api_mcp_bridge.py', 'w', encoding='utf-8') as f:
            f.write(bridge)
        
        print('✅ SUCCESS: Window control methods integrated!')
        print(f'✅ Added {len(remaining)} characters of window control code')
    else:
        print('❌ ERROR: Could not find marker in bridge file')
else:
    print('❌ ERROR: Could not find window_find in methods file')
