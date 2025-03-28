from pydantic import BaseModel, Field

from plugins.pokemon.spawn_pool.detail import SpawnDetail


class SpawnPool(BaseModel):
    enabled: bool = Field(description="是否启用")
    spawns: list[SpawnDetail] = Field(default=[], description="生成详情")