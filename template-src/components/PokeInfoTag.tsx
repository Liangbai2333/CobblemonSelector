import {ReactElement} from "react";

export default function PokeInfoTag({children}: { children: ReactElement[] }) {
    return (
        <div className="flex flex-col px-8 shadow-md justify-center items-center rounded-md border border-sky-100 bg-blue-50/50 text-sm py-1 space-y-1">{children}</div>
    )
}