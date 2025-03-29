import {ReactNode} from "react";

export default function PokeInfoTag({className = "", children}: { className?: string, children: ReactNode[] | ReactNode }) {
    return (
        <div className={`flex flex-col px-4 shadow-md justify-center items-center rounded-md border border-sky-100 bg-blue-50/50 text-[0.7rem] py-0.5 space-y-1 ${className}`}>{children}</div>
    )
}