from typing import Optional

from pydantic import BaseModel, Field

from plugins.pokemon.spawn_pool.condition import SpawnCondition


class WeightMultiplier(BaseModel):
    condition: Optional[SpawnCondition] = Field(default=None, description="权重倍率条件")
    anticondition: Optional[SpawnCondition] = Field(default=None, description="权重倍率条件非")
    multiplier: float = Field(default=1, description="权重倍率")