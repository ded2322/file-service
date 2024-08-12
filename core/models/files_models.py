from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Files(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size_files: Mapped[int]
    format_files: Mapped[str] = mapped_column(String(length=10))
    original_name_files: Mapped[str] = mapped_column(String)
    uid_files: Mapped[str] = mapped_column(String)
