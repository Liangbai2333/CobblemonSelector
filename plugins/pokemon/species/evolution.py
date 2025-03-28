from typing import Optional

from pydantic import BaseModel, Field

from plugins.pokemon.lang import get_lang
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
    requiredContext: Optional[str] = Field(default=None, description="进化条件上下文")


    def get_result_pokemon(self):
        from plugins.pokemon import pokemon_container
        return pokemon_container.get(self.result)

    def get_evo_context_i18n(self) -> str:
        if self.variant == "item_interact":
            (namespace, key) = self.requiredContext.split(":")
            return f"物品{get_lang().get(f"item.{namespace}.{key}")}交互进化"
        if self.variant == "block_click":
            (namespace, key) = self.requiredContext.split(":")
            return f"点击f{get_lang().get(f"block.{namespace}.{key}")}进化"
        if self.variant == "trade":
            return "通讯进化"
        return ""