import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import NavBar from "./components/NavBar/NavBar";
import ClanBattleRotation from "./pages/ClanBattleRotation";
import AddTeamComp from "./pages/AddTeamComp";
import ViewTeamComp from "./pages/ViewTeamComp";

function App() {
  return (
    <>
      <NavBar />
      <div>
        <Routes>
          <Route path="/clanBattle" element={<ClanBattleRotation />} />
          <Route path="/addTeamComp" element={<AddTeamComp />} />
          <Route path="/viewTeamComp/:teamCompId" element={<ViewTeamComp />} />
          <Route path="*" element={<Navigate to="/clanBattle" replace />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
