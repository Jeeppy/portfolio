from fastapi import FastAPI

from app.config import get_settings
from app.routers import projects

settings = get_settings()

app = FastAPI(title="Portfolio API", debug=settings.debug)

app.include_router(projects.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello Portfolio!"}
