import os
from openai import OpenAI
from ..utils.logger import Logger
from ..utils.file_helper import FileHelper
from ..utils.performance_monitor import PerformanceMonitor
from tenacity import retry, stop_after_attempt, wait_exponential

class TTSService:
    def __init__(self, api_key, output_dir, model="tts-1", voice="alloy"):
        self.logger = Logger(__name__)
        self.file_helper = FileHelper()
        self.performance = PerformanceMonitor()
        self.client = OpenAI(api_key=api_key)
        self.output_dir = output_dir
        self.model = model
        self.voice = voice
        
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
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _generate_speech(self, text, output_path):
        """Generate speech from text using OpenAI API with retry logic"""
        try:
            # Validate input text
            if not text or not text.strip():
                raise ValueError("Empty text input")
                
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(output_path)
            
            self.logger.debug(f"Generated audio file: {output_path}")
            
        except Exception as e:
            # Clean up partial file if it exists
            if os.path.exists(output_path):
                os.remove(output_path)
            raise 