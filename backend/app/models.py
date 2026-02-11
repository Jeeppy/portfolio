from datetime import UTC, date, datetime

from sqlmodel import Field, Relationship, SQLModel


class ProjectTagLink(SQLModel, table=True):
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    description: str = ""
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    tags: list["Tag"] = Relationship(
        back_populates="projects", link_model=ProjectTagLink
    )


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

    skills: list["Skill"] = Relationship(back_populates="profile")
    experiences: list["Experience"] = Relationship(back_populates="profile")
    education: list["Education"] = Relationship(back_populates="profile")


class ContactMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    projects: list[Project] = Relationship(
        back_populates="tags", link_model=ProjectTagLink
    )


class Skill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    category: str = ""
    level: int = 0
    profile_id: int | None = Field(default=None, foreign_key="profile.id")

    profile: "Profile | None" = Relationship(back_populates="skills")


class Experience(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    company: str
    position: str
    location: str = ""
    description: str = ""
    start_date: date
    end_date: date | None = None
    profile_id: int | None = Field(default=None, foreign_key="profile.id")

    profile: "Profile | None" = Relationship(back_populates="experiences")


class Education(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    school: str
    degree: str
    location: str = ""
    year: int
    profile_id: int | None = Field(default=None, foreign_key="profile.id")

    profile: "Profile | None" = Relationship(back_populates="education")
