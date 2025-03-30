import {Biome} from "../types/Pokemon.type.ts";

export default function BiomeHeader({biome}: { biome: Biome }) {
    return (
        <div className="inline-flex p-1 w-full min-w-64 min-h-8 bg-blue-500 text-white">
            <div className="m-2">
                <span
                    className="ml-2 mt-auto text-2xl font-bold">{biome.i18n_name}</span>
            </div>
        </div>
    )
}