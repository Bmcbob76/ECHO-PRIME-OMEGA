# PHOENIX SENTINEL 🔥🛡️
**Autonomous Windows Guardian with JARVIS Voice Interface**

## Overview
Phoenix Sentinel is an advanced AI system that combines three powerful skill sets into one unified autonomous guardian:

1. **JARVIS Voice Interface** - Natural language control of Windows systems
2. **Autonomous CPU Controller** - Self-managing process and resource optimization
3. **Windows API Mastery** - Deep system integration with 500+ API endpoints

## Authority Level: 11.0

## Skills Integration

### 🎤 JARVIS Project
- Voice-activated wake word detection ("sentinel")
- Natural language command processing
- JARVIS-style personality and responses
- Proactive assistance and status reporting
- Multi-turn conversation support

### 🤖 Autonomous CPU
- Self-managing process optimization
- Real-time resource monitoring and allocation
- Predictive decision making
- Machine learning-based execution optimization
- Autonomous scaling and throttling

### 🖥️ Windows API Mastery
- SeDebugPrivilege elevation
- Process injection capabilities
- Priority management (idle → realtime)
- Memory and thread control
- Deep system integration

### ⚕️ GS343 Healing
- Pattern-based error detection
- Automatic recovery protocols
- Self-healing capabilities
- Learning from failures

## Features

### Voice Commands
```
"Sentinel, status report"
"Sentinel, optimize memory"
"Sentinel, kill process"
"Sentinel, set priority high"
"Sentinel, free memory"
"Sentinel, optimize system"
```

### Autonomous Operations
- **CPU Monitoring**: Continuous real-time tracking
- **Automatic Throttling**: Reduces priority of high-CPU processes
- **Memory Management**: Automatic garbage collection when needed
- **Process Optimization**: Self-adjusting based on system load
- **Predictive Scaling**: Anticipates resource needs

### Windows Integration
- **Privilege Elevation**: Automatic SeDebugPrivilege enabling
- **Process Control**: Create, terminate, suspend, resume
- **Memory Operations**: Virtual memory allocation and management
- **Thread Management**: Multi-threaded operation control
- **Priority Management**: Real-time priority adjustment

## Architecture

```
PhoenixSentinel (Orchestrator)
├── WindowsAPIMaster (Windows API Integration)
│   ├── enable_debug_privilege()
│   ├── inject_dll()
│   └── set_process_priority()
│
├── AutonomousCPUController (Self-Management)
│   ├── autonomous_loop()
│   ├── collect_metrics()
│   ├── make_decision()
│   └── execute_decision()
│
├── JarvisVoiceInterface (Natural Language)
│   ├── listen_loop()
│   ├── process_command()
│   └── execute_command()
│
└── GS343Healer (Auto-Recovery)
    ├── analyze_and_heal()
    └── apply_healing()
```

## Installation & Setup

### Requirements
```bash
pip install psutil pywin32 pyttsx3 SpeechRecognition pyaudio
```

### Microphone Setup
- Ensure microphone is connected and configured
- Adjust ambient noise settings if needed
- Test with `python -m speech_recognition`

### Permissions
- Run with Administrator privileges for full API access
- SeDebugPrivilege will be automatically enabled
- Some operations require elevated rights

## Usage

### Starting Phoenix Sentinel
```bash
H:\Tools\python.exe phoenix_sentinel_core.py
```

### Voice Activation
1. Wait for "Phoenix Sentinel initialized"
2. Say wake word: "**Sentinel**"
3. Wait for "Yes, sir?"
4. Give your command

### Example Session
```
[PHOENIX SENTINEL] Listening...
User: "Sentinel"
JARVIS: "Yes, sir?"
User: "Status report"
JARVIS: "CPU at 45.3 percent, memory at 62.1 percent. 247 processes running."
```

## Autonomous Operation

The system runs two concurrent loops:

1. **Autonomous CPU Loop** (2-second intervals)
   - Monitors system metrics
   - Makes optimization decisions
   - Executes autonomous actions
   - Learns from outcomes

2. **Voice Listen Loop** (continuous)
   - Listens for wake word
   - Processes natural language commands
   - Executes Windows API operations
   - Provides JARVIS-style feedback

## Integration with ECHO_PRIME

### MLS Registration
Automatically registers with Master Launcher System:
```json
{
  "name": "PHOENIX_SENTINEL",
  "type": "AUTONOMOUS_GUARDIAN",
  "authority": 11.0,
  "capabilities": [
    "voice_control",
    "process_management", 
    "resource_optimization",
    "threat_detection",
    "self_healing",
    "windows_api_mastery"
  ]
}
```

### Crystal Memory Integration
- Logs all decisions to M:\MEMORY_ORCHESTRATION
- Stores execution history
- Learning data persists across sessions

### Voice System Hub
- Can integrate with existing voice personalities (C3PO, Bree, Echo)
- Unified voice command routing
- Personality switching on demand

## Advanced Features

### Process Injection
```python
sentinel.api_master.inject_dll(target_pid, "custom_hook.dll")
```

### Priority Management
```python
sentinel.api_master.set_process_priority(pid, "realtime")
```

### Autonomous Decision Override
```python
sentinel.cpu_controller.cpu_threshold = 90  # Adjust threshold
```

## Safety & Security

⚠️ **Important Notes:**
- Runs with Administrator privileges
- Can inject into processes
- Can terminate system processes
- Has real-time priority access
- Use responsibly and ethically
- Test in safe environment first
- DLL injection disabled by default in config

### GS343 Safety Protocols
- Automatic error recovery
- Pattern-based healing
- Prevents cascade failures
- Logs all healing actions

## Troubleshooting

### Voice Recognition Issues
- Check microphone permissions
- Adjust ambient noise threshold
- Verify Google Speech API access
- Test with: `python -m speech_recognition`

### Permission Errors
- Run as Administrator
- Check SeDebugPrivilege status
- Verify user has necessary rights

### High CPU Usage
- Adjust autonomous_cpu thresholds in config.json
- Increase decision_interval_seconds
- Disable learning temporarily

## Configuration

Edit `config.json` to customize:
- CPU/memory thresholds
- Voice settings (wake word, rate, volume)
- Logging levels
- Auto-healing behavior
- MLS integration

## Logging

All operations logged to:
- **File**: `sentinel.log`
- **Console**: Real-time output
- **Format**: `timestamp | component | level | message`

## Future Enhancements

- [ ] Multi-language support
- [ ] GPU monitoring and optimization
- [ ] Network traffic analysis
- [ ] Threat detection AI
- [ ] Cloud synchronization
- [ ] Mobile app control
- [ ] Gesture recognition

## Credits

**Skills Used:**
- `jarvis-project` - AI assistant with natural language
- `autonomous-cpu` - Self-directed CPU operations  
- `windows-api-mastery` - 500+ Windows API endpoints

**Authority Level:** 11.0  
**Commander:** Bobby Don McWilliams II (BROTHER)

## License

Part of ECHO_XV4 system - Authority Level 11.0

---

**"Your autonomous guardian awaits - Authority 11.0"** 🔥🛡️
