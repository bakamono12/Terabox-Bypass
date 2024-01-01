import os
from moviepy.editor import VideoFileClip
from config import PATH
import logging

logger = logging.getLogger(__name__)


def convert_video(video_path):
    try:
        # Process the video
        video_clip = VideoFileClip(video_path)
        duration = video_clip.duration
        width = video_clip.w
        height = video_clip.h
        thumbnail_path = PATH + "/" + video_clip.filename.split("/")[-1] + ".jpg"
        video_clip.save_frame(thumbnail_path, t=10)  # save the frame at 10 seconds
        return thumbnail_path, duration, width, height
    except Exception as e:
        logger.error(f"Error getting thumbnail: {e}")
        return "", "1", "300", "500"

# if __name__ == "__main__":
#     video_path = 'downloads/1234.mp4'
#     thumbnail_file_id,duration,width,height = convert_video(video_path)
#     print(f"Video File ID: {video_file_id}")
#     print(f"Thumbnail File ID: {thumbnail_file_id}")
