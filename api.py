"""Legacy ASGI entrypoint for ``uvicorn api:app``. App lives in ``backend.api``."""

from backend.api import app

__all__ = ["app"]
