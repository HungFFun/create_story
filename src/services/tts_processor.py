from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import hashlib
import os
from functools import lru_cache
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

class TTSProcessor:
    def __init__(self, max_workers=4, cache_dir="cache/tts", batch_size=10):
        self.max_workers = max_workers
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.batch_size = batch_size

    @lru_cache(maxsize=100)
    def get_cache_path(self, text: str) -> str:
        # Tạo unique filename dựa trên content
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{text_hash}.mp3")

    def process_batch(self, texts: List[str]) -> List[str]:
        audio_files = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_text = {executor.submit(self.text_to_speech, text): text 
                            for text in texts}
            
            for future in as_completed(future_to_text):
                try:
                    audio_file = future.result()
                    audio_files.append(audio_file)
                except Exception as e:
                    logger.error(f"Failed to process TTS: {e}")
                    
        return audio_files 

    def optimize_text(self, text: str) -> str:
        # Loại bỏ các ký tự không cần thiết
        text = text.strip()
        # Chuẩn hóa khoảng trắng
        text = ' '.join(text.split())
        # Các tối ưu khác tùy vào yêu cầu
        return text

    def text_to_speech(self, text: str) -> str:
        optimized_text = self.optimize_text(text)
        return self._process_tts(optimized_text)

    def process_texts(self, texts: List[str]) -> List[str]:
        results = []
        # Xử lý theo batch
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_results = self.process_batch(batch)
            results.extend(batch_results)
        return results