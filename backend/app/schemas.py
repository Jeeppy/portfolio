from datetime import date, datetime, time

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class TagRead(BaseModel):
    id: int
    name: str


class ProjectCategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)


class ProjectCategoryRead(BaseModel):
    id: int
    name: str
    slug: str


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    tags: list[str] = []
    published: bool = True
    demo_url: str | None = Field(default=None, max_length=500)
    repository_url: str | None = Field(default=None, max_length=500)
    category_id: int | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    slug: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    tags: list[str] | None = None
    published: bool | None = None
    demo_url: str | None = Field(default=None, max_length=500)
    repository_url: str | None = Field(default=None, max_length=500)
    category_id: int | None = None


class ProjectRead(BaseModel):
    id: int
    title: str
    slug: str
    description: str | None
    published: bool
    demo_url: str | None
    repository_url: str | None
    tags: list[TagRead]
    category: ProjectCategoryRead | None
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    level: int = Field(default=0, ge=0, le=10)


class SkillRead(BaseModel):
    id: int
    name: str
    category: str | None
    level: int


class ExperienceCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    start_date: date
    end_date: date | None = None


class ExperienceRead(BaseModel):
    id: int
    company: str
    position: str
    location: str | None
    description: str | None
    start_date: date
    end_date: date | None


class EducationCreate(BaseModel):
    school: str = Field(min_length=1, max_length=200)
    degree: str = Field(min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=200)
    year: int
    is_alternance: bool = False
    experience_id: int | None = None

    @model_validator(mode="after")
    def check_alternance_consistency(self) -> "EducationCreate":
        """Ensure experience_id is only set when is_alternance is True."""
        if self.experience_id is not None and not self.is_alternance:
            raise ValueError("experience_id required is_alternance=True")
        return self


class EducationRead(BaseModel):
    id: int
    school: str
    degree: str
    location: str | None
    year: int
    is_alternance: bool
    experience_id: int | None
    experience: ExperienceRead | None


class SocialLinkCreate(BaseModel):
    platform: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=500)
    display_order: int = Field(default=0)


class SocialLinkRead(BaseModel):
    id: int
    platform: str
    url: str
    display_order: int


class ProfileRead(BaseModel):
    id: int
    full_name: str | None
    title: str | None
    bio: str | None
    avatar_filename: str | None
    resume_filename: str | None
    location: str | None
    email: str | None
    skills: list[SkillRead] = []
    experiences: list[ExperienceRead] = []
    education: list[EducationRead] = []
    social_links: list[SocialLinkRead] = []


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=5000)
    location: str | None = Field(default=None, max_length=200)
    email: EmailStr | None = None
    skills: list[SkillCreate] | None = None
    experiences: list[ExperienceCreate] | None = None
    education: list[EducationCreate] | None = None
    social_links: list[SocialLinkCreate] | None = None


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


class AvailabilitySlotCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    is_active: bool = True


class AvailabilitySlotRead(BaseModel):
    id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool


class AppointmentCreate(BaseModel):
    visitor_name: str = Field(min_length=1, max_length=100)
    visitor_email: EmailStr
    subject: str | None = Field(default=None, max_length=200)
    message: str | None = Field(default=None, max_length=2000)
    appointment_date: date
    start_time: time
    end_time: time


class AppointmentRead(BaseModel):
    id: int
    visitor_name: str
    visitor_email: str
    subject: str | None
    message: str | None
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    created_at: datetime


class AppointmentStatusUpdate(BaseModel):
    status: str
