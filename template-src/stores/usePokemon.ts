import {useParams} from "react-router";
import {useEffect, useState} from "react";
import {PokemonForm} from "../types/Pokemon.type.ts";
import {getPokemonByName} from "../api";

export default function usePokemon() {
    const {name} = useParams<'name'>() as { name: string };

    const [pokemon, setPokemon] = useState<PokemonForm>()
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getPokemonByName(name);
                setPokemon(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch Pokemon data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData().catch((reason) => console.error(reason))
    }, [name])

    return {pokemon, loading, error}
}