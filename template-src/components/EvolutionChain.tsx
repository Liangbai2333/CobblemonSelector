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
            <div className="text-xs px-2">
                {evolution.i18n_name != '' ? `${evolution.i18n_name} ` : null}
                {evolution.requirements.map((requirement) => requirement.i18n_name).join(", ")}
                {evolution.consumeHeldItem ? " (消耗持有物)" : null}
            </div>
            {!isLast && (
                <div className="h-px w-full bg-gray-400"></div>
            )}
        </div>
    )
}

function EvolutionBranch({evolutionNodes}: { evolutionNodes: { evolution: Evolution, nodes: ReactNode }[] }) {
    {/* 这里终止渲染 */
    }
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

    {/* 这里渲染竖直线条与子链路 高度根据nodes数组大小计算, 不知道为什么justify-between不生效 */}
    const height = `${evolutionNodes.length * 6}rem`
    return (
        <div className="flex items-center">
            <div className="ml-2 h-0.5 w-8 bg-gray-400"></div>
            <div className="w-0.5 bg-gray-400" style={{
                height: height
            }}>
            </div>
            <div className="flex-col justify-between" style={{height: height}}>
                {evolutionNodes.map(({evolution, nodes}, index) => {
                    return (
                        <div key={index} className="flex items-center">
                            <EvolutionLine evolution={evolution} isLast={false}/>
                            {nodes}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}


function EvolutionNode({pokemon}: { pokemon: PokemonForm }) {
    const [evolutionResults, setEvolutionResults] = useState<PokemonForm[] | null>(null)

    const {i18n_name} = pokemon

    useEffect(() => {
        const fetchData = async () => {
            if (!pokemon.evolutions) {
                return
            }
            const evolutions = pokemon.evolutions.map((evolution) => {
                return getPokemonByName(evolution.result)
            })
            const results = await Promise.all(evolutions)
            setEvolutionResults(results)
        }
        fetchData().catch(console.error)
    }, [i18n_name]);

    return (
        <div className="flex items-center">
            <div className="flex-col">
                {pokemon.image_url != undefined ? <img
                    className="w-16 h-16'"
                    src={pokemon.image_url}
                    alt={pokemon.i18n_name}
                    onError={(e) => {
                        e.currentTarget.src = "/images/none.png"
                    }}
                /> : <img className="w-16 h-16'" src="/images/none.png"  alt="???"/>}
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

function renderEvolutionChainFrom(pokemon: PokemonForm) {
    return <EvolutionNode pokemon={pokemon}/>
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

    return firstForm ? renderEvolutionChainFrom(firstForm): "Loading..."
}