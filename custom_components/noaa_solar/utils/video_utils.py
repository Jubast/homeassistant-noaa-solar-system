"""NOAA Solar video creation utils."""

from os.path import join
from datetime import datetime
from io import BytesIO
import subprocess
from contextlib import ExitStack
from PIL import Image
import tempfile

from custom_components.noaa_solar.utils.image_utils import list_frames_from_disk


class Video:
    """Video object."""

    def __init__(self, video_format: str, data: bytes, created: datetime) -> None:
        """Initialize the Video."""
        self.video_format = video_format
        self.data = data
        self.created = created


def create_video(
    video_format: str, image_directory: str, last_image_created: datetime
) -> Video:
    """Generate a Video from the saved frames."""

    video = None
    if video_format == "MP4":
        video = Video(
            video_format, _create_mp4_video(image_directory), last_image_created
        )
    else:
        video = Video(
            video_format, _create_gif_video(image_directory), last_image_created
        )

    return video


def _create_mp4_video(image_directory: str) -> bytes:
    """Generate a MP4 from the saved frames."""

    #########
    ### TODO LEFT HERE, chek with chat4gpt
    ###########
    video_stream = BytesIO()

    # Set the first image to determine the size (if not provided)
    if not width or not height:
        first_image = images[0]
        height, width, _ = first_image.shape

    # Initialize OpenCV VideoWriter to write the video to the in-memory stream
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' for MP4
    video_writer = cv2.VideoWriter(video_stream, fourcc, fps, (width, height))

    # Add each image to the video stream
    for image in images:
        video_writer.write(image)

    # Release the video writer (important for closing the stream)
    video_writer.release()

    # Get the video content from the memory stream
    video_stream.seek(0)  # Move to the start of the stream
    video_data = video_stream.read()  # Read all video data into memory

    return video_data


def _create_gif_video(image_directory: str) -> None:
    """Generate a GIF from the saved frames."""
    frames = list_frames_from_disk(image_directory)

    gif = None
    with ExitStack() as stack:
        imgs = (stack.enter_context(Image.open(f)) for f in frames)
        img = next(imgs)

        gif_memory = BytesIO()
        img.save(
            fp=gif_memory,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=100,
            optimize=True,
            loop=0,
        )
        gif = gif_memory.getbuffer().tobytes()

    return gif
