from typing import Any

from fastapi import APIRouter

pokemon_router = APIRouter(
    prefix="/api/pokemon",
    tags=["pokemon"],
    responses={404: {"description": "Not found"}},
)


@pokemon_router.get("/{name}")
async def get_pokemon(name: str) -> dict[str, Any]:
    name = name.replace("$", " ")
    from plugins.pokemon import pokemon_container
    pokemon = pokemon_container.get(name)
    if pokemon is None:
        return {"error": "Pokemon not found"}
    return pokemon.model_dump()
