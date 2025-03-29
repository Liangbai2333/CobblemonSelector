import {ReactNode} from "react";

export default function PokeCard({children}: { children: ReactNode[] }) {
    return (
        <div className="flex h-screen w-screen justify-center">
            <div className="pokemon-start shadow-xl rounded-xl flex-col max-h-screen max-w-screen items-center overflow-y-auto">
                {children}
            </div>
        </div>
    )
}