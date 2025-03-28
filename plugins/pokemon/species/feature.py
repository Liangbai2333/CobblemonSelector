from typing import Optional, Literal, Union, Any, Self

from nonebot import logger
from pydantic import BaseModel, Field, ModelWrapValidatorHandler

from plugins.pokemon.extension.type import TypedModel
from plugins.pokemon.loader.data import feature_map


class Feature(TypedModel):
    type: str = Field(description="特性类型")
    visible: bool = Field(default=False, description="是否可见")
    needsKey: bool = Field(default=True, description="是否需要键")
    keys: list[str] = Field(default=[], description="键")
    isAspect: bool = Field(default=False, description="是否为种类方面")


    @classmethod
    def pre_wrap(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            if data in feature_map:
                return feature_map[data]
            else:
                logger.warning(f"Unknown feature {data}")
                cls.type = "flag"
                cls.keys = [data]
                cls.isAspect = False
                cls.visible = False
                cls.needsKey = False
                return cls
        return None


class IntFeature(Feature):
    class DisplayData(BaseModel):
        name: str = Field(default="", description="显示名称")

    type: Literal["integer"]
    default: int = Field(default=0, description="默认值")
    min: int = Field(default=0, description="最小值")
    max: int = Field(default=100, description="最大值")
    display: Optional[DisplayData] = Field(default=None, description="显示数据")

    isAspect: bool = Field(default=False, description="是否为种类方面")


class ChoiceFeature(Feature):
    type: Literal["choice"]
    default: Optional[str] = Field(default=None, description="默认值")
    isAspect: bool = Field(default=True, description="是否为种类方面")
    aspectFormat: str = Field(default="{{choice}}", description="种类方面格式")

class FlagFeature(Feature):
    type: Literal["flag"]
    default: Optional[Union[Literal["random"], bool]] = Field(default=None, description="默认值")
    isAspect: bool = Field(default=True, description="是否为种类方面")

