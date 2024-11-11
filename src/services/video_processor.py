from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
import os
from ..utils.logger import Logger
from ..utils.file_helper import FileHelper
from ..utils.performance_monitor import PerformanceMonitor
from ..utils.validation_helper import ValidationHelper
from tenacity import retry, stop_after_attempt, wait_exponential # type: ignore
from datetime import datetime

class VideoProcessor:
    def __init__(self, output_dir, fps=24, video_codec='libx264', audio_codec='aac'):
        self.logger = Logger(__name__)
        self.file_helper = FileHelper()
        self.performance = PerformanceMonitor()
        self.validator = ValidationHelper()
        self.output_dir = output_dir
        self.fps = fps
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        
    def create_video(self, audio_files, background_image, story_name):
        """
        Create complete video from audio files and background image
        """
        try:
            # Validate inputs
            self.validator.validate_files_exist([background_image, *audio_files])
            
            # Create output directories
            segments_dir = os.path.join(self.output_dir, story_name, "segments")
            final_dir = os.path.join(self.output_dir, story_name, "final")
            self.file_helper.ensure_dir(segments_dir)
            self.file_helper.ensure_dir(final_dir)
            
            # Create individual segments
            with self.performance.measure_time("Creating video segments"):
                video_segments = self._create_segments(
                    audio_files, 
                    background_image, 
                    segments_dir
                )
            
            # Merge segments
            with self.performance.measure_time("Merging video segments"):
                final_video_path = self._merge_segments(
                    video_segments,
                    os.path.join(final_dir, "complete_story.mp4")
                )
            
            # Add metadata
            total_duration = 0
            for audio_file in audio_files:
                audio_clip = AudioFileClip(audio_file)
                total_duration += audio_clip.duration
                audio_clip.close()
            
            metadata = {
                'title': story_name,
                'creation_date': datetime.now().isoformat(),
                'segments': len(audio_files),
                'duration': total_duration
            }
            self.file_helper.save_json(
                os.path.join(final_dir, 'metadata.json'),
                metadata
            )
            
            self.logger.info(f"Video creation completed: {final_video_path}")
            return final_video_path
            
        except Exception as e:
            self.logger.error(f"Error in video processing: {str(e)}")
            raise
            
    def _create_segments(self, audio_files, background_image, output_dir):
        """Create individual video segments for each audio file"""
        video_paths = []
        
        for audio_file in audio_files:
            try:
                # Generate output path
                base_name = os.path.splitext(os.path.basename(audio_file))[0]
                video_path = os.path.join(output_dir, f"{base_name}.mp4")
                
                # Create video segment
                with self.performance.measure_time(f"Processing segment {base_name}"):
                    audio_clip = AudioFileClip(audio_file)
                    image_clip = (ImageClip(background_image)
                                .set_duration(audio_clip.duration)
                                .set_fps(24))
                    
                    # Combine image and audio
                    video = image_clip.set_audio(audio_clip)
                    
                    # Write video file
                    video.write_videofile(
                        video_path,
                        codec=self.video_codec,
                        audio_codec=self.audio_codec,
                        temp_audiofile='temp-audio.m4a',
                        remove_temp=True,
                        threads=4,  # Multithread support
                        bitrate="2000k",  # Video quality
                        logger=self.logger.info  # Progress logging
                    )
                    
                    # Clean up
                    video.close()
                    audio_clip.close()
                    image_clip.close()
                    
                video_paths.append(video_path)
                
            except Exception as e:
                self.logger.error(f"Failed to create segment from {audio_file}: {str(e)}")
                raise
                
        return video_paths
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _merge_segments(self, video_paths, output_path):
        """Merge all video segments into final video with retry logic"""
        clips = []
        try:
            for path in video_paths:
                clip = VideoFileClip(path)
                clips.append(clip)
            
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac'
            )
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to merge video segments: {str(e)}")
            raise
            
        finally:
            # Ensure all clips are closed
            for clip in clips:
                try:
                    clip.close()
                except:
                    pass
            try:
                final_video.close()
            except:
                pass