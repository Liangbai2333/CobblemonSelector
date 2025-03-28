import './App.css'
import PokeImage from "./components/PokeImage.tsx";
import PokeCard from "./components/PokeCard.tsx";

function App() {
    return (
        <>
            <PokeCard>
                <div className="inline-flex p-1 w-fit min-w-64 min-h-8 bg-blue-500 text-white">
                    <PokeImage name="小火龙" image="../images/Abra/Abra.png"/>
                    <span>小火龙</span>
                    <span className="ml-auto mr-2">1</span>
                </div>
            </PokeCard>
        </>
    )
}

export default App
