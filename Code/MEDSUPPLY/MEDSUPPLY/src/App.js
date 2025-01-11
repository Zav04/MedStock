import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Medicamentos from "./pages/Medicamentos";
import Vacinas from "./pages/Vacinas";
import Descartaveis from "./pages/Descartaveis";
import Consumiveis from "./pages/Consumiveis";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/Medicamentos" element={<Medicamentos />} />
      <Route path="/Vacinas" element={<Vacinas />} />
      <Route path="/Descartaveis" element={<Descartaveis />} />
      <Route path="/Consumiveis" element={<Consumiveis />} />
    </Routes>
  );
};

export default App;
