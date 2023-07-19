"""Solar system gif utils."""

from hashlib import sha1

from contextlib import ExitStack
from glob import glob
from io import BytesIO
from os import makedirs, remove
from os.path import join, basename
from datetime import datetime

from PIL import Image


def save_png_gif_frame(image: bytes, image_directory: str) -> bool:
    """Saves a png image to the file system."""

    _ensure_directory_exists(image_directory)
    saved = _save_image_if_not_exists(image_directory, image)
    if saved:
        _remove_excess_images(image_directory)

    return saved


def create_gif(image_directory: str) -> bytes:
    """Create a gif of images in the directory."""

    glob_path = join(image_directory, "*.png")
    glob_paths = glob(glob_path)
    sorted_glob_paths = sorted(glob_paths, key=_get_datetime_from_filename)

    gif = None
    with ExitStack() as stack:
        imgs = (stack.enter_context(Image.open(f)) for f in sorted_glob_paths)
        img = next(imgs)

        gif_memory = BytesIO()
        img.save(
            fp=gif_memory,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=200,
            optimize=True,
            loop=0,
        )
        gif = gif_memory.getbuffer().tobytes()

    return gif


def save_gif(directory: str, gif_name: str, data: bytes) -> None:
    """Save a gif to the filesystem."""

    _ensure_directory_exists(directory)
    file_name = join(directory, gif_name)
    with open(file_name, "wb") as file:
        file.write(data)


def _save_image_if_not_exists(directory: str, data: bytes) -> bool:
    hash_result = sha1(data).hexdigest()

    glob_path = join(directory, hash_result + "*.png")
    glob_paths = glob(glob_path)

    if glob_paths:
        return False

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    image_name = hash_result + "_" + current_datetime + ".png"

    file_name = join(directory, image_name)
    with open(file_name, "wb") as file:
        file.write(data)

    return True


def _ensure_directory_exists(directory: str) -> None:
    makedirs(directory, exist_ok=True)


def _get_datetime_from_filename(file_path: str):
    file_name = basename(file_path)
    datetime_string = file_name.split("_")[1].split(".")[0]
    return datetime.strptime(datetime_string, "%Y%m%d%H%M%S")


def _remove_excess_images(directory: str) -> None:
    glob_path = join(directory, "*.png")
    glob_paths = glob(glob_path)
    sorted_glob_paths = sorted(glob_paths, key=_get_datetime_from_filename)

    max_images = 30
    if len(glob_paths) >= max_images:
        excess_count = len(sorted_glob_paths) - max_images

        for i in range(excess_count):
            remove(sorted_glob_paths[i])
