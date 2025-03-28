from typing import get_type_hints, Literal, Any, Self, ClassVar, Dict, Type, Union

from pydantic import BaseModel, ModelWrapValidatorHandler, model_validator


class TypedModel(BaseModel):

    _field_primitive: ClassVar[str]
    # 类注册表
    __subclass_registry: ClassVar[Dict[str, Type[Self]]] = {}


    def __init_subclass__(cls, **kwargs):
        """自动注册子类"""
        # super可能不是basemodel与typedmodel，此处不应这样用
        # super().__init_subclass__(**kwargs)
        # if 'type' not in kwargs:
        #     cls._field_primitive = "type"
        # else:
        #     cls._field_primitive = kwargs['type']
        cls._field_primitive = kwargs.pop('type', "type")
        super().__init_subclass__(**kwargs)
        type_name = kwargs.pop("type", None)
        if not type_name:
            # 如果没有提供新的type值，但父类有type值，则继承父类的type值
            # 获取第一个非object的父类
            for base in cls.__bases__:
                if base is not object and issubclass(base, TypedModel):
                    if hasattr(base, '_field_primitive') and base._field_primitive:
                        cls._field_primitive = base._field_primitive
                    break

        # 获取子类的字段的Literal值
        type_hints = get_type_hints(cls)
        if cls._field_primitive in type_hints:
            type_hint = type_hints[cls._field_primitive]
            # 检查是否为Literal类型
            if hasattr(type_hint, '__origin__') and type_hint.__origin__ is Literal:
                type_value = type_hint.__args__[0]
                cls.__subclass_registry[type_value] = cls


    @classmethod
    def pre_wrap(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Union[Self, None]:
        return None


    @model_validator(mode="wrap")
    @classmethod
    def __preprocess_data_native(cls, data: Any, handler: ModelWrapValidatorHandler[Self]):
        pre = cls.pre_wrap(data, handler)
        if pre:
            return pre
        return cls._preprocess_data(data, handler)

    @classmethod
    def _preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if "___$$native_processing" in data:
            return handler(data)
        if isinstance(data, dict):
            if cls._field_primitive in data and data[cls._field_primitive] in cls.__subclass_registry:
                return cls.__subclass_registry[data[cls._field_primitive]].model_validate({**data, "___$$native_processing": True})
            else:
                raise ValueError("Invalid data format")

        return handler(data)