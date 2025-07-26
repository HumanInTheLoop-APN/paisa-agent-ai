# Import and include routers AFTER app creation
from fastapi import FastAPI

from src.apis import artifacts, chat_sessions, health, messages
from src.auth import firebase_auth


def setup_app(app: FastAPI):
    app.include_router(firebase_auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(
        chat_sessions.router, prefix="/chat/sessions", tags=["Chat Sessions"]
    )
    app.include_router(messages.router, prefix="/chat", tags=["Messages"])
    app.include_router(artifacts.router, prefix="/chat", tags=["Artifacts"])
    app.include_router(health.router, tags=["Health"])
