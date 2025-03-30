import './App.css'
import {BrowserRouter, Navigate, Route, Routes} from "react-router";
import Pokemon from "./layouts/Pokemon.tsx";
import SpawnDetail from "./layouts/SpawnDetail.tsx";
import Biome from "./layouts/Biome.tsx";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/pokemon/bulbasaur" replace />} />
                <Route path="/pokemon">
                    <Route index element={<Navigate to="/pokemon/bulbasaur" replace />}/>
                    <Route path=":name" element={<Pokemon />}/>
                </Route>
                <Route path="/spawn">
                    <Route index element={<Navigate to="/spawn/bulbasaur/0" replace />}/>
                    <Route path=":name/:index" element={<SpawnDetail />}/>
                </Route>
                <Route path="/biome">
                    <Route index element={<Navigate to="/biome/is_jungle" replace />}/>
                    <Route path=":name" element={<Biome />}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
