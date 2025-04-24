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
const MOON_PHASE_MAPPING = {
    "0": "满月",
    "1": "亏凸月",
    "2": "下弦月",
    "3": "残月",
    "4": "新月",
    "5": "娥眉月",
    "6": "上弦月",
    "7": "盈凸月"
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
                <ConditionContainer.Item name="月相" value={
                    condition.moonPhase.toString().split(",").map((phase) => MOON_PHASE_MAPPING[phase.trim() as keyof typeof MOON_PHASE_MAPPING] || phase).join(", ")
                }/>
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
            {(condition.minHeight != undefined || condition.maxHeight != undefined) && (
                <ConditionContainer.Item name="生成空间高度范围" value={
                    (condition.minHeight && condition.maxHeight)
                        ? `${condition.minHeight} ~ ${condition.maxHeight}`
                        : (condition.minHeight ? `≥${condition.minHeight}` : `≤${condition.maxHeight}`)
                }/>
            )}
            {condition.neededBaseBlocksI18nName && condition.neededBaseBlocks.length > 0 && (
                <ConditionContainer.Item name="生成方块" value={
                    condition.neededBaseBlocksI18nName.join(", ")
                }/>
            )}
            {condition.neededNearbyBlocksI18nName && condition.neededNearbyBlocks.length > 0 && (
                <ConditionContainer.Item name="附近方块" value={
                    condition.neededNearbyBlocksI18nName.join(", ")
                }/>
            )}
            {(condition.minDepth != undefined || condition.maxDepth != undefined) && (
                <ConditionContainer.Item name="生成深度范围" value={
                    (condition.minDepth && condition.maxDepth)
                        ? `${condition.minDepth} ~ ${condition.maxDepth}`
                        : (condition.minDepth ? `≥${condition.minDepth}` : `≤${condition.maxDepth}`)
                }/>
            )}
            {condition.fluidI18nName != undefined && (
                <ConditionContainer.Item name="生成流体" value={
                    condition.fluidI18nName
                }/>
            )}
            {condition.fluidIsSource != undefined && (
                <ConditionContainer.Item name="是否在流体源头" value={
                    condition.fluidIsSource ? "是" : "否"
                }/>
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
    const weightMultiplier = detail?.weightMultiplier

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

                        {weightMultiplier && (
                            <>
                                <div className="h-px mt-3 w-full bg-gray-300"></div>
                                <div>
                                    <div className="px-4 text-md text-blue-500 font-bold mt-2">权重倍率</div>
                                    <div className="mx-auto mt-4 text-sm">
                                        <ConditionContainer>
                                            <div className="text-lg text-green-600 font-bold">倍率: {weightMultiplier.multiplier}x</div>
                                            {weightMultiplier.condition && (
                                                <>
                                                    <div className="text-[1rem] text-gray-700 font-bold py-2">应用条件</div>
                                                    {generateConditionItems(weightMultiplier.condition)}
                                                </>
                                            )}

                                            {weightMultiplier.anticondition && (
                                                <>
                                                    <div className="text-[1rem] text-gray-700 font-bold py-2">排除条件</div>
                                                    {generateConditionItems(weightMultiplier.anticondition)}
                                                </>
                                            )}

                                        </ConditionContainer>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                    <div className="h-px mt-5 w-full bg-gray-300"></div>
                </PokeCard>
            )}
        </div>
    )
}