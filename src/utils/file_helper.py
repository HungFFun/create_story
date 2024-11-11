import os
import shutil
import json
import re
from .logger import Logger

class FileHelper:
    def __init__(self):
        self.logger = Logger(__name__)
        
    def ensure_dir(self, directory):
        """Create directory if it doesn't exist"""
        if directory:
            # Normalize the path to handle any path separators
            directory = os.path.normpath(directory)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.logger.debug(f"Created directory: {directory}")
            return directory  # Return the normalized path
            
    def clean_filename(self, filename):
        """Remove invalid characters from filename"""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        
    def save_text(self, file_path, content):
        """Save text content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.debug(f"Saved text to: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save text file {file_path}: {str(e)}")
            raise
            
    def read_text(self, file_path):
        """Read text content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to read text file {file_path}: {str(e)}")
            raise
            
    def cleanup_temp_files(self, directory):
        """Remove temporary files and directories"""
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                self.logger.info(f"Cleaned up directory: {directory}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup directory {directory}: {str(e)}")
            raise 
            
    def save_json(self, filepath: str, data: dict):
        """
        Save data to a JSON file
        Args:
            filepath (str): Path to save the JSON file
            data (dict): Data to save
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Failed to save JSON file: {str(e)}")