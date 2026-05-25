from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {
        "service": "ShelfTxt API",
        "docs": "/docs",
        "health": "/health",
        "books": "/books",
        "recommend": "/recommend",
    }


@router.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {
        "status": "healthy",
        "service": "ShelfTxt",
    }