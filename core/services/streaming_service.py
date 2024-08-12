import aiofiles
from fastapi import UploadFile

from core.services.file_service import process_file, save_database, upload_s3
from core.utils.validator_file import FileType

CHUNK_SIZE = 1024 * 1024  # 1 MB


async def process_stream_upload(file: UploadFile, file_type: FileType):
    file_info = await process_file(file, file_type)

    async with aiofiles.open(file_info["path"], "wb") as out_file:
        while chunk := await file.read(CHUNK_SIZE):
            await out_file.write(chunk)
            yield f"Received chunk: {len(chunk)} bytes"

    await upload_s3(file_info["path"])
    await save_database(file, file_info)

    yield f"File saved with UID: {file_info['uid']}"


async def get_file_size(file_path: str) -> int:
    async with aiofiles.open(file_path, "rb") as f:
        await f.seek(0, 2)
        return await f.tell()
