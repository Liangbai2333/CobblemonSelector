from fastapi import APIRouter

pokemon_router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"],
    responses={404: {"description": "Not found"}},
)

