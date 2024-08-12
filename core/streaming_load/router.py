from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from core.services.streaming_service import process_stream_upload
from core.utils.validator_file import validate_file

router = APIRouter(prefix="/stream", tags=["streaming download"])


@router.post("/upload")
async def upload_file_stream(file: UploadFile = File(...)):
    try:
        file_type = validate_file(file)
        return StreamingResponse(process_stream_upload(file, file_type))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при потоковой загрузке файла: {str(e)}"
        )
