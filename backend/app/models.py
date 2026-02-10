from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    description: str = ""
    tags: str = "[]"  # JSON string
    published: bool = True
    create_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    update_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
