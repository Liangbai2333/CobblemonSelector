import PokeCard from "../components/PokeCard.tsx";
import usePokemon from "../stores/usePokemon.ts";
import {useParams} from "react-router";

const CONTEXTS_MAPPING = {
    grounded: '地面',
    seafloor: '海底',
    lavafloor: '岩浆底',
    submerged: '水下',
    surface: '水面',
    fishing: '钓鱼'
}

export default function SpawnDetail() {
    const { index: i = "0" } = useParams<{name: string, index: string}>();
    const {pokemon, loading, error} = usePokemon()

    const index = parseInt(i)

    if (pokemon && (!pokemon.spawn_details || index >= pokemon.spawn_details.length)) {
        return <div>No spawn details found</div>
    }

    const detail = pokemon?.spawn_details?.[index];

    return (
        <div className="text-center font-mono">
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {pokemon && detail && (
                <PokeCard>
                    <PokeCard.Header pokemon={pokemon} />

                    <div className="grow self-start justify-self-start mt-5 grid grid-cols-2">
                        <div className="text-sm ml-4 text-left">
                            <span className="text-gray-500">生成上下文</span>
                            <div className="mt-2 px-1 text-gray-700 font-bold">
                                {CONTEXTS_MAPPING[detail.context]}
                            </div>
                        </div>
                    </div>
                </PokeCard>
            )}
        </div>
    )
}