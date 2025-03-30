import {useParams} from "react-router";
import {useEffect, useState} from "react";
import {Biome} from "../types/Pokemon.type.ts";
import {getBiomeByName} from "../api";

export default function useBiome() {
    const {name} = useParams<'name'>() as { name: string };

    const [biome, setBiome] = useState<Biome>()
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getBiomeByName(name)
                setBiome(data)
                setError(null);
            } catch (err) {
                setError('Failed to fetch biome data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData().catch((reason) => console.error(reason))
    }, [name])

    return {biome, loading, error}
}