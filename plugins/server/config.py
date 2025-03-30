from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    cs_server_port: int = 8888
