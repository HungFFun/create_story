import os
from ..utils.logger import Logger
from ..utils.file_helper import FileHelper

class TextProcessor:
    def __init__(self, output_dir):
        self.logger = Logger(__name__)
        self.file_helper = FileHelper()
        self.output_dir = output_dir
        self.max_chars = 4000
        
    def process_text(self, text, story_name):
        """
        Chia văn bản thành các đoạn nhỏ và lưu vào files
        """
        try:
            # Tạo thư mục output cho story
            text_dir = os.path.join(self.output_dir, story_name, "text")
            self.file_helper.ensure_dir(text_dir)
            
            # Split text thành paragraphs
            paragraphs = self._split_into_paragraphs(text)
            
            # Combine paragraphs into chunks <= 4000 chars
            chunks = self._create_chunks(paragraphs)
            
            # Save chunks to files
            file_paths = []
            for i, chunk in enumerate(chunks, 1):
                file_path = os.path.join(text_dir, f"part{str(i).zfill(3)}.txt")
                self.file_helper.save_text(file_path, chunk)
                file_paths.append(file_path)
                
            self.logger.info(f"Created {len(file_paths)} text chunks")
            return file_paths
            
        except Exception as e:
            self.logger.error(f"Error processing text: {str(e)}")
            raise

    def _split_into_paragraphs(self, text):
        """Split text into paragraphs based on double newlines"""
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    def _create_chunks(self, paragraphs):
        """Combine paragraphs into chunks <= max_chars"""
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para)
            
            if current_length + para_length > self.max_chars:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        # Add final chunk
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks 