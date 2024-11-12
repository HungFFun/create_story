import re
from typing import List
from src.config.tts_config import TTSConfig
import os

class TextProcessor:
    def __init__(self, output_path):
        self.output_path = output_path
        self.config = TTSConfig()
        
    def split_into_chunks(self, text: str) -> List[str]:
        """
        Chia văn bản thành các đoạn nhỏ, đảm bảo:
        1. Không cắt giữa câu
        2. Không vượt quá giới hạn ký tự của TTS
        3. Cố gắng chia theo đoạn văn hoặc ý nghĩa
        """
        # Tách theo đoạn văn (dựa vào dấu xuống dòng)
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Bỏ qua đoạn trống
            if not paragraph.strip():
                continue
                
            # Nếu đoạn văn quá dài, cần chia nhỏ hơn
            if len(paragraph) > self.config.MAX_CHARS:
                # Tách thành các câu
                sentences = re.split('([.!?]+)', paragraph)
                
                for i in range(0, len(sentences), 2):
                    sentence = sentences[i]
                    # Thêm dấu câu nếu có
                    if i + 1 < len(sentences):
                        sentence += sentences[i + 1]
                        
                    # Nếu chunk hiện tại + câu mới vẫn trong giới hạn
                    if len(current_chunk) + len(sentence) < self.config.MAX_CHARS:
                        current_chunk += sentence
                    else:
                        # Lưu chunk hiện tại và bắt đầu chunk mới
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
            else:
                # Nếu đoạn văn ngắn, kiểm tra xem có thể thêm vào chunk hiện tại không
                if len(current_chunk) + len(paragraph) + 1 < self.config.MAX_CHARS:
                    current_chunk += ("\n" if current_chunk else "") + paragraph
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph
        
        # Thêm chunk cuối cùng nếu còn
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def save_chunks(self, chunks: List[str], output_dir: str, prefix: str = "part") -> List[str]:
        """
        Lưu các đoạn văn vào file và trả về danh sách đường dẫn
        """
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        file_paths = []
        for i, chunk in enumerate(chunks, 1):
            # Tạo tên file với số thứ tự có padding zeros
            filename = f"{prefix}{str(i).zfill(3)}.txt"
            filepath = f"{output_dir}/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(chunk)
            
            file_paths.append(filepath)
            
        return file_paths

    def process_text(self, text: str, output_dir: str) -> List[str]:
        """
        Xử lý văn bản và trả về danh sách các file đã tạo
        """
        # Chia văn bản thành các đoạn
        chunks = self.split_into_chunks(text)
        
        # Lưu các đoạn vào file
        return self.save_chunks(chunks, output_dir)