import {PokemonForm} from "../types/Pokemon.type.ts";
import {getPokemonByName} from "../api";
import {useEffect, useState} from "react";

async function getFirstForm(pokemon: PokemonForm): Promise<PokemonForm> {
    if (pokemon.preEvolution) {
        return await getFirstForm(await getPokemonByName(pokemon.preEvolution));
    }
    return pokemon;
}

export default function EvolutionChain({pokemon}: { pokemon: PokemonForm }) {
    const { i18n_name } = pokemon

    const [firstForm, setFirstForm] = useState<PokemonForm | null>(null)
    useEffect(() => {
        getFirstForm(pokemon).then((form) => {
            setFirstForm(form)
        }).catch(() => { setFirstForm(pokemon) })
    }, [i18n_name])

    return (
        <div className="ml-4 w-32 p-2 bg-blue-500 text-white text-center rounded shadow">
            {firstForm?.i18n_name}
        </div>
    )
}