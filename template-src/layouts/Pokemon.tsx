import PokeCard from "../components/PokeCard.tsx";
import PokeImage from "../components/PokeImage.tsx";
import {useParams} from "react-router";
import {getPokemonByName} from '../api';
import {PokemonForm} from '../types/Pokemon.type';
import {useEffect, useState} from "react";

export default function Pokemon() {
    const {id} = useParams<'id'>() as { id: string };

    const [pokemon, setPokemon] = useState<PokemonForm>()
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getPokemonByName(id);
                setPokemon(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch Pokemon data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [])

    return (
        <>
            <div className="text-center">
                {loading && <p>Loading...</p>}
                {error && <p>{error}</p>}
                {pokemon && (
                    <PokeCard>
                        <div className="inline-flex p-1 w-fit min-w-64 min-h-8 bg-blue-500 text-white">
                            <PokeImage name={pokemon.i18n_name} image={pokemon.image_url}/>
                            <span className="mt-auto">{pokemon.i18n_name}</span>
                            <span className="ml-auto mr-2">{pokemon.pokedex_number}</span>
                        </div>
                    </PokeCard>
                )}
            </div>
        </>
    )
}