"""NOAA Solar video creation utils."""

import logging
import os
import subprocess
from io import BytesIO
from contextlib import ExitStack
import tempfile

from PIL import Image

from .image_utils import list_frames_from_disk

_LOGGER = logging.getLogger(__name__)


def create_video(
    video_format: str,
    image_directory: str,
    video_path: str,
) -> None:
    """Generate a video from the saved frames and write it to video_path."""
    os.makedirs(os.path.dirname(video_path), exist_ok=True)

    if video_format == "MP4":
        _create_mp4_video(image_directory, video_path)
    else:
        _create_gif_video(image_directory, video_path)


def _create_mp4_video(image_directory: str, video_path: str) -> None:
    """Generate a browser-compatible H.264 MP4 from the saved frames using ffmpeg."""
    frames = list_frames_from_disk(image_directory)

    if not frames:
        return

    # Write a temporary file listing all frames in order (ffmpeg concat demuxer)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, dir=os.path.dirname(video_path)
    ) as list_file:
        list_path = list_file.name
        for frame in frames:
            list_file.write(f"file '{frame}'\n")
            list_file.write("duration 0.1\n")  # 10 fps

    with tempfile.NamedTemporaryFile(
        suffix=".mp4", delete=False, dir=os.path.dirname(video_path)
    ) as tmp_file:
        tmp_path = tmp_file.name

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",  # overwrite without asking
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_path,
                "-vf",
                "pad=ceil(iw/2)*2:ceil(ih/2)*2",  # ensure even dimensions for H.264
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-pix_fmt",
                "yuv420p",  # required for broad browser compatibility
                "-movflags",
                "+faststart",  # enable streaming / playback before full download
                tmp_path,
            ],
            check=True,
            capture_output=True,
        )
        os.replace(tmp_path, video_path)
    except subprocess.CalledProcessError as err:
        stderr = err.stderr.decode(errors="replace") if err.stderr else ""
        _LOGGER.error("ffmpeg failed (exit %d): %s", err.returncode, stderr)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)


def _create_gif_video(image_directory: str, video_path: str) -> None:
    """Generate a GIF from the saved frames and write it to video_path."""
    frames = list_frames_from_disk(image_directory)

    if not frames:
        return

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
        gif_bytes = gif_memory.getbuffer().tobytes()

    with tempfile.NamedTemporaryFile(
        suffix=".gif", delete=False, dir=os.path.dirname(video_path)
    ) as tmp_file:
        tmp_path = tmp_file.name
        tmp_file.write(gif_bytes)

    os.replace(tmp_path, video_path)
