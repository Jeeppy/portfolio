from datetime import date, datetime

from pydantic import BaseModel


class TagRead(BaseModel):
    id: int
    name: str


class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: str = ""
    tags: list[str] = []
    published: bool = True


class ProjectUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    published: bool | None = None


class ProjectRead(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    published: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagRead]


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SkillCreate(BaseModel):
    name: str
    category: str = ""
    level: int = 0


class SkillRead(BaseModel):
    id: int
    name: str
    category: str
    level: int


class ExperienceCreate(BaseModel):
    company: str
    position: str
    location: str = ""
    description: str = ""
    start_date: date
    end_date: date | None = None


class ExperienceRead(BaseModel):
    id: int
    company: str
    position: str
    location: str
    description: str
    start_date: date
    end_date: date | None


class EducationCreate(BaseModel):
    school: str
    degree: str
    location: str = ""
    year: int


class EducationRead(BaseModel):
    id: int
    school: str
    degree: str
    location: str
    year: int


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
    skills: list[SkillRead] = []
    experiences: list[ExperienceRead] = []
    education: list[EducationRead] = []


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
    skills: list[SkillCreate] | None = None
    experiences: list[ExperienceCreate] | None = None
    education: list[EducationCreate] | None = None


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
