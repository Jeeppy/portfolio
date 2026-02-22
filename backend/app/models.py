from datetime import UTC, date, datetime

from sqlmodel import Field, Relationship, SQLModel


class ProjectTagLink(SQLModel, table=True):
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


class ProjectCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    slug: str = Field(unique=True, index=True, max_length=100)

    projects: list["Project"] = Relationship(back_populates="category")


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=200)
    slug: str = Field(unique=True, index=True, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    published: bool = True
    demo_url: str | None = Field(default=None, max_length=500)
    repository_url: str | None = Field(default=None, max_length=500)
    category_id: int | None = Field(default=None, foreign_key="projectcategory.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    tags: list["Tag"] = Relationship(
        back_populates="projects", link_model=ProjectTagLink
    )
    category: ProjectCategory | None = Relationship(back_populates="projects")


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = Field(default=None, max_length=200)
    title: str | None = Field(default=None, max_length=200)
    bio: str | None = Field(default=None, max_length=500)
    avatar_filename: str | None = Field(default=None, max_length=500)
    resume_filename: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=200)
    email: str | None = Field(default=None, max_length=200)

    skills: list["Skill"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    experiences: list["Experience"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    education: list["Education"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    social_links: list["SocialLink"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ContactMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=200)
    subject: str = Field(max_length=200)
    message: str = Field(max_length=5000)
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = Field(default=None, index=True)


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)

    projects: list[Project] = Relationship(
        back_populates="tags", link_model=ProjectTagLink
    )


class Skill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    level: int = Field(default=0, ge=0, le=10)
    profile_id: int | None = Field(default=None, foreign_key="profile.id", index=True)

    profile: Profile | None = Relationship(back_populates="skills")


class Experience(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    company: str = Field(max_length=200)
    position: str = Field(max_length=200)
    location: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    start_date: date
    end_date: date | None = None
    profile_id: int | None = Field(default=None, foreign_key="profile.id", index=True)

    profile: Profile | None = Relationship(back_populates="experiences")


class Education(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    school: str = Field(max_length=200)
    degree: str = Field(max_length=200)
    location: str | None = Field(default=None, max_length=200)
    year: int
    profile_id: int | None = Field(default=None, foreign_key="profile.id", index=True)

    profile: Profile | None = Relationship(back_populates="education")


class SocialLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    platform: str = Field(max_length=100)
    url: str = Field(max_length=500)
    display_order: int = Field(default=0)
    profile_id: int | None = Field(default=None, foreign_key="profile.id")

    profile: Profile | None = Relationship(back_populates="social_links")
