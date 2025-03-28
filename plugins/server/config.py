from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    server_port: int = 8888
