from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class TagRead(BaseModel):
    id: int
    name: str


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    tags: list[str] = []
    published: bool = True


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    slug: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
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
    email: EmailStr
    password: str = Field(min_length=10, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(default="", max_length=100)
    level: int = Field(default=0, ge=0, le=10)


class SkillRead(BaseModel):
    id: int
    name: str
    category: str
    level: int


class ExperienceCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    location: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=5000)
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
    school: str = Field(min_length=1, max_length=200)
    degree: str = Field(min_length=1, max_length=200)
    location: str = Field(default="", max_length=200)
    year: int


class EducationRead(BaseModel):
    id: int
    school: str
    degree: str
    location: str
    year: int


class ProfileRead(BaseModel):
    id: int
    full_name: str | None
    title: str | None
    bio: str | None
    avatar_url: str | None
    resume_url: str | None
    location: str | None
    email: str | None
    github_url: str | None
    linkedin_url: str | None
    skills: list[SkillRead] = []
    experiences: list[ExperienceRead] = []
    education: list[EducationRead] = []


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=5000)
    avatar_url: str | None = Field(default=None, max_length=500)
    resume_url: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=200)
    email: EmailStr | None = None
    github_url: str | None = Field(default=None, max_length=500)
    linkedin_url: str | None = Field(default=None, max_length=500)
    skills: list[SkillCreate] | None = None
    experiences: list[ExperienceCreate] | None = None
    education: list[EducationCreate] | None = None


class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=5000)

    @field_validator("name", "subject", "message", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class ContactRead(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    read: bool
    created_at: datetime
