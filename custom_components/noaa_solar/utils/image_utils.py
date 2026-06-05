"""NOAA Solar image creation utils."""

import os
import tempfile
from hashlib import sha1
from glob import glob
from os import makedirs, remove
from os.path import join, basename
from datetime import datetime


class FrameRef:
    """Frame (image) reference object."""

    def __init__(self, file_name: str, file_datetime: datetime, saved: bool) -> None:
        """Initialize the frame ref."""
        self.file_name = file_name
        self.file_datetime = file_datetime
        self.saved = saved


def list_frames_from_disk(image_directory: str) -> list[str]:
    """Return sorted (by datetime) images stored on the file system."""
    glob_path = join(image_directory, "*.png")
    # Exclude latest.png — it doesn't follow the hash_datetime naming scheme.
    glob_paths = [p for p in glob(glob_path) if basename(p) != "latest.png"]
    return sorted(glob_paths, key=_get_datetime_from_filename)


def save_frame_to_disk(image: bytes, image_directory: str) -> FrameRef:
    """Save a image to the file system if it doesn't already exist."""

    _ensure_directory_exists(image_directory)
    gif_frame = _save_image_if_not_exists(image_directory, image)

    if gif_frame.saved:
        _update_latest(image_directory, image)
        _remove_excess_images(image_directory)

    return gif_frame


def read_image_bytes_from_disk(path: str) -> bytes:
    """Read image bytes from disk."""
    with open(path, "rb") as file_handle:
        return file_handle.read()


def _save_image_if_not_exists(directory: str, data: bytes) -> FrameRef:
    image_hash = sha1(data).hexdigest()
    glob_path = join(directory, image_hash + "*.png")
    glob_paths = glob(glob_path)

    if glob_paths:
        file_name = glob_paths[0]
        file_datetime = _get_datetime_from_filename(file_name)
        return FrameRef(file_name, file_datetime, False)

    current_datetime = datetime.now()
    image_name = image_hash + "_" + current_datetime.strftime("%Y%m%d%H%M%S") + ".png"

    file_path = join(directory, image_name)
    with open(file_path, "wb") as file:
        file.write(data)

    return FrameRef(image_name, current_datetime, True)


def _ensure_directory_exists(directory: str) -> None:
    makedirs(directory, exist_ok=True)


def _update_latest(image_directory: str, data: bytes) -> None:
    """Atomically overwrite latest.png with the newest frame."""
    latest_path = join(image_directory, "latest.png")
    with tempfile.NamedTemporaryFile(
        dir=image_directory, delete=False, suffix=".tmp"
    ) as tf:
        tf.write(data)
        tmp_path = tf.name
    os.replace(tmp_path, latest_path)


def _get_datetime_from_filename(file_path: str) -> datetime:
    file_name = basename(file_path)
    datetime_string = file_name.split("_")[1].split(".")[0]
    return datetime.strptime(datetime_string, "%Y%m%d%H%M%S")


def _remove_excess_images(directory: str) -> None:
    glob_path = join(directory, "*.png")
    glob_paths = [p for p in glob(glob_path) if basename(p) != "latest.png"]
    sorted_glob_paths = sorted(glob_paths, key=_get_datetime_from_filename)

    max_images = 60
    if len(glob_paths) >= max_images:
        excess_count = len(sorted_glob_paths) - max_images

        for i in range(excess_count):
            remove(sorted_glob_paths[i])
