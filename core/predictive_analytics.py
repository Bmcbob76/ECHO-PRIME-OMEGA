"""
Predictive Analytics System
Predicts server failures and issues using pattern analysis

Authority Level: 11.0
Commander Bobby Don McWilliams II
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import deque
import json

logger = logging.getLogger(__name__)

class PredictiveAnalytics:
    """Predict server failures using historical patterns"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.history_window = config.get('prediction_window', 24)  # hours
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
        # Historical data storage
        self.server_history = {}  # server_name -> deque of events
        self.failure_patterns = {}  # pattern_id -> pattern data
        self.predictions = {}  # server_name -> prediction data
        
        # Pattern detection
        self.pattern_signatures = self._initialize_patterns()
        
        logger.info("Predictive Analytics initialized")
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize known failure patterns"""
        patterns = {
            'memory_leak': {
                'signature': 'gradual_increase',
                'metric': 'memory',
                'threshold': 0.8,
                'duration': 60  # minutes
            },
            'cpu_spike': {
                'signature': 'sudden_increase',
                'metric': 'cpu',
                'threshold': 0.9,
                'duration': 5
            },
            'error_cascade': {
                'signature': 'error_frequency',
                'metric': 'errors',
                'threshold': 10,  # errors per minute
                'duration': 10
            },
            'disk_filling': {
                'signature': 'gradual_increase',
                'metric': 'disk',
                'threshold': 0.95,
                'duration': 120
            },
            'connection_exhaustion': {
                'signature': 'connection_buildup',
                'metric': 'connections',
                'threshold': 1000,
                'duration': 15
            }
        }
        return patterns
    
    def record_event(self, server_name: str, event_type: str, data: Dict[str, Any]):
        """Record server event for analysis"""
        if server_name not in self.server_history:
            self.server_history[server_name] = deque(maxlen=1000)
        
        event = {
            'timestamp': datetime.now(),
            'type': event_type,
            'data': data
        }
        
        self.server_history[server_name].append(event)
        
        # Analyze patterns after each event
        self._analyze_patterns(server_name)
    
    def _analyze_patterns(self, server_name: str):
        """Analyze server history for failure patterns"""
        if server_name not in self.server_history:
            return
        
        history = list(self.server_history[server_name])
        if len(history) < 10:  # Need minimum data
            return
        
        # Check each pattern
        for pattern_name, pattern_def in self.pattern_signatures.items():
            confidence = self._check_pattern(history, pattern_def)
            
            if confidence >= self.confidence_threshold:
                self._create_prediction(
                    server_name,
                    pattern_name,
                    confidence,
                    pattern_def
                )
    
    def _check_pattern(self, history: List[Dict], pattern: Dict) -> float:
        """Check if pattern matches historical data"""
        signature = pattern['signature']
        
        if signature == 'gradual_increase':
            return self._check_gradual_increase(history, pattern)
        elif signature == 'sudden_increase':
            return self._check_sudden_increase(history, pattern)
        elif signature == 'error_frequency':
            return self._check_error_frequency(history, pattern)
        elif signature == 'connection_buildup':
            return self._check_connection_buildup(history, pattern)
        
        return 0.0
    
    def _check_gradual_increase(self, history: List[Dict], pattern: Dict) -> float:
        """Detect gradual metric increase"""
        metric = pattern['metric']
        threshold = pattern['threshold']
        duration = pattern['duration']
        
        # Get recent values
        recent = [e for e in history[-20:] 
                 if metric in e.get('data', {})]
        
        if len(recent) < 5:
            return 0.0
        
        values = [e['data'][metric] for e in recent]
        
        # Calculate trend
        if len(values) >= 2:
            first_half = sum(values[:len(values)//2]) / (len(values)//2)
            second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
            
            if second_half > first_half * 1.2 and second_half >= threshold:
                return min(1.0, (second_half / threshold))
        
        return 0.0
    
    def _check_sudden_increase(self, history: List[Dict], pattern: Dict) -> float:
        """Detect sudden metric spike"""
        metric = pattern['metric']
        threshold = pattern['threshold']
        
        recent = [e for e in history[-10:] 
                 if metric in e.get('data', {})]
        
        if len(recent) < 3:
            return 0.0
        
        values = [e['data'][metric] for e in recent]
        latest = values[-1]
        average = sum(values[:-1]) / len(values[:-1])
        
        if latest > average * 2 and latest >= threshold:
            return min(1.0, latest / threshold)
        
        return 0.0
    
    def _check_error_frequency(self, history: List[Dict], pattern: Dict) -> float:
        """Detect increasing error frequency"""
        threshold = pattern['threshold']
        duration = pattern['duration']
        
        # Count errors in last duration minutes
        cutoff = datetime.now() - timedelta(minutes=duration)
        recent_errors = [e for e in history 
                        if e['type'] == 'error' and e['timestamp'] > cutoff]
        
        error_rate = len(recent_errors) / duration  # errors per minute
        
        if error_rate >= threshold:
            return min(1.0, error_rate / threshold)
        
        return 0.0
    
    def _check_connection_buildup(self, history: List[Dict], pattern: Dict) -> float:
        """Detect connection exhaustion"""
        metric = pattern['metric']
        threshold = pattern['threshold']
        
        recent = [e for e in history[-15:] 
                 if metric in e.get('data', {})]
        
        if len(recent) < 3:
            return 0.0
        
        latest_connections = recent[-1]['data'][metric]
        
        if latest_connections >= threshold:
            return min(1.0, latest_connections / threshold)
        
        return 0.0
    
    def _create_prediction(self, server_name: str, pattern_name: str, 
                          confidence: float, pattern: Dict):
        """Create failure prediction"""
        prediction = {
            'server': server_name,
            'pattern': pattern_name,
            'confidence': confidence,
            'detected_at': datetime.now(),
            'estimated_failure': datetime.now() + timedelta(minutes=pattern['duration']),
            'recommended_actions': self._get_recommended_actions(pattern_name),
            'severity': self._calculate_severity(confidence, pattern_name)
        }
        
        self.predictions[server_name] = prediction
        
        logger.warning(
            f"🔮 Prediction: {server_name} may fail in {pattern['duration']} minutes "
            f"(pattern: {pattern_name}, confidence: {confidence:.2%})"
        )
    
    def _get_recommended_actions(self, pattern_name: str) -> List[str]:
        """Get recommended actions for pattern"""
        actions = {
            'memory_leak': [
                'Restart server to clear memory',
                'Investigate memory leak in code',
                'Increase memory allocation temporarily'
            ],
            'cpu_spike': [
                'Check for runaway processes',
                'Load balance traffic to other servers',
                'Scale up CPU resources'
            ],
            'error_cascade': [
                'Enable circuit breaker',
                'Check dependent services',
                'Review recent deployments'
            ],
            'disk_filling': [
                'Clean up old logs',
                'Archive old data',
                'Increase disk space'
            ],
            'connection_exhaustion': [
                'Increase connection pool size',
                'Check for connection leaks',
                'Implement connection timeout'
            ]
        }
        
        return actions.get(pattern_name, ['Monitor closely'])
    
    def _calculate_severity(self, confidence: float, pattern_name: str) -> str:
        """Calculate prediction severity"""
        if confidence >= 0.9:
            return 'critical'
        elif confidence >= 0.8:
            return 'high'
        elif confidence >= 0.7:
            return 'medium'
        else:
            return 'low'
    
    def get_predictions(self, server_name: Optional[str] = None) -> List[Dict]:
        """Get active predictions"""
        if server_name:
            pred = self.predictions.get(server_name)
            return [pred] if pred else []
        
        return list(self.predictions.values())
    
    def get_server_risk_score(self, server_name: str) -> float:
        """Calculate overall risk score for server"""
        if server_name not in self.predictions:
            return 0.0
        
        prediction = self.predictions[server_name]
        return prediction['confidence']
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'active_predictions': len(self.predictions),
            'predictions': [],
            'high_risk_servers': [],
            'statistics': {
                'servers_monitored': len(self.server_history),
                'patterns_detected': len(self.pattern_signatures),
                'prediction_window_hours': self.history_window
            }
        }
        
        for server, pred in self.predictions.items():
            report['predictions'].append({
                'server': server,
                'pattern': pred['pattern'],
                'confidence': pred['confidence'],
                'severity': pred['severity'],
                'time_to_failure': (
                    pred['estimated_failure'] - datetime.now()
                ).total_seconds() / 60,  # minutes
                'actions': pred['recommended_actions']
            })
            
            if pred['severity'] in ['critical', 'high']:
                report['high_risk_servers'].append(server)
        
        return report
    
    def clear_prediction(self, server_name: str):
        """Clear prediction after action taken"""
        if server_name in self.predictions:
            del self.predictions[server_name]
            logger.info(f"✅ Cleared prediction for {server_name}")


if __name__ == "__main__":
    # Test predictive analytics
    config = {
        'prediction_window': 24,
        'confidence_threshold': 0.7
    }
    
    pa = PredictiveAnalytics(config)
    
    # Simulate memory leak
    for i in range(20):
        pa.record_event('test_server', 'metrics', {
            'memory': 0.5 + (i * 0.02),
            'cpu': 0.3
        })
    
    # Generate report
    report = pa.generate_report()
    print(json.dumps(report, indent=2, default=str))
