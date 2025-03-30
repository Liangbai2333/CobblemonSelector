import useBiome from "../stores/useBiome.ts";
import PokeCard from "../components/PokeCard.tsx";
import BiomeHeader from "../components/BiomeHeader.tsx";

export default function Biome() {
    const {biome, loading, error} = useBiome()

    return (
        <div className="text-center font-mono">
                {loading && <p>Loading...</p>}
                {error && <p>{error}</p>}
                {biome && (
                    <PokeCard>
                        <BiomeHeader biome={biome}/>

                        <div className="grow grid grid-cols-2 auto-rows-max mt-4 pr-3 gap-2">

                        </div>
                    </PokeCard>
                )}
        </div>
    )
}