from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, select

import app.uploads as file_uploads
from app.models import Skill, SocialLink

ADMIN_PROFILE_URL = "/api/admin/profile"
AVATAR_URL = f"{ADMIN_PROFILE_URL}/avatar"
RESUME_URL = f"{ADMIN_PROFILE_URL}/resume"


def test_update_profile(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "full_name": "Jean-Pierre",
            "title": "Développeur",
            "bio": "Hello world",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jean-Pierre"
    assert data["title"] == "Développeur"
    assert data["bio"] == "Hello world"


def test_update_profile_with_skills(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [
                {"name": "Python", "category": "backend", "level": 5},
                {"name": "FastAPI", "category": "backend", "level": 4},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 2
    assert data["skills"][0]["name"] == "Python"
    assert data["skills"][1]["level"] == 4


def test_update_profile_replaces_skills(admin_client: TestClient) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [{"name": "Python", "category": "backend", "level": 5}],
        },
    )

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "skills": [{"name": "Go", "category": "backend", "level": 3}],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 1
    assert data["skills"][0]["name"] == "Go"


def test_update_profile_with_experiences(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "experiences": [
                {
                    "company": "Acme",
                    "position": "Dev",
                    "start_date": "2023-01-01",
                    "end_date": "2024-06-30",
                },
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["experiences"]) == 1
    assert data["experiences"][0]["company"] == "Acme"


def test_update_profile_with_education(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {"school": "MIT", "degree": "CS", "year": 2020},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["education"]) == 1
    assert data["education"][0]["school"] == "MIT"


def test_update_profile_without_auth(client: TestClient) -> None:
    response = client.put(ADMIN_PROFILE_URL, json={"full_name": "Nope"})

    assert response.status_code == 401


def test_update_profile_partial_update(admin_client: TestClient) -> None:
    admin_client.put(ADMIN_PROFILE_URL, json={"full_name": "Jean", "title": "Dev"})

    response = admin_client.put(ADMIN_PROFILE_URL, json={"bio": "new bio"})

    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "new bio"
    assert data["full_name"] == "Jean"


def test_update_profile_invalid_skill_level(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": -1}]},
    )
    assert response.status_code == 422

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": 11}]},
    )
    assert response.status_code == 422


def test_update_profile_cascade_deletes_skills(
    admin_client: TestClient, session: Session
) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={"skills": [{"name": "Python", "category": "backend", "level": 5}]},
    )
    session.expire_all()
    assert len(session.exec(select(Skill)).all()) == 1

    admin_client.put(ADMIN_PROFILE_URL, json={"skills": []})
    session.expire_all()
    assert len(session.exec(select(Skill)).all()) == 0


def test_update_profile_with_social_links(admin_client: TestClient) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "social_links": [
                {
                    "platform": "github",
                    "url": "https://github.com/user",
                    "display_order": 0,
                },
                {
                    "platform": "linkedin",
                    "url": "https://linedin.com/in/user",
                    "display_order": 1,
                },
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["social_links"]) == 2
    assert data["social_links"][0]["platform"] == "github"
    assert data["social_links"][1]["platform"] == "linkedin"


def test_update_profile_replaces_social_links(admin_client: TestClient) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "social_links": [{"platform": "github", "url": "https://github.com/user"}]
        },
    )

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "social_links": [{"platform": "twitter", "url": "https://twitter.com/user"}]
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["social_links"]) == 1
    assert data["social_links"][0]["platform"] == "twitter"


def test_update_profile_cascade_deletes_social_links(
    admin_client: TestClient, session: Session
) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "social_links": [{"platform": "github", "url": "https://github.com/user"}]
        },
    )
    session.expire_all()
    assert len(session.exec(select(SocialLink)).all()) == 1

    admin_client.put(ADMIN_PROFILE_URL, json={"social_links": []})
    session.expire_all()
    assert len(session.exec(select(SocialLink)).all()) == 0


def test_upload_avatar(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.post(
        AVATAR_URL,
        files={"file": ("avatar.jpg", b"fake-image-data", "image/jpeg")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["avatar_filename"] is not None
    assert data["avatar_filename"].endswith(".jpg")


def test_upload_avatar_invalid_type(
    admin_client: TestClient, upload_dirs: None
) -> None:
    response = admin_client.post(
        AVATAR_URL, files={"file": ("resume.pdf", b"fake-pdf-data", "application/pdf")}
    )

    assert response.status_code == 415


def test_upload_avatar_too_large(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.post(
        AVATAR_URL,
        files={
            "file": ("big.jpg", b"x" * (file_uploads.AVATAR_MAX_SIZE + 1), "image/jpeg")
        },
    )

    assert response.status_code == 413


def test_upload_avatar_replaces_old(
    admin_client: TestClient, upload_dirs: None, tmp_path: Path
) -> None:
    first = admin_client.post(
        AVATAR_URL,
        files={"file": ("first.jpg", b"first-image", "image/jpeg")},
    )
    old_filename = first.json()["avatar_filename"]
    old_path = tmp_path / "avatars" / old_filename

    second = admin_client.post(
        AVATAR_URL,
        files={"file": ("second.jpg", b"second-image", "image/jpeg")},
    )

    assert second.status_code == 200
    assert second.json()["avatar_filename"] != old_filename
    assert not old_path.exists()


def test_delete_avatar(admin_client: TestClient, upload_dirs: None) -> None:
    admin_client.post(
        AVATAR_URL,
        files={"file": ("avatar.jpg", b"fake-image-data", "image/jpeg")},
    )

    response = admin_client.delete(AVATAR_URL)

    assert response.status_code == 200
    assert response.json()["avatar_filename"] is None


def test_delete_avatar_no_avatar(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.delete(AVATAR_URL)

    assert response.status_code == 200
    assert response.json()["avatar_filename"] is None


def test_upload_avatar_with_no_auth(client: TestClient, upload_dirs: None) -> None:
    response = client.post(
        AVATAR_URL,
        files={"file": ("avatar.jpg", b"fake-image-data", "image/jpeg")},
    )

    assert response.status_code == 401


def test_upload_resume(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.post(
        RESUME_URL,
        files={"file": ("cv.pdf", b"fake-pdf-data", "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["resume_filename"] is not None
    assert data["resume_filename"].endswith(".pdf")


def test_upload_resume_invalid_type(
    admin_client: TestClient, upload_dirs: None
) -> None:
    response = admin_client.post(
        RESUME_URL,
        files={"file": ("avatar.jpg", b"fake-image-data", "image/jpeg")},
    )

    assert response.status_code == 415


def test_upload_resume_too_large(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.post(
        RESUME_URL,
        files={
            "file": (
                "big.pdf",
                b"x" * (file_uploads.RESUME_MAX_SIZE + 1),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 413


def test_upload_resume_replaces_old(
    admin_client: TestClient, upload_dirs: None, tmp_path: Path
) -> None:
    first = admin_client.post(
        RESUME_URL,
        files={"file": ("first.pdf", b"first-pdf", "application/pdf")},
    )
    old_filename = first.json()["resume_filename"]
    old_path = tmp_path / "resumes" / old_filename

    second = admin_client.post(
        RESUME_URL,
        files={"file": ("second.pdf", b"second-pdf", "application/pdf")},
    )

    assert second.status_code == 200
    assert second.json()["resume_filename"] != old_filename
    assert not old_path.exists()


def test_delete_resume(admin_client: TestClient, upload_dirs: None) -> None:
    admin_client.post(
        RESUME_URL,
        files={"file": ("cv.pdf", b"fake-pdf-data", "application/pdf")},
    )

    response = admin_client.delete(RESUME_URL)

    assert response.status_code == 200
    assert response.json()["resume_filename"] is None


def test_delete_resume_no_resume(admin_client: TestClient, upload_dirs: None) -> None:
    response = admin_client.delete(RESUME_URL)

    assert response.status_code == 200
    assert response.json()["resume_filename"] is None


def test_upload_resume_with_no_auth(client: TestClient, upload_dirs: None) -> None:
    response = client.post(
        RESUME_URL,
        files={"file": ("cv.pdf", b"fake-pdf-data", "application/pdf")},
    )

    assert response.status_code == 401


def test_update_profile_with_alternance_education(admin_client: TestClient) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "experiences": [
                {
                    "company": "Acme",
                    "position": "Dev",
                    "start_date": "2022-09-01",
                    "end_date": "2024-06-30",
                }
            ]
        },
    )
    profile = admin_client.put(ADMIN_PROFILE_URL, json={}).json()
    exp_id = profile["experiences"][0]["id"]

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {
                    "school": "IUT",
                    "degree": "BUT Info",
                    "year": 2024,
                    "is_alternance": True,
                    "experience_id": exp_id,
                }
            ]
        },
    )

    assert response.status_code == 200
    edu = response.json()["education"][0]
    assert edu["is_alternance"] is True
    assert edu["experience_id"] == exp_id
    assert edu["experience"]["company"] == "Acme"


def test_update_profile_education_experience_id_requires_is_alternance(
    admin_client: TestClient,
) -> None:
    admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "experiences": [
                {"company": "Acme", "position": "Dev", "start_date": "2022-09-01"}
            ]
        },
    )
    profile = admin_client.put(ADMIN_PROFILE_URL, json={}).json()
    exp_id = profile["experiences"][0]["id"]

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {
                    "school": "IUT",
                    "degree": "BUT",
                    "year": 2024,
                    "is_alternance": False,
                    "experience_id": exp_id,
                }
            ]
        },
    )

    assert response.status_code == 422


def test_update_profile_education_invalid_experience_id(
    admin_client: TestClient,
) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {
                    "school": "IUT",
                    "degree": "BUT",
                    "year": 2024,
                    "is_alternance": True,
                    "experience_id": 9999,
                }
            ]
        },
    )

    assert response.status_code == 422


def test_update_profile_education_experience_wrong_profile(
    admin_client: TestClient, session: Session
) -> None:
    from app.models import Experience as ExpModel

    orphan = ExpModel(
        company="Other", position="Dev", start_date=date(2022, 1, 1), profile_id=9999
    )
    session.add(orphan)
    session.commit()
    session.refresh(orphan)

    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={
            "education": [
                {
                    "school": "IUT",
                    "degree": "BUT",
                    "year": 2024,
                    "is_alternance": True,
                    "experience_id": orphan.id,
                }
            ]
        },
    )

    assert response.status_code == 422


def test_update_profile_education_default_not_alternance(
    admin_client: TestClient,
) -> None:
    response = admin_client.put(
        ADMIN_PROFILE_URL,
        json={"education": [{"school": "MIT", "degree": "CS", "year": 2020}]},
    )

    assert response.status_code == 200
    edu = response.json()["education"][0]
    assert edu["is_alternance"] is False
    assert edu["experience_id"] is None
    assert edu["experience"] is None
