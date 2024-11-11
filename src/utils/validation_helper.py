import os
from .logger import Logger

class ValidationHelper:
    def __init__(self):
        self.logger = Logger(__name__)
        
    def validate_files_exist(self, file_paths):
        """Check if all files exist"""
        for path in file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
                
    def validate_google_doc_id(self, doc_id):
        """Validate Google Doc ID format"""
        if not doc_id or not isinstance(doc_id, str):
            raise ValueError("Invalid Google Doc ID")
            
    def validate_text_content(self, text):
        """Validate text content"""
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text content")
        if len(text.strip()) == 0:
            raise ValueError("Empty text content")
            
    def validate_project_structure(self, base_dir):
        """Validate project directory structure"""
        required_dirs = ['src', 'assets', 'output', 'logs']
        for dir_name in required_dirs:
            dir_path = os.path.join(base_dir, dir_name)
            if not os.path.isdir(dir_path):
                raise ValueError(f"Required directory missing: {dir_path}")
                
    def validate_output_structure(self, story_dir):
        """Validate output directory structure"""
        required_dirs = ['text', 'audio', 'segments', 'final']
        for dir_name in required_dirs:
            dir_path = os.path.join(story_dir, dir_name)
            if not os.path.isdir(dir_path):
                raise ValueError(f"Output directory missing: {dir_path}")
                
    def validate_video_output(self, video_path):
        """Validate video file"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if os.path.getsize(video_path) == 0:
            raise ValueError(f"Video file is empty: {video_path}") 