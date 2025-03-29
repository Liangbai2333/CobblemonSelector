export default function Tag({color = "yellow", text, className}: {
    color?: 'gray' | 'yellow',
    text: string,
    className?: string
}) {
    const colors = {
        gray: "bg-gray-200/50 border-gray-300",
        yellow: "bg-yellow-100/50 border-yellow-200"
    };

    return (
        <div className={`${colors[color]} p-1 rounded-2xl shadow-md text-center border ${className}`}>{text}</div>
    )
}