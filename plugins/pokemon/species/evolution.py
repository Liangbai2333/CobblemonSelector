from pydantic import BaseModel, Field

from plugins.pokemon.species.evolution_requirement import EvolutionRequirement
from plugins.pokemon.species.move import Move


class Evolution(BaseModel):
    id: str = Field(description="进化ID")
    variant: str = Field(description="进化条件选择器")
    result: str = Field(description="进化结果")
    optional: bool = Field(default=False, description="是否可选")
    consumeHeldItem: bool = Field(default=False, description="是否需要持有道具")
    learnableMoves: list[Move] = Field(default=[], description="可学习招式")

    requirements: list[EvolutionRequirement] = Field(default=[], description="进化条件")
