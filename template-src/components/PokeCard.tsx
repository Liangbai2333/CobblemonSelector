import {ReactElement} from "react";

export default function PokeCard({children}: { children: ReactElement }) {
    return (
        <div className="flex h-screen w-screen justify-center">
            <div className="shadow-md rounded-xl flex-col max-h-screen max-w-screen items-center overflow-hidden">
                {children}
            </div>
        </div>
    )
}