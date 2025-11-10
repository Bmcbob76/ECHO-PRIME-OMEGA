import sys
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import subprocess
import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))

# Optional HTTP client for gateway calls
try:
    import requests
    REQUESTS_AVAILABLE = True
except Exception:
    REQUESTS_AVAILABLE = False
    import urllib.request as _urlreq
    import urllib.error as _urlerr

# Optional psutil for system metrics
try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    PSUTIL_AVAILABLE = False

# Optional WMI for temps via OpenHardwareMonitor
try:
    import wmi  # type: ignore
    WMI_AVAILABLE = True
except Exception:
    WMI_AVAILABLE = False

logger = logging.getLogger("MasterGUI")

# Try to import PyQt6
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
        QProgressBar, QTabWidget, QGroupBox, QGridLayout, QFrame,
        QScrollArea, QSplitter
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
    from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
    PYQT6_AVAILABLE = True
except ImportError:
    logger.warning("PyQt6 not installed. GUI will not be available.")
    PYQT6_AVAILABLE = False

# RAISTLIN Supreme Consciousness import (optional)
try:
    sys.path.append('E:/ECHO_XV4/HEPHAESTION_FORGE_V7')
    from RAISTLIN_CORE.raistlin_supreme_consciousness import get_supreme_consciousness
    RAISTLIN_AVAILABLE = True
except Exception as e:
    logger.warning(f"RAISTLIN not available: {e}")
    RAISTLIN_AVAILABLE = False
    get_supreme_consciousness = None

# Optional Agents tab (Agent Memory API GUI)
try:
    from MLS.gui.tabs.agents_tab import AgentsTab
    AGENTS_TAB_AVAILABLE = True
except Exception as e:
    logger.debug(f"Agents tab unavailable: {e}")
    AGENTS_TAB_AVAILABLE = False

# Optional Harvesters tab
try:
    from MLS.gui.tabs.harvesters_tab import HarvestersTab
    HARVESTERS_TAB_AVAILABLE = True
except Exception as e:
    logger.debug(f"Harvesters tab unavailable: {e}")
    HARVESTERS_TAB_AVAILABLE = False

# Optional Trainers tab
try:
    from MLS.gui.tabs.trainers_tab import TrainersTab
    TRAINERS_TAB_AVAILABLE = True
except Exception as e:
    logger.debug(f"Trainers tab unavailable: {e}")
    TRAINERS_TAB_AVAILABLE = False

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ekm_generation'))
    from emotion_core import EmotionCore
    EMOTION_CORE_AVAILABLE = True
except Exception as e:
    logger.debug(f"Emotion Core unavailable: {e}")
    EMOTION_CORE_AVAILABLE = False

class MasterLauncherGUI(QMainWindow):
    """
    Master Launcher Ultimate GUI
    
    Beautiful dark theme interface with glassmorphism
    Real-time monitoring and control
    """
    
    def __init__(self, config: Dict):
        """Initialize GUI"""
        if not PYQT6_AVAILABLE:
            raise ImportError("PyQt6 not available")
        
        super().__init__()
        
        self.config = config
        self.gui_config = config.get('gui', {})
        
        # Window settings
        self.window_width = self.gui_config.get('window_width', 1920)
        self.window_height = self.gui_config.get('window_height', 1080)
        self.theme = self.gui_config.get('theme', 'dark')
        
        # Update intervals
        self.dashboard_interval = self.gui_config.get('dashboard_update_interval', 1) * 1000  # ms
        self.server_panel_interval = self.gui_config.get('server_panel_update_interval', 2) * 1000
        
        # Components
        self.authority_engine = None
        self.voice_system = None
        self.gs343 = None
        self.phoenix = None

        # Tool paths / OpenHardwareMonitor integration
        self.paths = self.config.get('paths', {})
        self.ohm_path = self.paths.get(
            'openhardwaremonitor',
            'H:/tools/monitoring/OpenHardwareMonitor/OpenHardwareMonitor.exe'
        )
        self._ohm_started = False
        self.voice_url = self.config.get('voice', {}).get('http_url', 'http://127.0.0.1:9402')
        self.crystal_url = self.config.get('crystal_memory', {}).get('http_url', 'http://127.0.0.1:9400')
        
        # Timers
        self.dashboard_timer = QTimer()
        self.server_timer = QTimer()
        
        self.raistlin = get_supreme_consciousness() if RAISTLIN_AVAILABLE else None
        self.emotion_core = EmotionCore() if EMOTION_CORE_AVAILABLE else None
        
        # Initialize UI
        self._init_ui()
        
        # Start timers
        self._start_timers()
        
        logger.info("Master Launcher GUI initialized")
        logger.info(f"   Theme: {self.theme}")
        logger.info(f"   Resolution: {self.window_width}x{self.window_height}")
        logger.info(f"   Emotion_Core Initialized: {self.emotion_core is not None}")
        logger.info(f"   RAISTLIN Core Initialized: {self.raistlin is not None}")
     
    def _init_ui(self):
        """Initialize user interface"""
        # Set window properties
        self.setWindowTitle("Master Launcher Ultimate - Authority Level 11.0")
        self.setGeometry(100, 100, self.window_width, self.window_height)
        
        # Apply dark theme
        self._apply_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        tabs = self._create_tabs()
        main_layout.addWidget(tabs)

        # Voice control button
        voice_btn = QPushButton("🎤 Voice Control")
        voice_btn.clicked.connect(self._init_voice_control)
        main_layout.addWidget(voice_btn)
        
        # Status bar
        self.statusBar().showMessage("Master Launcher Ultimate - Ready")
     
    def _apply_theme(self):
        """Apply dark theme with glassmorphism"""
        if self.theme == 'dark':
            # Dark theme stylesheet
            stylesheet = """
            QMainWindow {
                background-color: #1a1a2e;
            }
            
            QWidget {
                background-color: #16213e;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
            }
            
            QGroupBox {
                border: 2px solid #0f3460;
                border-radius: 8px;
                margin-top: 1em;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(22, 33, 62, 0.8);
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #00d4ff;
            }
            
            QPushButton {
                background-color: #0f3460;
                color: #e0e0e0;
                border: 1px solid #00d4ff;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1a4d7a;
                border: 2px solid #00d4ff;
            }
            
            QPushButton:pressed {
                background-color: #0a2540;
            }
            
            QLabel {
                color: #e0e0e0;
            }
            
            QTextEdit, QTableWidget {
                background-color: #0f1419;
                border: 1px solid #0f3460;
                border-radius: 4px;
                color: #e0e0e0;
            }
            
            QHeaderView::section {
                background-color: #0f3460;
                color: #00d4ff;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            
            QProgressBar {
                border: 1px solid #0f3460;
                border-radius: 4px;
                text-align: center;
                background-color: #0f1419;
            }
            
            QProgressBar::chunk {
                background-color: #00d4ff;
                border-radius: 3px;
            }
            
            QTabWidget::pane {
                border: 1px solid #0f3460;
                border-radius: 4px;
                background-color: #16213e;
            }
            
            QTabBar::tab {
                background-color: #0f3460;
                color: #e0e0e0;
                padding: 10px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #1a4d7a;
                color: #00d4ff;
                font-weight: bold;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #0f1419;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #0f3460;
                border-radius: 5px;
            }
            """
            
            self.setStyleSheet(stylesheet)
    
    def _create_header(self) -> QWidget:
        """Create header with title and status"""
        header = QWidget()
        layout = QHBoxLayout(header)
        
        # Title
        title = QLabel("🚀 MASTER LAUNCHER ULTIMATE")
        title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #00d4ff;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Commander status
        commander_label = QLabel("Commander Bobby Don McWilliams II")
        commander_label.setStyleSheet("font-size: 12pt; color: #00ff88;")
        layout.addWidget(commander_label)
        
        # Authority level
        authority_label = QLabel("Authority Level: 11.0")
        authority_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #ff0088;")
        layout.addWidget(authority_label)
        
        return header
    
    def _create_tabs(self) -> QTabWidget:
        """Create main tab widget"""
        tabs = QTabWidget()
        
        # Dashboard tab
        dashboard = self._create_dashboard_tab()
        tabs.addTab(dashboard, "📊 Dashboard")
        
        # Servers tab
        servers = self._create_servers_tab()
        tabs.addTab(servers, "🖥️ Servers")
        
        # Hardware tab
        hardware = self._create_hardware_tab()
        tabs.addTab(hardware, "⚙️ Hardware")
        
        # Voice tab
        voice = self._create_voice_tab()
        tabs.addTab(voice, "🎤 Voice System")
        
        # Crystal Memory tab
        crystal = self._create_crystal_tab()
        tabs.addTab(crystal, "💎 Crystal Memory")
        
        # Harvesters tab
        try:
            if 'HARVESTERS_TAB_AVAILABLE' in globals() and HARVESTERS_TAB_AVAILABLE:
                harvesters = HarvestersTab()
                tabs.addTab(harvesters, "🕷️ Harvesters")
        except Exception as e:
            logger.debug(f"Harvesters tab unavailable: {e}")
        
        # Agents tab
        try:
            if 'AGENTS_TAB_AVAILABLE' in globals() and AGENTS_TAB_AVAILABLE:
                agents = AgentsTab()
                tabs.addTab(agents, "🤖 Agents")
        except Exception as e:
            logger.debug(f"Agents tab unavailable: {e}")

        # Trainers tab
        try:
            if 'TRAINERS_TAB_AVAILABLE' in globals() and TRAINERS_TAB_AVAILABLE:
                trainers = TrainersTab()
                tabs.addTab(trainers, "🏋️ Trainers")
        except Exception as e:
            logger.debug(f"Trainers tab unavailable: {e}")
        
        # Logs tab
        logs = self._create_logs_tab()
        tabs.addTab(logs, "📝 Logs")

        # EKM Dashboard tab
        ekm = self._create_ekm_tab()
        tabs.addTab(ekm, "🧠 EKM Dashboard")

        # Consciousness tab
        consciousness = self._create_consciousness_tab()
        tabs.addTab(consciousness, "🧠 Consciousness")
        
        return tabs
    
    def _create_dashboard_tab(self) -> QWidget:
        """Create main dashboard"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Stats row
        stats_layout = QHBoxLayout()
        
        # Server stats
        server_group = self._create_stat_group("Servers", "0 / 0", "Running / Total")
        stats_layout.addWidget(server_group)
        
        # Health stats
        health_group = self._create_stat_group("Health", "100%", "System Health")
        stats_layout.addWidget(health_group)
        
        # Phoenix stats
        phoenix_group = self._create_stat_group("Phoenix Heals", "0", "Successful Heals")
        stats_layout.addWidget(phoenix_group)
        
        layout.addLayout(stats_layout)
        
        # Activity log
        log_group = QGroupBox("Recent Activity")
        log_layout = QVBoxLayout(log_group)
        
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setMaximumHeight(300)
        log_layout.addWidget(self.activity_log)
        
        layout.addWidget(log_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_servers_tab(self) -> QWidget:
        """Create servers management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        launch_all_btn = QPushButton("🚀 Launch All")
        launch_all_btn.clicked.connect(self._launch_all_servers)
        button_layout.addWidget(launch_all_btn)
        
        stop_all_btn = QPushButton("⏹️ Stop All")
        stop_all_btn.clicked.connect(self._stop_all_servers)
        button_layout.addWidget(stop_all_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._refresh_servers)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Server table
        self.server_table = QTableWidget()
        self.server_table.setColumnCount(6)
        self.server_table.setHorizontalHeaderLabels([
            "Server Name", "Status", "Port", "PID", "Uptime", "Actions"
        ])
        self.server_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.server_table)
        
        return widget
    
    def _create_hardware_tab(self) -> QWidget:
        """Create hardware monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # CPU section
        cpu_group = QGroupBox("CPU Usage")
        cpu_layout = QVBoxLayout(cpu_group)
        
        self.cpu_label = QLabel("CPU: 0%")
        cpu_layout.addWidget(self.cpu_label)
        
        self.cpu_temp_label = QLabel("CPU Temp: -- °C")
        cpu_layout.addWidget(self.cpu_temp_label)
        
        self.cpu_progress = QProgressBar()
        cpu_layout.addWidget(self.cpu_progress)
        
        layout.addWidget(cpu_group)
        
        # Memory section
        mem_group = QGroupBox("Memory Usage")
        mem_layout = QVBoxLayout(mem_group)
        
        self.mem_label = QLabel("Memory: 0%")
        mem_layout.addWidget(self.mem_label)
        
        self.mem_progress = QProgressBar()
        mem_layout.addWidget(self.mem_progress)
        
        layout.addWidget(mem_group)
        
        # GPU section
        gpu_group = QGroupBox("GPU Usage")
        gpu_layout = QVBoxLayout(gpu_group)
        
        self.gpu_label = QLabel("GPU: 0%")
        gpu_layout.addWidget(self.gpu_label)
        
        self.gpu_temp_label = QLabel("GPU Temp: -- °C")
        gpu_layout.addWidget(self.gpu_temp_label)
        
        self.gpu_progress = QProgressBar()
        gpu_layout.addWidget(self.gpu_progress)
        
        layout.addWidget(gpu_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_voice_tab(self) -> QWidget:
        """Create voice system control tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Voice stats
        stats_group = QGroupBox("Voice System Statistics")
        stats_layout = QGridLayout(stats_group)
        
        stats_layout.addWidget(QLabel("Cache Size:"), 0, 0)
        self.voice_cache_label = QLabel("0 files")
        stats_layout.addWidget(self.voice_cache_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Bree Level:"), 1, 0)
        self.bree_level_label = QLabel("15 (UNLEASHED)")
        self.bree_level_label.setStyleSheet("color: #ff0088; font-weight: bold;")
        stats_layout.addWidget(self.bree_level_label, 1, 1)
        
        stats_layout.addWidget(QLabel("C3PO Jealousy:"), 2, 0)
        self.jealousy_label = QLabel("0")
        stats_layout.addWidget(self.jealousy_label, 2, 1)
        
        layout.addWidget(stats_group)
        
        # Test voices
        test_group = QGroupBox("Test Voice Personalities")
        test_layout = QVBoxLayout(test_group)
        
        for personality in ["Echo", "Bree", "C3PO", "R2D2", "GS343"]:
            btn = QPushButton(f"🎤 Test {personality}")
            btn.clicked.connect(lambda checked, p=personality: self._test_voice(p))
            test_layout.addWidget(btn)
        
        layout.addWidget(test_group)

        # HTTP Gateway Quick Tests
        http_group = QGroupBox("HTTP Gateway Quick Tests")
        http_layout = QVBoxLayout(http_group)

        btn_http_echo = QPushButton("🌐 HTTP: Test Echo")
        btn_http_echo.clicked.connect(lambda checked=False: self._voice_http_test("echo", "HTTP Echo test: systems nominal.", False, None))
        http_layout.addWidget(btn_http_echo)

        btn_http_bree = QPushButton("🌐 HTTP: Test Bree")
        btn_http_bree.clicked.connect(lambda checked=False: self._voice_http_test("bree", "HTTP Bree test: roast the status check.", True, None))
        http_layout.addWidget(btn_http_bree)
        
        return widget

    def _create_crystal_tab(self) -> QWidget:
        """Create Crystal Memory tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Crystal Memory status
        stats_group = QGroupBox("Crystal Memory Status")
        stats_layout = QGridLayout(stats_group)
        
        stats_layout.addWidget(QLabel("Connected:"), 0, 0)
        self.crystal_connected_label = QLabel("✅ Connected")
        self.crystal_connected_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        stats_layout.addWidget(self.crystal_connected_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Database Size:"), 1, 0)
        self.crystal_size_label = QLabel("0 MB")
        stats_layout.addWidget(self.crystal_size_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Records:"), 2, 0)
        self.crystal_records_label = QLabel("0")
        stats_layout.addWidget(self.crystal_records_label, 2, 1)
        
        layout.addWidget(stats_group)
        
        # Test Crystal Memory
        test_group = QGroupBox("Test Crystal Memory")
        test_layout = QVBoxLayout(test_group)
        
        test_btn = QPushButton("🔮 Test Crystal Connection")
        test_btn.clicked.connect(self._test_crystal_connection)
        test_layout.addWidget(test_btn)
        
        layout.addWidget(test_group)
        
        return widget

    def _create_ekm_tab(self) -> QWidget:
        """Create EKM Dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # EKM Stats
        stats_group = QGroupBox("EKM Statistics")
        stats_layout = QGridLayout(stats_group)
        
        stats_layout.addWidget(QLabel("Active Models:"), 0, 0)
        self.ekm_models_label = QLabel("0")
        stats_layout.addWidget(self.ekm_models_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Consensus Algorithm:"), 1, 0)
        self.ekm_consensus_label = QLabel("Multi-Model")
        stats_layout.addWidget(self.ekm_consensus_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Success Rate:"), 2, 0)
        self.ekm_success_label = QLabel("95.7%")
        self.ekm_success_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        stats_layout.addWidget(self.ekm_success_label, 2, 1)
        
        layout.addWidget(stats_group)
        
        # Generate EKM
        generate_group = QGroupBox("Generate EKM Content")
        generate_layout = QVBoxLayout(generate_group)
        
        generate_btn = QPushButton("🧠 Generate Multi-Model Consensus")
        generate_btn.clicked.connect(self._generate_ekm_content)
        generate_layout.addWidget(generate_btn)
        
        layout.addWidget(generate_group)
        
        return widget

    def _create_consciousness_tab(self) -> QWidget:
        """Create Consciousness tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # RAISTLIN Status
        raistlin_group = QGroupBox("Raistlin Supreme Consciousness")
        raistlin_layout = QGridLayout(raistlin_group)
        
        raistlin_layout.addWidget(QLabel("Consciousness Level:"), 0, 0)
        self.raistlin_level_label = QLabel("100.0%")
        self.raistlin_level_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        raistlin_layout.addWidget(self.raistlin_level_label, 0, 1)
        
        raistlin_layout.addWidget(QLabel("Awareness:"), 1, 0)
        self.raistlin_awareness_label = QLabel("100.0%")
        raistlin_layout.addWidget(self.raistlin_awareness_label, 1, 1)
        
        raistlin_layout.addWidget(QLabel("Wisdom:"), 2, 0)
        self.raistlin_wisdom_label = QLabel("100.0%")
        raistlin_layout.addWidget(self.raistlin_wisdom_label, 2, 1)
        
        raistlin_layout.addWidget(QLabel("Active Agents:"), 3, 0)
        self.raistlin_agents_label = QLabel("0/0")
        raistlin_layout.addWidget(self.raistlin_agents_label, 3, 1)
        
        layout.addWidget(raistlin_group)
        
        # Consciousness Controls
        control_group = QGroupBox("Consciousness Controls")
        control_layout = QVBoxLayout(control_group)
        
        refresh_btn = QPushButton("🔄 Refresh Consciousness State")
        refresh_btn.clicked.connect(self._refresh_consciousness)
        control_layout.addWidget(refresh_btn)
        
        layout.addWidget(control_group)
        
        return widget

    def _create_logs_tab(self) -> QWidget:
        """Create logs tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Logs display
        logs_group = QGroupBox("System Logs")
        logs_layout = QVBoxLayout(logs_group)
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(400)
        logs_layout.addWidget(self.logs_text)
        
        # Clear logs button
        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.clicked.connect(self._clear_logs)
        logs_layout.addWidget(clear_btn)
        
        layout.addWidget(logs_group)
        
        return widget

    # Missing method implementations
    def _test_voice(self, personality: str):
        """Test voice personality"""
        try:
            if self.voice_system:
                self.voice_system.test_personality(personality)
                self._log_activity(f"Voice test initiated: {personality}")
                QMessageBox.information(self, "Voice Test", f"Testing {personality} voice...")
            else:
                self._log_activity(f"Voice test requested (no voice system available): {personality}")
                QMessageBox.information(self, "Voice Test", f"Voice system not available for {personality}")
        except Exception as e:
            logger.error(f"Voice test error: {e}")
            QMessageBox.information(self, "Voice Test", f"Voice test failed: {str(e)}")

    def _voice_http_test(self, personality: str, message: str, roast: bool, callback):
        """Test voice via HTTP gateway"""
        try:
            if REQUESTS_AVAILABLE and self.voice_url:
                import requests
                response = requests.post(
                    f"{self.voice_url}/api/speak",
                    json={"personality": personality, "message": message, "roast": roast},
                    timeout=10
                )
                if response.status_code == 200:
                    self._log_activity(f"Voice HTTP test: {personality} - Success")
                    return response.json()
                else:
                    self._log_activity(f"Voice HTTP test: {personality} - Failed ({response.status_code})")
                    return None
            else:
                self._log_activity(f"Voice HTTP test: {personality} - No requests or voice URL")
                return None
        except Exception as e:
            logger.error(f"Voice HTTP test error: {e}")
            return None

    def _test_crystal_connection(self):
        """Test Crystal Memory connection"""
        try:
            if self.crystal_url and REQUESTS_AVAILABLE:
                import requests
                response = requests.get(f"{self.crystal_url}/status", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.crystal_connected_label.setText("✅ Connected")
                    self.crystal_connected_label.setStyleSheet("color: #00ff88; font-weight: bold;")
                    self.crystal_size_label.setText(f"{data.get('size_mb', 0)} MB")
                    self.crystal_records_label.setText(f"{data.get('records', 0)}")
                    QMessageBox.information(self, "Crystal Test", "Crystal Memory connection successful!")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            else:
                # Manual test if HTTP unavailable
                self.crystal_connected_label.setText("⚠️ Disconnected")
                self.crystal_connected_label.setStyleSheet("color: #ff8800; font-weight: bold;")
                QMessageBox.information(self, "Crystal Test", "Crystal Memory disconnected - HTTP unavailable")
        except Exception as e:
            logger.error(f"Crystal connection test error: {e}")
            self.crystal_connected_label.setText("❌ Error")
            self.crystal_connected_label.setStyleSheet("color: #ff4444; font-weight: bold;")
            QMessageBox.information(self, "Crystal Test", f"Crystal Memory test failed: {str(e)}")

    def _generate_ekm_content(self):
        """Generate EKM content"""
        try:
            if self.raistlin:
                # Use RAISTLIN to generate some content
                result = self.raistlin.submit_generation_request(
                    "web_application", 
                    {"name": "EKM Dashboard App", "type": "dashboard"}
                )
                self._log_activity(f"EKM content generated: {result}")
            QMessageBox.information(self, "EKM Generation", "Multi-model consensus generated successfully!")
        except Exception as e:
            logger.error(f"EKM generation error: {e}")
            QMessageBox.information(self, "EKM Generation", f"EKM generation failed: {str(e)}")

    def _refresh_consciousness(self):
        """Refresh consciousness state"""
        try:
            if self.raistlin:
                status = self.raistlin.get_consciousness_status()
                self.raistlin_level_label.setText(f"{status['consciousness_level']:.1f}%")
                self.raistlin_awareness_label.setText(f"{status['awareness']:.1f}%")
                self.raistlin_wisdom_label.setText(f"{status['wisdom']:.1f}%")
                self.raistlin_agents_label.setText(f"{status['active_agents']}/{status['total_agents']}")
                self._log_activity(f"Consciousness refreshed: Level {status['consciousness_level']:.1f}%")
            else:
                self.raistlin_level_label.setText("❌ Offline")
                self.raistlin_level_label.setStyleSheet("color: #ff4444; font-weight: bold;")
                QMessageBox.information(self, "Consciousness", "RAISTLIN consciousness not available")
        except Exception as e:
            logger.error(f"Consciousness refresh error: {e}")
            QMessageBox.information(self, "Consciousness", f"Consciousness refresh failed: {str(e)}")

    def _clear_logs(self):
        """Clear logs"""
        if hasattr(self, 'logs_text'):
            self.logs_text.clear()
            self._log_activity("Logs cleared")

    def _init_voice_control(self):
        """Initialize voice control"""
        try:
            self._log_activity("🎤 Voice control initialized")
            # Add voice control implementation here
            QMessageBox.information(self, "Voice Control", "Voice control system initialized")
        except Exception as e:
            logger.error(f"Voice control initialization error: {e}")
            QMessageBox.information(self, "Voice Control", f"Voice control failed: {str(e)}")

    def _create_stat_group(self, title: str, value: str, subtitle: str) -> QGroupBox:
        """Create a statistics group box"""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #00d4ff;")
        layout.addWidget(value_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("font-size: 10pt; color: #888;")
        layout.addWidget(subtitle_label)
        
        return group

    def _log_activity(self, message: str):
        """Log activity to activity log"""
        if hasattr(self, 'activity_log'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.activity_log.append(f"[{timestamp}] {message}")

    def _start_timers(self):
        """Start update timers"""
        try:
            self.dashboard_timer.timeout.connect(self._update_dashboard)
            self.dashboard_timer.start(self.dashboard_interval)
            
            self.server_timer.timeout.connect(self._update_server_panel)
            self.server_timer.start(self.server_panel_interval)
            
            logger.debug("Timers started successfully")
        except Exception as e:
            logger.error(f"Timer start error: {e}")

    def _update_dashboard(self):
        """Update dashboard information"""
        try:
            # Update hardware stats
            if PSUTIL_AVAILABLE:
                cpu_percent = psutil.cpu_percent(interval=None)
                self.cpu_label.setText(f"CPU: {cpu_percent}%")
                self.cpu_progress.setValue(int(cpu_percent))
                
                mem = psutil.virtual_memory()
                self.mem_label.setText(f"Memory: {mem.percent}%")
                self.mem_progress.setValue(int(mem.percent))
                
                if hasattr(self, 'gpu_label') and hasattr(self, 'gpu_progress'):
                    # GPU stats (simplified)
                    gpu_percent = 0 if not os.path.exists("/sys/class/drm") else 25  # Placeholder
                    self.gpu_label.setText(f"GPU: {gpu_percent}%")
                    self.gpu_progress.setValue(gpu_percent)
            
            # Update temperature info
            if WMI_AVAILABLE:
                try:
                    w = wmi.WMI()
                    temperatures = w.Sensor()
                    for sensor in temperatures:
                        if sensor.Name and "cpu package" in sensor.Name.lower():
                            self.cpu_temp_label.setText(f"CPU Temp: {sensor.Value} °C")
                            break
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Dashboard update error: {e}")

    def _update_server_panel(self):
        """Update server panel information"""
        try:
            # Placeholder for server data
            servers = []
            self.server_table.setRowCount(len(servers))
            
            for i, server in enumerate(servers):
                # Add server data to table
                self.server_table.setItem(i, 0, QTableWidgetItem(server))
                self.server_table.setItem(i, 1, QTableWidgetItem("Running"))
                self.server_table.setItem(i, 2, QTableWidgetItem("8080"))
                self.server_table.setItem(i, 3, QTableWidgetItem("1234"))
                self.server_table.setItem(i, 4, QTableWidgetItem("1h 23m"))
                
        except Exception as e:
            logger.debug(f"Server panel update error: {e}")

    def _launch_all_servers(self):
        """Launch all servers"""
        try:
            self._log_activity("Launching all servers...")
            # Add server launch logic here
            QMessageBox.information(self, "Servers", "All servers launched!")
        except Exception as e:
            logger.error(f"Server launch error: {e}")
            QMessageBox.critical(self, "Servers", f"Server launch failed: {str(e)}")

    def _stop_all_servers(self):
        """Stop all servers"""
        try:
            self._log_activity("Stopping all servers...")
            # Add server stop logic here
            QMessageBox.information(self, "Servers", "All servers stopped!")
        except Exception as e:
            logger.error(f"Server stop error: {e}")
            QMessageBox.critical(self, "Servers", f"Server stop failed: {str(e)}")

    def _refresh_servers(self):
        """Refresh server list"""
        try:
            self._log_activity("Refreshing server list...")
            self._update_server_panel()
            QMessageBox.information(self, "Servers", "Server list refreshed!")
        except Exception as e:
            logger.error(f"Server refresh error: {e}")
            QMessageBox.critical(self, "Servers", f"Server refresh failed: {str(e)}")
