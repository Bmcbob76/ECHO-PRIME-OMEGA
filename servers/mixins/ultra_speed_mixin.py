"""
ULTRA SPEED MIXIN
Authority Level 11.0 - Commander Bobby Don McWilliams II

Ultra-fast file operations for ALL ECHO PRIME servers.
Provides atomic operations, caching, batch processing, and optimized I/O.

Usage:
    class MyServer(UltraSpeedMixin):
        def __init__(self):
            super().__init__()
            # Now has ultra_write, ultra_read, ultra_edit, etc.
"""

import os
import re
import shutil
import gzip
from pathlib import Path
from typing import List, Dict, Optional
import logging


class UltraSpeedMixin:
    """Ultra-speed file operations mixin for any server"""

    def __init__(self):
        self._ultra_speed_cache = {}
        self._cache_max_size = 1000
        self.ultra_speed_metrics = {
            'files_written': 0,
            'files_read': 0,
            'files_edited': 0,
            'files_moved': 0,
            'files_deleted': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }

        # Setup logging if not already configured
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(self.__class__.__name__)

    def ultra_write(self, path: str, content: str, encoding: str = 'utf-8') -> Dict:
        """
        Ultra-fast file writing with atomic operations.
        Creates parent directories automatically.

        Args:
            path: Full file path
            content: Content to write
            encoding: File encoding (default: utf-8)

        Returns:
            dict: {'success': bool, 'path': str, 'size': int, 'message': str}
        """
        try:
            file_path = Path(path)

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Atomic write (write to temp, then rename)
            temp_path = file_path.with_suffix(file_path.suffix + '.tmp')

            with open(temp_path, 'w', encoding=encoding) as f:
                f.write(content)

            # Atomic rename
            temp_path.replace(file_path)

            self.ultra_speed_metrics['files_written'] += 1

            return {
                'success': True,
                'path': str(file_path),
                'size': len(content),
                'message': f'File written successfully: {file_path}'
            }

        except Exception as e:
            self.logger.error(f"ultra_write failed: {e}")
            return {
                'success': False,
                'path': path,
                'error': str(e),
                'message': f'Write failed: {e}'
            }

    def ultra_read(self, path: str, encoding: str = 'utf-8', use_cache: bool = True) -> Dict:
        """
        Ultra-fast file reading with caching optimization.

        Args:
            path: Full file path
            encoding: File encoding (default: utf-8)
            use_cache: Use cache if available (default: True)

        Returns:
            dict: {'success': bool, 'content': str, 'size': int, 'cached': bool}
        """
        try:
            file_path = Path(path)

            # Check cache
            if use_cache and str(file_path) in self._ultra_speed_cache:
                self.ultra_speed_metrics['cache_hits'] += 1
                cached_data = self._ultra_speed_cache[str(file_path)]
                return {
                    'success': True,
                    'content': cached_data['content'],
                    'size': cached_data['size'],
                    'cached': True,
                    'message': 'Read from cache'
                }

            self.ultra_speed_metrics['cache_misses'] += 1

            # Read file
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()

            # Update cache
            if use_cache:
                self._update_cache(str(file_path), content)

            self.ultra_speed_metrics['files_read'] += 1

            return {
                'success': True,
                'content': content,
                'size': len(content),
                'cached': False,
                'message': f'File read successfully: {file_path}'
            }

        except Exception as e:
            self.logger.error(f"ultra_read failed: {e}")
            return {
                'success': False,
                'path': path,
                'error': str(e),
                'message': f'Read failed: {e}'
            }

    def ultra_edit(self, path: str, old_text: str, new_text: str, use_regex: bool = False) -> Dict:
        """
        Fast file editing with string replacement. Supports regex patterns.

        Args:
            path: Full file path
            old_text: Text to find and replace
            new_text: Replacement text
            use_regex: Use regex pattern matching (default: False)

        Returns:
            dict: {'success': bool, 'replacements': int, 'message': str}
        """
        try:
            # Read file
            read_result = self.ultra_read(path, use_cache=False)
            if not read_result['success']:
                return read_result

            content = read_result['content']

            # Perform replacement
            if use_regex:
                new_content = re.sub(old_text, new_text, content)
                replacements = len(re.findall(old_text, content))
            else:
                replacements = content.count(old_text)
                new_content = content.replace(old_text, new_text)

            # Write back
            write_result = self.ultra_write(path, new_content)
            if not write_result['success']:
                return write_result

            # Invalidate cache
            if str(path) in self._ultra_speed_cache:
                del self._ultra_speed_cache[str(path)]

            self.ultra_speed_metrics['files_edited'] += 1

            return {
                'success': True,
                'replacements': replacements,
                'message': f'Replaced {replacements} occurrences in {path}'
            }

        except Exception as e:
            self.logger.error(f"ultra_edit failed: {e}")
            return {
                'success': False,
                'path': path,
                'error': str(e),
                'message': f'Edit failed: {e}'
            }

    def ultra_move(self, source: str, destination: str, overwrite: bool = False) -> Dict:
        """
        Move or rename files/directories with conflict resolution.

        Args:
            source: Source path
            destination: Destination path
            overwrite: Overwrite if destination exists (default: False)

        Returns:
            dict: {'success': bool, 'source': str, 'destination': str}
        """
        try:
            src_path = Path(source)
            dest_path = Path(destination)

            if not src_path.exists():
                return {
                    'success': False,
                    'error': 'Source does not exist',
                    'message': f'Source not found: {source}'
                }

            if dest_path.exists() and not overwrite:
                return {
                    'success': False,
                    'error': 'Destination exists',
                    'message': f'Destination already exists: {destination}'
                }

            # Create parent directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Move/rename
            shutil.move(str(src_path), str(dest_path))

            # Invalidate cache
            if str(src_path) in self._ultra_speed_cache:
                del self._ultra_speed_cache[str(src_path)]

            self.ultra_speed_metrics['files_moved'] += 1

            return {
                'success': True,
                'source': source,
                'destination': destination,
                'message': f'Moved {source} → {destination}'
            }

        except Exception as e:
            self.logger.error(f"ultra_move failed: {e}")
            return {
                'success': False,
                'source': source,
                'destination': destination,
                'error': str(e),
                'message': f'Move failed: {e}'
            }

    def ultra_delete(self, path: str, recursive: bool = False) -> Dict:
        """
        Delete files or directories. Use with caution.

        Args:
            path: Path to delete
            recursive: Delete directories recursively (default: False)

        Returns:
            dict: {'success': bool, 'path': str, 'message': str}
        """
        try:
            target_path = Path(path)

            if not target_path.exists():
                return {
                    'success': False,
                    'error': 'Path does not exist',
                    'message': f'Path not found: {path}'
                }

            if target_path.is_dir():
                if not recursive:
                    return {
                        'success': False,
                        'error': 'Directory requires recursive flag',
                        'message': f'Use recursive=True to delete directory: {path}'
                    }
                shutil.rmtree(target_path)
            else:
                target_path.unlink()

            # Invalidate cache
            if str(target_path) in self._ultra_speed_cache:
                del self._ultra_speed_cache[str(target_path)]

            self.ultra_speed_metrics['files_deleted'] += 1

            return {
                'success': True,
                'path': path,
                'message': f'Deleted: {path}'
            }

        except Exception as e:
            self.logger.error(f"ultra_delete failed: {e}")
            return {
                'success': False,
                'path': path,
                'error': str(e),
                'message': f'Delete failed: {e}'
            }

    def ultra_batch_write(self, files: List[Dict[str, str]]) -> Dict:
        """
        Batch write multiple files in one operation for maximum speed.

        Args:
            files: List of {'path': str, 'content': str} dicts

        Returns:
            dict: {'success': bool, 'written': int, 'failed': int, 'results': list}
        """
        results = []
        written = 0
        failed = 0

        for file_spec in files:
            path = file_spec.get('path')
            content = file_spec.get('content', '')

            result = self.ultra_write(path, content)
            results.append(result)

            if result['success']:
                written += 1
            else:
                failed += 1

        return {
            'success': failed == 0,
            'written': written,
            'failed': failed,
            'results': results,
            'message': f'Batch write: {written} succeeded, {failed} failed'
        }

    def ultra_speed_stats(self) -> Dict:
        """
        Get ultra-speed performance statistics and metrics.

        Returns:
            dict: Performance metrics and cache statistics
        """
        cache_size = len(self._ultra_speed_cache)
        total_ops = sum(self.ultra_speed_metrics.values()) - \
                    self.ultra_speed_metrics['cache_hits'] - \
                    self.ultra_speed_metrics['cache_misses']

        cache_hit_rate = 0.0
        if self.ultra_speed_metrics['cache_hits'] + self.ultra_speed_metrics['cache_misses'] > 0:
            cache_hit_rate = self.ultra_speed_metrics['cache_hits'] / \
                           (self.ultra_speed_metrics['cache_hits'] + self.ultra_speed_metrics['cache_misses'])

        return {
            'metrics': self.ultra_speed_metrics.copy(),
            'cache': {
                'size': cache_size,
                'max_size': self._cache_max_size,
                'hit_rate': f'{cache_hit_rate:.2%}'
            },
            'total_operations': total_ops
        }

    def _update_cache(self, path: str, content: str):
        """Update LRU cache with new content"""
        # Simple LRU: remove oldest if cache full
        if len(self._ultra_speed_cache) >= self._cache_max_size:
            # Remove first (oldest) item
            oldest_key = next(iter(self._ultra_speed_cache))
            del self._ultra_speed_cache[oldest_key]

        self._ultra_speed_cache[path] = {
            'content': content,
            'size': len(content)
        }

    def ultra_clear_cache(self):
        """Clear the file cache"""
        self._ultra_speed_cache.clear()
        return {'success': True, 'message': 'Cache cleared'}
