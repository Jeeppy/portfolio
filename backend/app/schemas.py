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


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileRead(BaseModel):
    id: int
    full_name: str
    title: str
    bio: str
    avatar_url: str
    resume_url: str
    location: str
    email: str
    github_url: str
    linkedin_url: str
    skills: str
    experiences: str
    education: str


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    title: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    resume_url: str | None = None
    location: str | None = None
    email: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    experiences: str | None = None
    education: str | None = None


class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str


class ContactRead(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    read: bool
    created_at: datetime
