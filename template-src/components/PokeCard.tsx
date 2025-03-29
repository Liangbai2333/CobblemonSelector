import {ReactNode} from "react";

export default function PokeCard({children}: { children: ReactNode[] }) {
    return (
        <div className="flex justify-center">
            <div className="pokemon-start shadow-xl flex-col items-center">
                {children}
            </div>
        </div>
    )
}