import Tag from "./Tag.tsx";

export default function Ability({name, description, hidden}: { name: string, description: string, hidden: boolean }) {
    return (
        <div className="border border-gray-200 rounded-lg px-2 py-1 w-full space-y-1">
            <div className="flex w-full text-lg text-blue-500 font-bold justify-between">
                <span>{name}</span>
                {hidden && (
                    <Tag className="inline-flex text-xs rounded-lg shadow-none text-gray-700" color="gray" text="隐藏"/>
                )}
            </div>
            <div className="text-xs ">{description}</div>
        </div>
    )
}