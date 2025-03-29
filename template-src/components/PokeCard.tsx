import {ReactNode} from "react";
import {PokemonForm} from "../types/Pokemon.type.ts";

PokeCard.Header = ({pokemon}: { pokemon: PokemonForm }) => (
    <div className="inline-flex p-1 w-full min-w-64 min-h-8 bg-blue-500 text-white">
        <div className="m-2">
            <span className="mt-auto text-sm"># {pokemon.pokedex_number}</span>
            <span
                className="ml-2 mt-auto text-2xl font-bold">{pokemon.i18n_name} ({pokemon.name})</span>
        </div>
    </div>
)

export default function PokeCard({children}: { children: ReactNode[] | ReactNode }) {
    return (
        <div className="flex justify-center">
            <div className="pokemon-start shadow-xl flex-col items-center">
                {children}
            </div>
        </div>
    )
}