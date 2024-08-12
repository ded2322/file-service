from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from core.logs.logs import logger_error, logger_response
from core.orm.file_orm import FilesOrm
from core.services.file_service import define_file_path, process_upload

router = APIRouter(prefix="/http", tags=["http upload file"])

@router.get("/load/{uid}")
async def get_video(uid: str):
    """
    Отдает файл с сервера по uid
    """
    file_info = await FilesOrm.found_one_or_none(uid_files=uid)
    if not file_info:
        logger_error.error("Ошибка при нахождении файла")
        raise HTTPException(status_code=404, detail="Файл не найден")

    file_path = await define_file_path(file_info)
    logger_response.info(f"Был выгружен файл под uid {uid}")

    return FileResponse(
        file_path,
        filename=file_info["original_name_files"],
        media_type=f"application/{file_info['format_files']}",
    )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Загружает файл, сохраняет его локально, отправляет в S3 и сохраняет метаданные в БД.

    Args:
        file (UploadFile): Загружаемый файл.

    Returns:
        dict: Словарь с информацией о загруженном файле.

    Raises:
        HTTPException: Если произошла ошибка при обработке файла.
    """
    try:
        result = await process_upload(file)
        logger_response.info(f"Было загружен файл под именем {result}")
        return {"message": f"Файл сохранен под именем {result}"}
    except HTTPException as e:
        logger_error.error(f"Ошибка при загрузке файла: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке файла: {str(e)}"
        )



