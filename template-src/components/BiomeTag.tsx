import {Biome} from "../types/Pokemon.type.ts";

export default function BiomeTag({biome}: { biome: Biome }) {
    return (
        <div className="w-fit px-1 rounded-sm shadow-sm bg-gray-300/50 text-gray-700 text-md text-center">
            {biome.i18n_name}
        </div>
    )
}