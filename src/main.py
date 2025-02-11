from fastapi import FastAPI
from httpx import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from src.api.quiz import router
import uvicorn

app = FastAPI()

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if "/docs" not in request.url.path and "/admin" not in request.url.path:
            response = await call_next(request)
            response.headers["x-content-type-options"] = "nosniff"
            response.headers["x-frame-options"] = "deny"
            response.headers["Content-Security-Policy"] = "default-src"
            return response
        else:
            return await call_next(request)

            
app.add_middleware(SecurityMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)