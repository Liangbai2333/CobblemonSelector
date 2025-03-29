export default function Ability({name, description}: {name: string, description: string}) {
    return (
        <div className="border border-gray-200 rounded-lg p-1 min-w-64 gap-1">
            <div className="justify-self-start text-xl text-blue-500">{name}</div>
            <div className="text-xs">{description}</div>
        </div>
    )
}