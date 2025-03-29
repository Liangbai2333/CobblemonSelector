import PokeCard from "../components/PokeCard.tsx";
import usePokemon from "../stores/usePokemon.ts";
import {useParams} from "react-router";
import BucketTag from "../components/BucketTag.tsx";
import ConditionContainer from "../components/ConditionContainer.tsx";
import {SpawnCondition} from "../types/Pokemon.type.ts";

const CONTEXTS_MAPPING = {
    grounded: '地面',
    seafloor: '海底',
    lavafloor: '岩浆底',
    submerged: '水下',
    surface: '水面',
    fishing: '钓鱼'
}
const TIMES_MAPPING = {
    "day": "白天",
    "night": "黑夜",
    "any": "任何时间",
    "dawn": "黎明",
    "dusk": "黄昏",
    "noon": "中午",
    "midnight": "午夜",
    "morning": "早上",
    "afternoon": "下午",
    "evening": "晚上"
}

function generateConditionItems(condition: SpawnCondition) {
    return (
        <>
            <ConditionContainer.Item
                name="生物群系"
                value=
                    {condition.biomes.length > 0 ? condition.biomes.filter((biome) => biome.i18n_name.match(/[\u4e00-\u9fa5]+/g)).map((biome) => biome.i18n_name).join(", ") : "任意群系"}
                isFirst={true}
            />
            {condition.canSeeSky != undefined && (
                <ConditionContainer.Item name="能否看见天空"
                                         value={condition.canSeeSky ? "能" : "不能"}/>
            )}
            {condition.moonPhase != undefined && (
                <ConditionContainer.Item name="月相" value={condition.moonPhase}/>
            )}
            {(condition.minX != undefined || condition.maxX != undefined) && (
                <ConditionContainer.Item name="X轴范围" value={
                    (condition.minX && condition.maxX)
                        ? `${condition.minX} ~ ${condition.maxX}`
                        : (condition.minX ? `≥${condition.minX}` : `≤${condition.maxX}`)
                }/>
            )}
            {(condition.minY != undefined || condition.maxY != undefined) && (
                <ConditionContainer.Item name="Y轴范围" value={
                    (condition.minY && condition.maxY)
                        ? `${condition.minY} ~ ${condition.maxY}`
                        : (condition.minY ? `≥${condition.minY}` : `≤${condition.maxY}`)
                }/>
            )}
            {(condition.minZ != undefined || condition.maxZ != undefined) && (
                <ConditionContainer.Item name="Z轴范围" value={
                    (condition.minZ && condition.maxZ)
                        ? `${condition.minZ} ~ ${condition.maxZ}`
                        : (condition.minZ ? `≥${condition.minZ}` : `≤${condition.maxZ}`)
                }/>
            )}
            {condition.isRaining != undefined && (
                <ConditionContainer.Item name="是否下雨"
                                         value={condition.isRaining ? "是" : "否"}/>
            )}
            {condition.isThundering != undefined && (
                <ConditionContainer.Item name="是否雷雨"
                                         value={condition.isThundering ? "是" : "否"}/>
            )}
            {condition.isSlimeChunk != undefined && (
                <ConditionContainer.Item name="是否在史莱姆区块"
                                         value={condition.isSlimeChunk ? "是" : "否"}/>
            )}
            {(condition.maxLight != undefined || condition.minLight != undefined) && (
                <ConditionContainer.Item name="光照强度范围" value={
                    (condition.minLight && condition.maxLight)
                        ? `${condition.minLight}-${condition.maxLight}`
                        : (condition.minLight ? `${condition.minLight}-15` : `0-${condition.maxLight}`)
                }/>
            )}
            {(condition.minSkyLight != undefined || condition.maxSkyLight != undefined) && (
                <ConditionContainer.Item name="天空光照强度范围" value={
                    (condition.minSkyLight && condition.maxSkyLight)
                        ? `${condition.minSkyLight}-${condition.maxSkyLight}`
                        : (condition.minSkyLight ? `${condition.minSkyLight}-15` : `0-${condition.maxSkyLight}`)
                }/>
            )}
            {condition.timeRange != undefined && (
                <ConditionContainer.Item name="时间范围"
                                         value={condition.timeRange.split(",").map((time) => TIMES_MAPPING[time.trim() as keyof typeof TIMES_MAPPING] || time).join(", ")}/>
            )}
        </>
    )
}

// 累，之后再解耦
export default function SpawnDetail() {
    const {index: i = "0"} = useParams<{ name: string, index: string }>();
    const {pokemon, loading, error} = usePokemon()

    const index = parseInt(i)

    if (pokemon && (!pokemon.spawn_details || index >= pokemon.spawn_details.length)) {
        return <div>No spawn details found</div>
    }

    const detail = pokemon?.spawn_details?.[index];
    const condition = detail?.condition
    const anticondition = detail?.anticondition

    return (
        <div className="text-center font-mono">
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {pokemon && detail && (
                <PokeCard>
                    <PokeCard.Header pokemon={pokemon}/>

                    <div className="grow w-full self-start justify-self-start mt-5 grid grid-cols-2 gap-y-4 text-sm">
                        <div className="px-4 text-left">
                            <span className="text-gray-500 text-xs">生成上下文</span>
                            <div className="px-1 text-gray-700 font-bold">
                                {CONTEXTS_MAPPING[detail.context]}
                            </div>
                        </div>
                        <div className="px-4 text-left">
                            <span className="text-gray-500 text-xs">稀有度</span>
                            <BucketTag bucket={detail.bucket}/>
                        </div>
                        <div className="px-4 text-left">
                            <span className="text-gray-500 text-xs">等级</span>
                            <div className="px-1 text-gray-700 font-bold">
                                {detail.level}
                            </div>
                        </div>
                        <div className="px-4 text-left">
                            <span className="text-gray-500 text-xs">权重</span>
                            <div className="px-1 text-gray-700 font-bold">
                                {detail.weight}
                            </div>
                        </div>
                        <div className="px-4 text-left">
                            <span className="text-gray-500 text-xs">预设</span>
                            <div className="px-1 text-gray-700 font-bold">
                                {detail.presets.map((preset) => preset.i18n_name).join(", ")}
                            </div>
                        </div>
                    </div>
                    <div className="h-px mt-3 w-full bg-gray-300"></div>

                    <div className="w-full text-left">
                        {condition && (
                            <>
                                <div>
                                    <div className="px-4 text-md text-blue-500 font-bold mt-2">生成条件</div>
                                    <div className="mx-auto mt-4 text-sm">
                                        <ConditionContainer>
                                            {generateConditionItems(condition)}
                                        </ConditionContainer>
                                    </div>
                                </div>
                            </>
                        )}

                        {anticondition && (
                            <>
                                <div className="h-px mt-3 w-full bg-gray-300"></div>
                                <div>
                                    <div className="px-4 text-md text-blue-500 font-bold mt-2">排除条件</div>
                                    <div className="mx-auto mt-4 text-sm">
                                        <ConditionContainer>
                                            {generateConditionItems(anticondition)}
                                        </ConditionContainer>
                                    </div>
                                </div>
                            </>
                        )}

                        {!condition && !anticondition && (
                            <div className="px-4 text-md text-blue-500 font-bold mt-2 text-center">无生成条件</div>
                        )}
                    </div>
                    <div className="h-px mt-5 w-full bg-gray-300"></div>
                </PokeCard>
            )}
        </div>
    )
}