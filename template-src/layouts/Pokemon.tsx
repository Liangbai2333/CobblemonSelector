import PokeCard from "../components/PokeCard.tsx";
import PokeImage from "../components/PokeImage.tsx";
import {useParams} from "react-router";
import {getPokemonByName} from '../api';
import {PokemonForm} from '../types/Pokemon.type';
import {useEffect, useState} from "react";
import TypeTag from "../components/TypeTag.tsx";
import PokeInfoTag from "../components/PokeInfoTag.tsx";

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
                console.log(data)
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
            <div className="text-center font-sans">
                {loading && <p>Loading...</p>}
                {error && <p>{error}</p>}
                {pokemon && (
                    <PokeCard>
                        <div className="inline-flex p-1 w-full min-w-64 min-h-8 bg-blue-500 text-white">
                            <div className="m-2">
                                <span className="mt-auto text-sm"># {pokemon.pokedex_number}</span>
                                <span
                                    className="ml-2 mt-auto text-2xl font-bold">{pokemon.i18n_name} ({pokemon.name})</span>
                            </div>
                        </div>
                        <div className="flex">
                            <div className="flex-col w-fit p-3 mr-2">
                                <PokeImage name={pokemon.i18n_name} image={pokemon.image_url}/>
                                <div className="mt-5 space-y-2">
                                    <TypeTag primaryType={pokemon.primaryType}/>
                                    {pokemon.secondaryType && <TypeTag primaryType={pokemon.secondaryType}/>}
                                </div>
                            </div>
                            <div className="grid grid-cols-2 auto-rows-max mt-4 pr-3 gap-2">
                                <PokeInfoTag>
                                    <span className="text-gray-700">身高</span>
                                    <span>{pokemon.height / 10}{' '}米</span>
                                </PokeInfoTag>
                                <PokeInfoTag>
                                    <span className="text-gray-700">体重</span>
                                    <span>{pokemon.weight / 10}{' '}千克</span>
                                </PokeInfoTag>
                                <PokeInfoTag>
                                    <span className="text-gray-700">性别比例</span>
                                    <span>{pokemon.maleRatio != -1 ? `♂${pokemon.maleRatio * 100}%: ♀${100 - pokemon.maleRatio * 100}%` : "无性别"}</span>
                                </PokeInfoTag>
                                {pokemon.eggGroups && (
                                    <PokeInfoTag>
                                        <span className="text-gray-700">蛋组</span>
                                        <span>{pokemon.eggGroups.map(eggGroup => eggGroup.i18n_name).join(", ")}</span>
                                    </PokeInfoTag>
                                )}
                            </div>
                        </div>
                    </PokeCard>
                )}
            </div>
        </>
    )
}