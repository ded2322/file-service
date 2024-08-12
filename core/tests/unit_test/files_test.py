import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from core.config import files_paths
from core.services.file_service import (
    FilesOrm,
    S3Service,
    define_file_path,
    process_file,
    process_upload,
    save_database,
    state_dir,
    upload_s3,
)
from core.utils.validator_file import FileType


@pytest.mark.asyncio
async def test_process_upload(mock_file):
    mock_file_info = {
        "uid": "test-uid-1234",
        "path": Path("/test/path/file.txt"),
        "format": "txt",
    }

    with (
        patch("core.services.file_service.validate_file", return_value=FileType.TEXT),
        patch("core.services.file_service.process_file", return_value=mock_file_info),
        patch("core.services.file_service.save_file_locally", new_callable=AsyncMock),
        patch("core.services.file_service.upload_s3", new_callable=AsyncMock),
        patch("core.services.file_service.save_database", new_callable=AsyncMock),
    ):
        result = await process_upload(mock_file)

        assert isinstance(result, str)
        assert result == "test-uid-1234"


@pytest.mark.asyncio
async def test_process_file(mock_file):
    file_type = FileType.TEXT
    result = await process_file(mock_file, file_type)

    assert isinstance(result, dict)
    assert "uid" in result
    assert "format" in result
    assert "path" in result
    assert result["format"] == "txt"


@pytest.mark.asyncio
async def test_define_file_path():
    file_info = {"format_files": "txt", "uid_files": str(uuid.uuid4())}

    with patch("core.services.file_service.get_file_type", return_value=FileType.TEXT):
        result = await define_file_path(file_info)

        assert isinstance(result, Path)
        assert str(result).endswith(f"{file_info['uid_files']}.txt")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "file_type,expected_path",
    [
        (FileType.TEXT, files_paths.TEXT_UPLOAD_DIR),
        (FileType.IMAGE, files_paths.IMAGE_UPLOAD_DIR),
        (FileType.VIDEO, files_paths.VIDEO_UPLOAD_DIR),
        (FileType.OTHER, files_paths.OTHER_UPLOAD_DIR),
    ],
)
async def test_state_dir(file_type, expected_path):
    result = await state_dir(file_type)
    assert result == expected_path


@pytest.mark.asyncio
async def test_upload_s3():
    file_path = "test/path/file.txt"
    with patch.object(S3Service, "upload_file", new_callable=AsyncMock) as mock_upload:
        await upload_s3(file_path)
        mock_upload.assert_called_once_with(file_path)


@pytest.mark.asyncio
async def test_save_database(mock_file):
    file_info = {"format": "txt", "uid": str(uuid.uuid4())}

    with patch.object(FilesOrm, "insert_data", new_callable=AsyncMock) as mock_insert:
        await save_database(mock_file, file_info)
        mock_insert.assert_called_once_with(
            size_files=mock_file.size,
            format_files=file_info["format"],
            original_name_files=mock_file.filename,
            uid_files=file_info["uid"],
        )
