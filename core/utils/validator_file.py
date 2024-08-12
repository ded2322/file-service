from enum import Enum

from fastapi import UploadFile


class FileType(Enum):
    TEXT = "txt_files"
    IMAGE = "images_files"
    VIDEO = "media_files"
    OTHER = "other_files"


TEXT_EXTENSIONS = ["txt", "doc", "docx", "pdf", "rtf"]
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp"]
VIDEO_EXTENSIONS = ["mp4", "avi", "mov", "wmv", "flv"]


def get_file_type(file_name: str) -> FileType:
    extensions = file_name.split(".")[-1].lower()
    if extensions in TEXT_EXTENSIONS:
        return FileType.TEXT
    if extensions in IMAGE_EXTENSIONS:
        return FileType.IMAGE
    elif extensions in VIDEO_EXTENSIONS:
        return FileType.VIDEO
    else:
        return FileType.OTHER


def validate_file(file: UploadFile) -> FileType:
    file_type = get_file_type(file.filename)

    return file_type
