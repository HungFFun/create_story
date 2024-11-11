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

    def process_story(self, doc_id, background_image):
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
                    audio_files = self.tts_service.process_files(text_files, story_name)

                # Create final video
                with self.performance.measure_time("Creating video"):
                    final_video = self.video_processor.create_video(
                        audio_files, background_image, story_name
                    )

                # Validate output
                self.validator.validate_output_structure(
                    os.path.join("output", story_name)
                )
                self.validator.validate_video_output(final_video)

                # Generate performance report
                self.logger.info(self.performance.generate_report())

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
