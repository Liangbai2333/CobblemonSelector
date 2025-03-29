import {PokemonType} from "../types/Pokemon.type.ts";

export default function TypeTag({primaryType}: { primaryType: PokemonType }) {
    const typeTranslations = {
        normal: '一般',
        fire: '火',
        water: '水',
        grass: '草',
        electric: '电',
        ice: '冰',
        fighting: '格斗',
        poison: '毒',
        ground: '地面',
        flying: '飞行',
        psychic: '超能力',
        bug: '虫',
        rock: '岩石',
        ghost: '幽灵',
        dragon: '龙',
        dark: '恶',
        steel: '钢',
        fairy: '妖精'
    };

    // Type color mapping using Tailwind classes
    const typeColors = {
        normal: 'bg-gray-400 text-gray-800',
        fire: 'bg-red-500 text-white',
        water: 'bg-blue-500 text-white',
        grass: 'bg-green-500 text-white',
        electric: 'bg-yellow-400 text-yellow-900',
        ice: 'bg-blue-200 text-blue-800',
        fighting: 'bg-red-700 text-white',
        poison: 'bg-purple-500 text-white',
        ground: 'bg-yellow-600 text-white',
        flying: 'bg-blue-300 text-blue-800',
        psychic: 'bg-pink-500 text-white',
        bug: 'bg-green-400 text-green-900',
        rock: 'bg-yellow-700 text-white',
        ghost: 'bg-purple-700 text-white',
        dragon: 'bg-indigo-700 text-white',
        dark: 'bg-gray-700 text-white',
        steel: 'bg-gray-500 text-white',
        fairy: 'bg-pink-300 text-pink-800'
    };

    // Get the Chinese translation and color class for the given type
    const translation: string = typeTranslations[primaryType] || primaryType;
    const colorClass: string = typeColors[primaryType] || 'bg-gray-200 text-gray-800';

    return (
        <div className={`${colorClass} w-16 h-6 rounded-xl ring font-bold`}>
            {translation}
        </div>
    )
}
