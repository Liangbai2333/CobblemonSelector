import useSpawnBiome from "../stores/useSpawnBiome.ts";
import PokeCard from "../components/PokeCard.tsx";
import BiomeHeader from "../components/BiomeHeader.tsx";
import PokeInfoTag from "../components/PokeInfoTag.tsx";
import BiomeTag from "../components/BiomeTag.tsx";
import SpawnBiomeBucketTag from "../components/SpawnBiomeBucketTag.tsx";
import SpawnBiomePokemonTag from "../components/SpawnBiomePokemonTag.tsx";

export default function Biome() {
    const {spawnBiome, loading, error} = useSpawnBiome()

    return (
        <div className="text-center font-mono">
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {spawnBiome && (
                <PokeCard>
                    <BiomeHeader biome={spawnBiome}/>

                    <div className="grow grid grid-cols-2 auto-rows-max my-4 px-5 gap-x-4">
                        <PokeInfoTag>
                            <span className="w-32 text-gray-700 text-xl">总权重</span>
                            <span className="text-lg">{spawnBiome.total_weight.toFixed(2)}</span>
                        </PokeInfoTag>
                        <PokeInfoTag>
                            <span className="w-32 text-gray-700 text-xl">替换</span>
                            <span className="text-lg">{spawnBiome.replace ? "是" : "否"}</span>
                        </PokeInfoTag>
                    </div>
                    <div className="h-px mt-3 w-full bg-gray-300"></div>
                    <div className="text-xl text-blue-500 font-bold mt-2">代表群系</div>
                    <div
                        // 怎么解决这个把父容器撑开的问题?
                        className="flex flex-wrap mt-2 max-w-96 mx-auto items-center justify-center gap-2">
                        {spawnBiome.sub_biomes
                            .map((biome, index) => {
                                return (
                                    <BiomeTag key={index} biomeName={biome}/>
                                )
                            })
                        }
                    </div>
                    <div className="h-px mt-3 w-full bg-gray-300"></div>
                    <div className="text-xl text-blue-500 font-bold mt-2">稀有度分布</div>
                    <div className="flex mt-2 gap-x-4 px-4 justify-center">
                        {spawnBiome.buckets.map((bucket, index) => {
                            return (
                                <SpawnBiomeBucketTag key={index} bucket={bucket}/>
                            )
                        })}
                    </div>
                    <div className="h-px mt-3 w-full bg-gray-300"></div>
                    <div className="text-xl text-blue-500 font-bold mt-2">生成宝可梦</div>
                    <div className="flex flex-col mt-2 px-4 gap-y-4">
                        {spawnBiome.details.map((detail, index) => {
                            return (
                                <SpawnBiomePokemonTag key={index} detail={detail} />
                            )
                        })}
                    </div>
                    <div className="h-px mt-5 w-full bg-gray-300"></div>
                </PokeCard>
            )}
        </div>
    )
}