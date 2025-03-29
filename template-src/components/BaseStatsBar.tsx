export default function BaseStatsBar({name, value, max}: {name: string, value: number, max: number}) {
    return (
        <div className="flex w-full space-x-4 items-center justify-center text-sm">
            <span>{name}: {value}</span>
            <div className="w-1/2 h-4 bg-gray-300 rounded-full overflow-hidden">
                <div
                    className={`h-full bg-green-300`}
                    style={{width: `${value / max * 100}%`}}
                ></div>
            </div>
        </div>
    )
}