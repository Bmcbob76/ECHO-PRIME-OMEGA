#!/usr/bin/env python3
"""
PHOENIX VOICE - GUILTY SPARK INTEGRATION
Real-time TTS synthesis using trained Glow-TTS model
Authority Level: 11.0 - COMMANDER AUTHORIZED
"""

import os
import sys
import torch
import json
import numpy as np
from pathlib import Path
from TTS.tts.models.glow_tts import GlowTTS
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.utils.audio import AudioProcessor
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
from datetime import datetime
import wave
import io

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Configure logging
LOG_DIR = Path("E:/ECHO_XV4/logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [PHOENIX-GS343] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'phoenix_guilty_spark.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Model paths - CORRECTED TO ECHO_XV4
MODEL_PATH = "E:/ECHO_XV4/EPCP30/VOICE_CLONING/output/guilty_spark_voice-October-04-2025_05+19AM-78d05db"
CONFIG_PATH = os.path.join(MODEL_PATH, "config.json")
CHECKPOINT_PATH = os.path.join(MODEL_PATH, "best_model.pth")

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Global model storage
model = None
config = None
ap = None
device = None

def load_guilty_spark_model():
    """Load Guilty Spark voice model"""
    global model, config, ap, device
    
    logger.info("="*70)
    logger.info("🔷 PHOENIX VOICE - GUILTY SPARK MODEL INITIALIZATION")
    logger.info("="*70)
    
    try:
        # Set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"💻 Device: {device}")
        if torch.cuda.is_available():
            logger.info(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"📊 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        
        # Load config
        logger.info(f"📂 Loading config: {CONFIG_PATH}")
        config = GlowTTSConfig()
        config.load_json(CONFIG_PATH)
        logger.info(f"🔊 Sample Rate: {config.audio['sample_rate']} Hz")
        
        # Initialize audio processor
        logger.info("🎵 Initializing audio processor...")
        ap = AudioProcessor(**config.audio)
        
        # Initialize model
        logger.info("🧠 Initializing GlowTTS model...")
        model = GlowTTS(config)
        
        # Load checkpoint
        logger.info(f"📥 Loading checkpoint: {CHECKPOINT_PATH}")
        checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
        model.load_state_dict(checkpoint['model'])
        model.to(device)
        model.eval()
        
        param_count = sum(p.numel() for p in model.parameters())
        logger.info(f"✅ MODEL LOADED SUCCESSFULLY")
        logger.info(f"📊 Parameters: {param_count:,}")
        logger.info(f"🎤 Voice: 343 Guilty Spark")
        logger.info("="*70)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ CRITICAL: Model loading failed", exc_info=True)
        return False

def synthesize_speech(text, speed=1.0, noise_scale=0.0):
    """
    Synthesize speech from text using Guilty Spark voice
    
    Args:
        text: Input text to synthesize
        speed: Speech speed multiplier (1.0 = normal)
        noise_scale: Inference noise scale (0.0 = deterministic)
    
    Returns:
        waveform: NumPy array of audio samples
    """
    global model, config, ap, device
    
    try:
        logger.info(f"🎤 Synthesizing: '{text[:50]}...' (speed: {speed})")
        
        # Preprocess text
        text = text.strip()
        if not text:
            raise ValueError("Empty text input")
        
        # Convert text to sequence
        text_inputs = np.array(model.tokenizer.text_to_ids(text), dtype=np.int32)
        text_inputs = torch.from_numpy(text_inputs).unsqueeze(0).to(device)
        
        # Generate speech with inference noise scale
        with torch.no_grad():
            outputs = model.inference(
                text_inputs,
                lengths=torch.tensor([len(text_inputs[0])]).to(device)
            )
        
        # Extract mel spectrogram
        mel = outputs['model_outputs'].cpu().numpy()[0]
        
        # Convert mel to waveform (Griffin-Lim reconstruction)
        waveform = ap.inv_melspectrogram(mel.T)
        
        # Apply speed adjustment
        if speed != 1.0:
            target_length = int(len(waveform) / speed)
            indices = np.linspace(0, len(waveform) - 1, target_length)
            waveform = np.interp(indices, np.arange(len(waveform)), waveform)
        
        # Normalize to prevent clipping
        waveform = waveform / np.max(np.abs(waveform)) * 0.95
        
        duration = len(waveform) / config.audio['sample_rate']
        logger.info(f"✅ Synthesis complete: {len(waveform):,} samples, {duration:.2f}s")
        
        return waveform
        
    except Exception as e:
        logger.error(f"❌ Synthesis error: {str(e)}", exc_info=True)
        raise

def waveform_to_wav_bytes(waveform, sample_rate=22050):
    """Convert waveform numpy array to WAV bytes"""
    # Convert to 16-bit PCM
    waveform_int16 = np.int16(waveform * 32767)
    
    # Create WAV in memory
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(waveform_int16.tobytes())
    
    wav_io.seek(0)
    return wav_io

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    gpu_info = {}
    if torch.cuda.is_available():
        gpu_info = {
            'name': torch.cuda.get_device_name(0),
            'memory_allocated': f"{torch.cuda.memory_allocated(0) / 1e9:.2f} GB",
            'memory_total': f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
        }
    
    return jsonify({
        'status': 'online',
        'service': 'Phoenix Voice - Guilty Spark',
        'model_loaded': model is not None,
        'device': str(device) if device else 'unknown',
        'gpu': gpu_info,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'authority_level': '11.0'
    })

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Synthesize speech from text and return WAV file
    
    JSON Body:
        {
            "text": "Text to synthesize",
            "speed": 1.0 (optional, default: 1.0),
            "noise_scale": 0.0 (optional, default: 0.0)
        }
    
    Returns:
        WAV audio file (audio/wav)
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text parameter'}), 400
        
        text = data['text']
        speed = data.get('speed', 1.0)
        noise_scale = data.get('noise_scale', 0.0)
        
        # Synthesize
        waveform = synthesize_speech(text, speed=speed, noise_scale=noise_scale)
        
        # Convert to WAV
        wav_bytes = waveform_to_wav_bytes(waveform, config.audio['sample_rate'])
        
        return send_file(
            wav_bytes,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'gs343_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        )
        
    except Exception as e:
        logger.error(f"❌ Synthesis request error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize_json', methods=['POST'])
def synthesize_json():
    """
    Synthesize speech and return base64 encoded audio
    
    JSON Body:
        {
            "text": "Text to synthesize",
            "speed": 1.0 (optional),
            "noise_scale": 0.0 (optional)
        }
    
    Returns:
        JSON with base64 audio data
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text parameter'}), 400
        
        text = data['text']
        speed = data.get('speed', 1.0)
        noise_scale = data.get('noise_scale', 0.0)
        
        # Synthesize
        waveform = synthesize_speech(text, speed=speed, noise_scale=noise_scale)
        
        # Convert to WAV bytes
        wav_bytes = waveform_to_wav_bytes(waveform, config.audio['sample_rate'])
        
        # Encode to base64
        import base64
        audio_b64 = base64.b64encode(wav_bytes.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio': audio_b64,
            'sample_rate': config.audio['sample_rate'],
            'duration': len(waveform) / config.audio['sample_rate'],
            'text': text,
            'voice': 'Guilty Spark'
        })
        
    except Exception as e:
        logger.error(f"❌ Synthesis JSON request error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/batch_synthesize', methods=['POST'])
def batch_synthesize():
    """
    Batch synthesize multiple texts
    
    JSON Body:
        {
            "texts": ["Text 1", "Text 2", ...],
            "speed": 1.0 (optional),
            "noise_scale": 0.0 (optional)
        }
    
    Returns:
        JSON with list of base64 encoded audios
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'Missing texts parameter'}), 400
        
        texts = data['texts']
        speed = data.get('speed', 1.0)
        noise_scale = data.get('noise_scale', 0.0)
        
        results = []
        
        for idx, text in enumerate(texts, 1):
            try:
                logger.info(f"🔄 Batch {idx}/{len(texts)}")
                
                # Synthesize
                waveform = synthesize_speech(text, speed=speed, noise_scale=noise_scale)
                
                # Convert to WAV bytes
                wav_bytes = waveform_to_wav_bytes(waveform, config.audio['sample_rate'])
                
                # Encode to base64
                import base64
                audio_b64 = base64.b64encode(wav_bytes.read()).decode('utf-8')
                
                results.append({
                    'text': text,
                    'audio': audio_b64,
                    'duration': len(waveform) / config.audio['sample_rate'],
                    'success': True
                })
                
            except Exception as e:
                logger.error(f"❌ Batch item {idx} failed: {str(e)}")
                results.append({
                    'text': text,
                    'error': str(e),
                    'success': False
                })
        
        success_count = sum(1 for r in results if r['success'])
        
        return jsonify({
            'results': results,
            'sample_rate': config.audio['sample_rate'],
            'total': len(texts),
            'successful': success_count,
            'failed': len(texts) - success_count
        })
        
    except Exception as e:
        logger.error(f"❌ Batch synthesis error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get model information and configuration"""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 503
    
    return jsonify({
        'model_name': 'Guilty Spark Voice (343)',
        'model_type': 'GlowTTS',
        'model_path': MODEL_PATH,
        'checkpoint': CHECKPOINT_PATH,
        'sample_rate': config.audio['sample_rate'],
        'parameters': sum(p.numel() for p in model.parameters()),
        'device': str(device),
        'test_sentences': config.test_sentences,
        'audio_config': {
            'sample_rate': config.audio['sample_rate'],
            'hop_length': config.audio['hop_length'],
            'win_length': config.audio['win_length'],
            'num_mels': config.audio['num_mels']
        }
    })

@app.route('/test_voice', methods=['GET'])
def test_voice():
    """Quick voice test endpoint"""
    try:
        test_text = "I am 343 Guilty Spark. Greetings. I am the monitor of installation zero four."
        waveform = synthesize_speech(test_text)
        wav_bytes = waveform_to_wav_bytes(waveform, config.audio['sample_rate'])
        
        return send_file(
            wav_bytes,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='gs343_test.wav'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MAIN SERVER
# ============================================================================

def main():
    """Main server entry point"""
    logger.info("="*70)
    logger.info("🔷 PHOENIX VOICE - GUILTY SPARK SERVER")
    logger.info("🎖️  AUTHORITY LEVEL: 11.0")
    logger.info("🏠 ROOT: E:\\ECHO_XV4")
    logger.info("="*70)
    
    # Load model
    if not load_guilty_spark_model():
        logger.error("❌ CRITICAL: Failed to load model. Exiting.")
        sys.exit(1)
    
    # Start server
    port = 7343  # 343 Guilty Spark reference
    logger.info(f"\n🚀 Starting Phoenix Voice server on port {port}")
    logger.info(f"📡 Health: http://localhost:{port}/health")
    logger.info(f"🔊 Synthesize: POST http://localhost:{port}/synthesize")
    logger.info(f"🧪 Test: GET http://localhost:{port}/test_voice")
    logger.info(f"📊 Info: GET http://localhost:{port}/model_info")
    logger.info("="*70)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()
