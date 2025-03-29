import {PokemonForm} from "../types/Pokemon.type.ts";
import {getPokemonByName} from "../api";
import {useEffect, useState} from "react";

async function getFirstForm(pokemon: PokemonForm): Promise<PokemonForm> {
    if (pokemon.preEvolution) {
        return await getFirstForm(await getPokemonByName(pokemon.preEvolution));
    }
    return pokemon;
}


// 先放置自己，绘制线条后递归交给下一级PokemonForm
export function EvolutionNode({pokemon}: { pokemon: PokemonForm }) {
    const [evolutionResults, setEvolutionResults] = useState<PokemonForm[] | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            const evolutions = pokemon.evolutions.map((evolution) => {
                return getPokemonByName(evolution.result)
            })
            const results = await Promise.all(evolutions)
            setEvolutionResults(results)
        }
        fetchData().catch(console.error)
    }, []);

    return (
        <div className="flex items-center">
            <div
                className="w-fit p-1 bg-blue-500 text-white text-center rounded shadow"
            >
                {pokemon.i18n_name}
            </div>
            {pokemon.evolutions.map((evolution) => {
                return (
                    <div className="flex items-center">
                        <div className="flex-col space-y-0.5 mx-2 mb-4">
                            <div
                                className="text-xs px-4">{evolution.requirements.map((requirement) => requirement.i18n_name).join(", ")}</div>
                            {pokemon.evolutions && (
                                <div className="h-px w-full bg-gray-400"></div>
                            )}
                        </div>
                        {evolutionResults && evolutionResults.map((result) => {
                            return <EvolutionNode pokemon={result}/>
                        })}
                    </div>
                )
            })}

        </div>
    )
}

export default function EvolutionChain({pokemon}: { pokemon: PokemonForm }) {
    const {i18n_name} = pokemon

    const [firstForm, setFirstForm] = useState<PokemonForm | null>(null)
    useEffect(() => {
        getFirstForm(pokemon).then((form) => {
            setFirstForm(form)
        }).catch(() => {
            setFirstForm(pokemon)
        })
    }, [i18n_name])

    return firstForm ? (
        <div className="ml-4">
            <EvolutionNode pokemon={firstForm} />
        </div>
    ) : "Loading..."
}