import {Evolution, PokemonForm} from "../types/Pokemon.type.ts";
import {getPokemonByName} from "../api";
import {ReactNode, useEffect, useState} from "react";

async function getFirstForm(pokemon: PokemonForm): Promise<PokemonForm> {
    if (pokemon.preEvolution) {
        return await getFirstForm(await getPokemonByName(pokemon.preEvolution));
    }
    return pokemon;
}

function EvolutionLine({evolution, isLast}: { evolution: Evolution, isLast: boolean }) {
    return (
        <div className="flex-col space-y-0.5 mx-2 mb-4">
            <div
                className="text-xs px-2">{evolution.requirements.map((requirement) => requirement.i18n_name).join(", ")}</div>
            {!isLast && (
                <div className="h-px w-full bg-gray-400"></div>
            )}
        </div>
    )
}

function EvolutionBranch({evolutionNodes}: { evolutionNodes: { evolution: Evolution, nodes: ReactNode }[] }) {
    {/* 这里终止渲染 */}
    if (evolutionNodes.length == 0) {
        return null
    }

    if (evolutionNodes.length == 1) {
        const {evolution, nodes} = evolutionNodes[0]

        return (
            <>
                {/*这里是倒数第二个, 因为只能进化一次*/}
                <EvolutionLine evolution={evolution} isLast={false}/>
                {nodes}
            </>
        )
    }

    {/* 这里渲染竖直线条与子链路 */}
    return (
        <div className="h-px w-full bg-gray-400"></div>
    )
}


function EvolutionNode({pokemon}: { pokemon: PokemonForm }) {
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
            <div className="flex-col">
                <img
                    className="w-16 h-16' rounded-full"
                    src={pokemon.image_url}
                    alt={pokemon.i18n_name}
                />
                <div className="mt-2 text-center">
                    <span className="text-sm font-medium">{pokemon.i18n_name}</span>
                </div>
            </div>
            {pokemon.evolutions && evolutionResults &&
                (
                    <EvolutionBranch evolutionNodes={pokemon.evolutions.map((evolution, index) => {
                        return {
                            evolution: evolution,
                            nodes: <EvolutionNode key={index} pokemon={evolutionResults[index]}/>
                        }
                    })}/>
                )
            }
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
            <EvolutionNode pokemon={firstForm}/>
        </div>
    ) : "Loading..."
}