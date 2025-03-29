import {ReactNode} from "react";

ConditionContainer.Item = ({name, value, isFirst = false}: {name: string, value: ReactNode | ReactNode[], isFirst?: boolean}) => {
    return (
        <>
            {!isFirst && (
                <hr className="border-t border-dashed border-gray-300 my-2"/>
            )}
            <div className="flex justify-between gap-8">
                <span className="text-gray-700">{name}</span>
                <span className="text-gray-700">{value}</span>
            </div>
        </>
    )
}

export default function ConditionContainer({children}: { children: ReactNode[] | ReactNode }) {
    return (
        <div className="flex flex-col mx-3 p-3 rounded-md bg-gray-200/70">
            {children}
        </div>
    )
}