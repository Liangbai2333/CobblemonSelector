from pydantic import BaseModel, Field

from plugins.pokemon.i18n.translatable import Translatable


class SpawnBucket(BaseModel, Translatable):
    name: str = Field(description="bucket 名称")
    weight: float = Field(description="bucket 权重")

    def get_translation_key(self) -> str:
        return "bucket"


    def get_i18n_name(self):
        return self.translate(self.name)

    def __hash__(self):
        return hash(self.name)



_buckets: dict[str, SpawnBucket] = {}

def _register_bucket(bucket: SpawnBucket) -> SpawnBucket:
    _buckets[bucket.name] = bucket
    return bucket


common = _register_bucket(SpawnBucket(name="common", weight=93.8))
uncommon = _register_bucket(SpawnBucket(name="uncommon", weight=5.0))
rare = _register_bucket(SpawnBucket(name="rare", weight=1.0))
ultra_rare = _register_bucket(SpawnBucket(name="ultra-rare", weight=0.2))

def get_bucket(name: str):
    return _buckets.get(name, common)


def get_buckets():
    return _buckets.values()
