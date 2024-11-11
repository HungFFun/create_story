import os
from openai import OpenAI
from ..utils.logger import Logger
from ..utils.file_helper import FileHelper
from ..utils.performance_monitor import PerformanceMonitor

class TTSService:
    def __init__(self, api_key, output_dir):
        self.logger = Logger(__name__)
        self.file_helper = FileHelper()
        self.performance = PerformanceMonitor()
        self.client = OpenAI(api_key=api_key)
        self.output_dir = output_dir
        
    def process_files(self, text_files, story_name):
        """
        Convert text files to speech using OpenAI TTS
        """
        try:
            # Create audio output directory
            audio_dir = os.path.join(self.output_dir, story_name, "audio")
            self.file_helper.ensure_dir(audio_dir)
            
            audio_files = []
            
            for text_file in text_files:
                with self.performance.measure_time(f"TTS processing {text_file}"):
                    # Read text content
                    text = self.file_helper.read_text(text_file)
                    
                    # Generate base filename
                    base_name = os.path.splitext(os.path.basename(text_file))[0]
                    audio_path = os.path.join(audio_dir, f"{base_name}.mp3")
                    
                    # Generate speech
                    self._generate_speech(text, audio_path)
                    audio_files.append(audio_path)
                    
            self.logger.info(f"Generated {len(audio_files)} audio files")
            return audio_files
            
        except Exception as e:
            self.logger.error(f"Error in TTS processing: {str(e)}")
            raise
            
    def _generate_speech(self, text, output_path):
        """Generate speech from text using OpenAI API"""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(output_path)
            
            self.logger.debug(f"Generated audio file: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate speech: {str(e)}")
            raise 