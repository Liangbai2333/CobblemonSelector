import {BiomeSpawnBucket} from "../types/Pokemon.type.ts";

export default function SpawnBiomeBucketTag({bucket}: {bucket: BiomeSpawnBucket}) {
    const bucketStyles = {
        common: 'bg-green-100 text-green-800 border border-green-300',
        uncommon: 'bg-blue-100 text-blue-800 border border-blue-300',
        rare: 'bg-purple-100 text-purple-800 border border-purple-300',
        "ultra-rare": 'bg-red-100 text-red-800 border border-red-300'
    }

    return (
        <div className={`w-22 h-18 justify-center items-center shadow-xs rounded-md space-y-2 ${bucketStyles[bucket.name]}`}>
            <div className="text-xl text-blue-500 font-bold mt-2">{bucket.i18n_name}</div>
            <div className="text-sm text-gray-700 font-medium">{bucket.num_pokemon}只</div>
        </div>
    )
}