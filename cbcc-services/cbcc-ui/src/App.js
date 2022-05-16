import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import "./App.css";

import NavBar from "./components/NavBar/NavBar";
import ClanBattleRotation from "./pages/ClanBattleRotation";

function App() {
  return (
    <Router>
      <NavBar />
      <div>
        <Routes>
          <Route path="/clanbattle" element={<ClanBattleRotation />} />
          <Route path="*" element={<Navigate to="/clanbattle" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
