from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    description: str = ""
    tags: str = "[]"
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = ""
    title: str = ""
    bio: str = ""
    avatar_url: str = ""
    resume_url: str = ""
    location: str = ""
    email: str = ""
    github_url: str = ""
    linkedin_url: str = ""
    skills: str = "[]"
    experiences: str = "[]"
    education: str = "[]"


class ContactMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
