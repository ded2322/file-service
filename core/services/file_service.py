import uuid
from pathlib import Path

from fastapi import UploadFile

from core.config import files_paths
from core.orm.file_orm import FilesOrm
from core.services.s3_service import S3Service
from core.utils.file_utils import save_file_locally
from core.utils.validator_file import FileType, get_file_type, validate_file


async def process_upload(file: UploadFile) -> str:
    file_type = validate_file(file)
    file_info = await process_file(file, file_type)

    await save_file_locally(file, file_info["path"])
    await upload_s3(file_info["path"])
    await save_database(file, file_info)
    return file_info["uid"]


async def process_file(file: UploadFile, file_type: FileType) -> dict:
    uid = str(uuid.uuid4())
    format_file = file.filename.split(".")[-1].lower()

    upload_dir = await state_dir(file_type)

    return {
        "uid": uid,
        "format": format_file,
        "path": upload_dir / f"{uid}.{format_file}",
    }


async def define_file_path(file_info: dict):
    """
    Принимает словарь с ключами
    format_files
    uid_files
    """
    type_file = get_file_type(file_info["format_files"])
    file_path = await state_dir(type_file)
    return file_path / f"{file_info['uid_files']}.{file_info['format_files']}"


async def state_dir(file_type: FileType) -> Path:
    if file_type == file_type.TEXT:
        return files_paths.TEXT_UPLOAD_DIR
    elif file_type == file_type.IMAGE:
        return files_paths.IMAGE_UPLOAD_DIR
    elif file_type == file_type.VIDEO:
        return files_paths.VIDEO_UPLOAD_DIR
    else:
        return files_paths.OTHER_UPLOAD_DIR


async def upload_s3(file_path: str):
    s3_service = S3Service()
    await s3_service.upload_file(file_path)


async def save_database(file: UploadFile, file_info: dict):
    await FilesOrm.insert_data(
        size_files=file.size,
        format_files=file_info["format"],
        original_name_files=file.filename,
        uid_files=file_info["uid"],
    )
