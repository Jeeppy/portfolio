from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: str = ""
    tags: str = "[]"
    published: bool = True


class ProjectUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    tags: str | None = None
    published: bool | None = None


class ProjectRead(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    tags: str
    published: bool
    created_at: datetime
    updated_at: datetime
