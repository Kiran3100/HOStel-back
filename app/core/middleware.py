# app/core/middleware.py
from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from app.core.constants import HEADER_REQUEST_ID


def register_cors_middleware(app: FastAPI, allow_origins: list[str] | None = None) -> None:
    """
    Register CORS middleware.

    Adjust `allow_origins` for production.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_request_id_middleware(app: FastAPI) -> None:
    """
    Simple middleware to inject a request ID into headers for tracing.
    """

    @app.middleware("http")
    async def add_request_id_header(request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get(HEADER_REQUEST_ID) or str(uuid.uuid4())
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers[HEADER_REQUEST_ID] = request_id
        return response


def register_timing_middleware(app: FastAPI) -> None:
    """
    Add X-Process-Time header with request processing time in seconds.
    """

    @app.middleware("http")
    async def add_timing_header(request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response: Response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response


def register_middlewares(app: FastAPI) -> None:
    """
    Convenience function to register all core middlewares.
    """
    register_cors_middleware(app)
    register_request_id_middleware(app)
    register_timing_middleware(app)