"""Content type utils for image platform."""


def get_content_type(video_format: str) -> str:
    """Returns content type for video format."""
    if video_format == "MP4":
        return "video/mp4"

    return "image/gif"
