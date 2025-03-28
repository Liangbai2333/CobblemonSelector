import './App.css'
import {BrowserRouter, Navigate, Route, Routes} from "react-router";
import Pokemon from "./layouts/Pokemon.tsx";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Pokemon />} />
                <Route path="/pokemon">
                    <Route index element={<Navigate to="/pokemon/1" replace />}/>
                    <Route path=":id" element={<Pokemon />}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
