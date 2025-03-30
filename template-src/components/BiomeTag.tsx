export default function BiomeTag({biomeName}: { biomeName: string }) {
    return (
        <div className="w-fit px-1 rounded-sm shadow-sm bg-gray-300/50 text-gray-700 text-md text-center">
            {biomeName}
        </div>
    )
}