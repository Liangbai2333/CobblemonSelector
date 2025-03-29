import PokeCard from "../components/PokeCard.tsx";
import usePokemon from "../stores/usePokemon.ts";
import {useParams} from "react-router";

export default function SpawnDetail() {
    const { index: i = "0" } = useParams<{name: string, index: string}>();
    const {pokemon, loading, error} = usePokemon()

    const index = parseInt(i)

    if (pokemon && (!pokemon.spawn_details || index >= pokemon.spawn_details.length)) {
        return <div>No spawn details found</div>
    }

    return (
        <div className="text-center font-mono">
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {pokemon && (
                <PokeCard>
                    <PokeCard.Header pokemon={pokemon} />


                </PokeCard>
            )}
        </div>
    )
}