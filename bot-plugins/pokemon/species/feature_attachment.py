from pydantic import BaseModel, Field

from plugins.pokemon.species.feature import Feature


class FeatureAssignment(BaseModel):
    pokemon: list[str] = Field(default=[], description="Pokémon")
    features: list[Feature] = Field(default=[], description="特性")
