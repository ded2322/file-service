import shutil

from fastapi import UploadFile


async def save_file_locally(file: UploadFile, file_path: str):
    with open(file_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
