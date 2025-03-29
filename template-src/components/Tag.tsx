export default function Tag({style = "", text}: { style?: string, text: string }) {
    return (
        <div className={`bg-yellow-100/50 p-1 rounded-2xl shadow-md text-center border border-yellow-200/30 ${style}`}>{text}</div>
    )
}