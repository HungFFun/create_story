from openai import OpenAI
from src.config.tts_config import TTSConfig
from tenacity import retry, stop_after_attempt, wait_exponential
import os

class TTSService:
    def __init__(self, api_key: str, output_dir: str):
        self.client = OpenAI(api_key=api_key)
        self.output_dir = output_dir
        self.config = TTSConfig()

    def split_text(self, text: str) -> list[str]:
        """Split text into chunks that are small enough for the API"""
        chunks = []
        current_chunk = ""
        
        # Split by sentences (roughly)
        sentences = text.split('.')
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < self.config.MAX_CHARS:
                current_chunk += sentence + '.'
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + '.'
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    @retry(
        stop=stop_after_attempt(TTSConfig.MAX_RETRIES),
        wait=wait_exponential(
            multiplier=TTSConfig.RETRY_MULTIPLIER,
            min=TTSConfig.RETRY_MIN_WAIT,
            max=TTSConfig.RETRY_MAX_WAIT
        )
    )
    def generate_audio(self, text_file: str, output_file: str) -> None:
        """
        Generates audio from text file and saves it to the output file
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Read the text file
        with open(text_file, 'r') as f:
            text = f.read()
        
        # Split text into chunks
        chunks = self.split_text(text)
        
        # Generate audio for each chunk
        temp_files = []
        for i, chunk in enumerate(chunks):
            temp_file = f"{output_file}.part{i}.{self.config.AUDIO_FORMAT}"
            response = self.client.audio.speech.create(
                model=self.config.MODEL,
                voice=self.config.VOICE,
                input=chunk
            )
            response.stream_to_file(temp_file)
            temp_files.append(temp_file)
        
        # Merge all chunks
        if len(temp_files) == 1:
            # If only one chunk, just rename it
            os.rename(temp_files[0], output_file)
        else:
            # Merge multiple chunks
            self.merge_audio_files(temp_files, output_file)
            
            # Clean up temp files
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except OSError:
                    pass

    def merge_audio_files(self, audio_files: list[str], output_file: str) -> None:
        """
        Merges multiple audio files into one
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Use pydub to merge audio files
        from pydub import AudioSegment
        
        combined = AudioSegment.empty()
        for audio_file in audio_files:
            segment = AudioSegment.from_mp3(audio_file)
            combined += segment
            
        combined.export(output_file, format=self.config.AUDIO_FORMAT)