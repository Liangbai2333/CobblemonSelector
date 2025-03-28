import PokeCard from "../components/PokeCard.tsx";
import PokeImage from "../components/PokeImage.tsx";
import {useParams} from "react-router";

export default function Pokemon() {
    const { id } = useParams<'id'>();

    console.log(id)

    return (
        <>
            <PokeCard>
                <div className="inline-flex p-1 w-fit min-w-64 min-h-8 bg-blue-500 text-white">
                    <PokeImage name="小火龙" image="../images/Abra/Abra.png"/>
                    <span className="mt-auto">小火龙</span>
                    <span className="ml-auto mr-2">1</span>
                </div>
            </PokeCard>
        </>
    )
}