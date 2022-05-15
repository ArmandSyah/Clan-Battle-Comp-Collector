import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import "./App.css";

import { useGetLatestClanBattleQuery } from "./app/api/apiSlice";

import ClanBattleRotation from "./pages/ClanBattleRotation";

function App() {
  console.log(useGetLatestClanBattleQuery());

  console.log("test");

  return (
    <Router>
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
