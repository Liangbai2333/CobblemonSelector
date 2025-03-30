import {useParams} from "react-router";
import {useEffect, useState} from "react";
import {BiomeSpawn} from "../types/Pokemon.type.ts";
import {getSpawnBiomeByName} from "../api";

export default function useSpawnBiome() {
    const {name} = useParams<'name'>() as { name: string };

    const [spawnBiome, setSpawnBiome] = useState<BiomeSpawn>()
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getSpawnBiomeByName(name)
                setSpawnBiome(data)
                setError(null);
            } catch (err) {
                setError('Failed to fetch spawn biome data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData().catch((reason) => console.error(reason))
    }, [name])

    return {spawnBiome, loading, error}
}