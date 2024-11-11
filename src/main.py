import os
from dotenv import load_dotenv
from .services.google_docs_service import GoogleDocsService
from .services.text_processor import TextProcessor
from .services.tts_service import TTSService
from .services.video_processor import VideoProcessor
from .utils.logger import Logger
from .utils.validation_helper import ValidationHelper
from .utils.performance_monitor import PerformanceMonitor
from .utils.file_helper import FileHelper


class StoryVideoGenerator:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        self.logger = Logger(__name__)
        self.validator = ValidationHelper()
        self.performance = PerformanceMonitor()

        # Initialize services
        self.google_docs = GoogleDocsService()
        self.text_processor = TextProcessor("output")
        self.tts_service = TTSService(os.getenv("OPENAI_API_KEY"), "output")
        self.video_processor = VideoProcessor("output")
        self.file_helper = FileHelper()

    def process_story(self, doc_id: str, background_image: str) -> str:
        """
        Process complete story from Google Doc to final video
        """
        try:
            # Validate inputs
            self.validator.validate_google_doc_id(doc_id)
            self.validator.validate_files_exist([background_image])

            with self.performance.measure_time("Complete story processing"):
                # Get document content
                with self.performance.measure_time("Fetching document"):
                    content = self.google_docs.get_document(doc_id)
                    self.validator.validate_text_content(content)

                # Process text into chunks
                with self.performance.measure_time("Processing text"):
                    story_name = self.file_helper.clean_filename(f"story_{doc_id}")
                    text_files = self.text_processor.process_text(content, story_name)

                # Generate audio files
                with self.performance.measure_time("Generating audio"):
                    audio_segments_dir = os.path.join("output", story_name, "segments")
                    audio_final_dir = os.path.join("output", story_name, "final")
                    
                    # Ensure directories exist
                    os.makedirs(audio_segments_dir, exist_ok=True)
                    os.makedirs(audio_final_dir, exist_ok=True)

                    audio_files = []
                    for i, text_file in enumerate(text_files, 1):
                        # Save segment audio to segments folder
                        segment_audio = os.path.join(audio_segments_dir, f"part{i:03d}.mp3")
                        self.tts_service.generate_audio(text_file, segment_audio)
                        audio_files.append(segment_audio)

                    # Merge all audio segments into final audio
                    final_audio = os.path.join(audio_final_dir, "complete_story.mp3")
                    self.tts_service.merge_audio_files(audio_files, final_audio)

                # Create necessary directories
                story_dir = os.path.join("output", f"story_{doc_id}")
                text_dir = os.path.join(story_dir, "text")
                audio_dir = os.path.join(story_dir, "audio")
                segments_dir = os.path.join(story_dir, "segments")
                final_dir = os.path.join(story_dir, "final")
                
                self.file_helper.ensure_dir(text_dir)
                self.file_helper.ensure_dir(audio_dir)
                self.file_helper.ensure_dir(segments_dir)
                self.file_helper.ensure_dir(final_dir)

                # Create final video
                with self.performance.measure_time("Creating video"):
                    final_video = self.video_processor.create_video(
                        [final_audio], background_image, story_name
                    )

                # Validate output
                self.validator.validate_output_structure(
                    os.path.join("output", story_name)
                )
                self.validator.validate_video_output(final_video)

                # Generate performance report
                self.logger.info(self.performance.generate_report())
                
                self.logger.info(f"Video creation completed: {final_video}")
                return final_video

        except Exception as e:
            self.logger.error(f"Failed to process story: {str(e)}")
            raise


# Example usage
# Extract doc_id from the URL
doc_id = "1b94DdmQC0B-wQ4QcZvsxhk9SWpzodzPhNt0CipIRGNQ"

generator = StoryVideoGenerator()
video_path = generator.process_story(
    doc_id=doc_id,
    background_image='assets/background.jpg'
)
print(f"Video generated successfully: {video_path}")
