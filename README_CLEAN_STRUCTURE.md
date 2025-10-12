# 🚀 MLS LAUNCHER - CLEAN DIRECTORY STRUCTURE

## Commander Bobby Don McWilliams II - Authority Level 11.0

### CORE FILES (DO NOT MOVE):

- `master_modular_launcher_enhanced.py` - Main launcher (THE BEAST!)
- `server_registry.json` - Server configuration registry
- `config.yaml` - Launcher configuration
- `server_manager.py` - Server management utilities
- `ECHO_MCP_MASTER_LAUNCHER.py` - MCP integration launcher

### STARTUP FILES:

- `LAUNCH_NOW.bat` - Quick launcher
- `RUN_LAUNCHER.bat` - Alternative launcher

### DIRECTORIES:

- `servers/` - All server files (AUTO-DISCOVERED)
- `modules/` - Launcher modules and plugins
- `logs/` - Runtime logs
- `static/` - Web interface assets
- `BACKUPS/` - System backups
- `venv/` - Python virtual environment

### ARCHIVED:

- `DOCUMENTATION_ARCHIVE/` - All docs, old launchers, tests moved here

### WHY GREP_SEARCH GETS STUCK:

1. **Large binary files** in cache/venv
2. **Infinite regex patterns**
3. **Memory limits** with huge log files
4. **Timeout issues** scanning deep directories

**SOLUTION**: Use `list_dir` and `run_in_terminal` instead of `grep_search` for file operations!

🔥 **LAUNCHER IS NOW CLEAN AND FOCUSED!** 🔥
