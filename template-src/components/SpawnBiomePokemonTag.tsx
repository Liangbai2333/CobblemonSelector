import {BiomeSpawnDetail} from "../types/Pokemon.type.ts";
import BucketTag from "./BucketTag.tsx";

/*
一晚上想怎么定位想了一坨出来，谢谢，等待重构，等我html学成归来！
 */
export default function SpawnBiomePokemonTag({detail}: { detail: BiomeSpawnDetail }) {
    return (
        <div
            className={`h-18 shadow-md items-center rounded-md border border-sky-100 bg-blue-50/50`}>
            <div className="relative flex flex-col gap-y-1 h-full w-full">
                <div className="text-lg text-blue-500 font-bold mt-2">
                    <img className="h-8 w-8 mr-2 inline rounded-full" src={detail.imageUrl} alt={detail.target} onError={(e) => {e.currentTarget.src="/images/none.png"}}/>
                    <span>{detail.target}</span>
                </div>
                {/*本来想借助between定位，结果..absolute！*/}
                <div className="flex justify-between h-full mx-2">
                    <div className="w-5/6 mt-auto mb-1">
                        <div className="justify-self-start text-sm">
                            <span>概率: {(detail.percentage * 100).toFixed(2)}%{' '}</span>
                            <span>权重: {detail.weight.toFixed(2)}{' '}</span>
                            <span>等级: {detail.levelRange}</span>
                        </div>
                    </div>
                    <div className="absolute right-2 bottom-3/10">
                        <BucketTag bucket={detail.bucket} />
                    </div>
                </div>
            </div>
        </div>

    )
}