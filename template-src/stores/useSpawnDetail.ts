import {useEffect, useState} from "react";
import {SpawnDetail} from "../types/Pokemon.type.ts";
import {getSpawnByNameAndIndex} from "../api";
import {useParams} from "react-router";

// 暂时不用
export default function useSpawnDetail() {
    const {name, index} = useParams<{ name: string, index: string }>();

    const [detail, setDetail] = useState<SpawnDetail>()
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getSpawnByNameAndIndex(name!!, parseInt(index!!))
                setDetail(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch Pokemon data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData().catch((reason) => console.error(reason))
    }, [name, index])

    return {detail, loading, error}
}