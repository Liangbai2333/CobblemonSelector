import {SpawnBucket} from "../types/Pokemon.type.ts";

export default function BucketTag({bucket}: { bucket: SpawnBucket }) {
    const typeStyles = {
        common: 'bg-green-100 text-green-800',
        uncommon: 'bg-blue-100 text-blue-800',
        rare: 'bg-purple-100 text-purple-800',
        "ultra-rare": 'bg-red-100 text-red-800'
    }

    console.log(bucket)

    return (
        <div className={`px-2 py-0.5 rounded-full w-fit h-fit ${typeStyles[bucket.name]}`}>
            {bucket.i18n_name}
        </div>
    )
}