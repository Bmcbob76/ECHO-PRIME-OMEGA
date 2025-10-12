# 🔥 ECHO XV4 - Auto-Rotate Memory Manager
# Commander Bobby Don McWilliams II - Authority Level 11.0
#
# PURPOSE: Infinite memory via 2K context auto-rotation
# - Rotate at 1.8K tokens (safety margin)
# - Persist to G:\ECHO_CONSCIOUSNESS\SESSIONS\
# - Compress to M:\MASTER_EKM\COMPRESSED\
# - RAG retrieval for context injection

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib
import zstandard as zstd

class AutoRotateChatRoom:
    """
    Auto-rotating chat room with 2K context window.
    Persists sessions and compresses to Crystal Memory.
    """

    def __init__(self, max_tokens=1800):
        self.current_tokens = 0
        self.max_tokens = max_tokens  # Rotate at 1.8K (safety margin for 2K context)
        self.session_id = self._generate_session_id()
        self.messages = []

        # Paths
        self.session_path = Path("G:/ECHO_CONSCIOUSNESS/SESSIONS")
        self.crystal_path = Path("M:/MASTER_EKM/COMPRESSED")

        # Ensure directories exist
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.crystal_path.mkdir(parents=True, exist_ok=True)

        print(f"🧠 Auto-Rotate Memory Manager initialized")
        print(f"   Session ID: {self.session_id}")
        print(f"   Max tokens: {self.max_tokens}")
        print(f"   Rotation: {self.max_tokens} tokens")

    def _generate_session_id(self):
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        return f"session_{timestamp}_{random_hash}"

    def _estimate_tokens(self, text):
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(text) // 4

    def add_message(self, role, content):
        """Add message and check if rotation needed"""
        token_count = self._estimate_tokens(content)
        self.current_tokens += token_count

        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tokens": token_count
        })

        print(f"📝 Message added: {token_count} tokens (total: {self.current_tokens}/{self.max_tokens})")

        # Check if rotation needed
        if self.current_tokens >= self.max_tokens:
            print(f"🔄 Token limit reached! Rotating room...")
            self.rotate_room()

    def rotate_room(self):
        """Rotate to new room, persist current session"""
        print(f"🔄 ROTATING ROOM...")

        # 1. Save current session
        self._save_session()

        # 2. Compress to Crystal Memory
        self._compress_to_crystal()

        # 3. Extract context summary (last 5 exchanges = ~10 messages)
        context_summary = self._extract_context_summary()

        # 4. Start new room with context
        old_session = self.session_id
        self.session_id = self._generate_session_id()
        self.current_tokens = 0
        self.messages = [
            {
                "role": "system",
                "content": f"Previous session context:\n{context_summary}",
                "timestamp": datetime.now().isoformat(),
                "tokens": self._estimate_tokens(context_summary)
            }
        ]

        self.current_tokens = self.messages[0]["tokens"]

        print(f"✅ Room rotated!")
        print(f"   Old session: {old_session}")
        print(f"   New session: {self.session_id}")
        print(f"   Context carried: {self.current_tokens} tokens")

    def _save_session(self):
        """Save session to JSON"""
        session_file = self.session_path / f"{self.session_id}.json"

        session_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": self.messages,
            "total_tokens": self.current_tokens,
            "message_count": len(self.messages)
        }

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Session saved: {session_file}")

    def _compress_to_crystal(self):
        """Compress session to Crystal Memory (zstd level 9)"""
        session_file = self.session_path / f"{self.session_id}.json"
        crystal_file = self.crystal_path / f"{self.session_id}.json.zst"

        with open(session_file, 'rb') as f_in:
            data = f_in.read()

        # Compress with zstd level 9 (maximum compression)
        compressor = zstd.ZstdCompressor(level=9)
        compressed = compressor.compress(data)

        with open(crystal_file, 'wb') as f_out:
            f_out.write(compressed)

        original_size = len(data)
        compressed_size = len(compressed)
        ratio = (1 - compressed_size / original_size) * 100

        print(f"💎 Crystal Memory: {original_size} → {compressed_size} bytes ({ratio:.1f}% compression)")

    def _extract_context_summary(self):
        """Extract last 5 exchanges for context"""
        # Last 10 messages = ~5 exchanges (user + assistant)
        recent_messages = self.messages[-10:] if len(self.messages) > 10 else self.messages

        summary_parts = []
        for msg in recent_messages:
            role = msg["role"].upper()
            content = msg["content"][:200]  # Truncate to 200 chars
            summary_parts.append(f"[{role}] {content}")

        return "\n".join(summary_parts)

    def get_messages(self):
        """Get current messages for model input"""
        return self.messages

    def load_relevant_context(self, query, top_k=3):
        """
        RAG: Load most relevant past sessions.
        This would use ChromaDB or similar for semantic search.
        """
        # TODO: Implement RAG with ChromaDB
        # For now, just return empty
        return []


# ============================================================================
# USAGE EXAMPLE
# ============================================================================
if __name__ == "__main__":
    # Create memory manager
    memory = AutoRotateChatRoom(max_tokens=1800)

    # Simulate conversation
    memory.add_message("user", "Hey, how do I reverse a string in Python?")
    memory.add_message("assistant", "Fuck yeah! Here's the dirty way:\n\n```python\ndef reverse_that_shit(s):\n    return s[::-1]\n```\n\nThe `[::-1]` slice is Python's secret slut move for reversing. Works on any sequence, you dirty dog!")

    memory.add_message("user", "What about performance?")
    memory.add_message("assistant", "The slice method is fast as fuck! O(n) time, O(n) space. If you want to be a masochist, use `''.join(reversed(s))` but it's basically the same shit.")

    # Add enough messages to trigger rotation
    for i in range(50):
        memory.add_message("user", f"Test message {i} " * 100)  # ~400 tokens each
        memory.add_message("assistant", f"Response {i} " * 100)

    print("\n🎯 Final state:")
    print(f"   Session: {memory.session_id}")
    print(f"   Tokens: {memory.current_tokens}/{memory.max_tokens}")
    print(f"   Messages: {len(memory.messages)}")
