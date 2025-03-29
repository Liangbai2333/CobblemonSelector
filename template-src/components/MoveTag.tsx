import {Move} from "../types/Pokemon.type.ts";

export default function MoveTag({move}: { move: Move }) {
    return (
        <div className="w-fit h-4 px-1 rounded-sm shadow-sm bg-gray-300/50 text-gray-700 text-xs text-center">
            {move.i18n_name}
            {(typeof move.condition == 'number') && (
                <span>
                    {` (Lv. ${move.condition})`}
                </span>
            )}
        </div>
    )
}