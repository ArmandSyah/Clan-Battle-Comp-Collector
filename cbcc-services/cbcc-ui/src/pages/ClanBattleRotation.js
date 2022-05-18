import React from "react";

import ClanBattleRotationBoss from "../components/ClanBattleRotationBoss/ClanBattleRotationBoss";
import TeamCompEntry from "../components/TeamCompEntry/TeamCompEntry";
import { useGetLatestClanBattleQuery } from "../app/api/apiSlice";

const TeamCompEntries = (teamComp) => {
  return <TeamCompEntry teamComp={teamComp} />;
};

const ClanBattleRotationBossSection = (bossData) => {
  const teamComps = bossData["team_comps"];

  const teamCompElements = teamComps.map(TeamCompEntries);

  return (
    <ClanBattleRotationBoss
      key={bossData["unit_name_en"]}
      bossId={bossData["id"]}
      bossName={bossData["unit_name_en"]}
      icon={bossData["icon"]}
    >
      {teamCompElements}
    </ClanBattleRotationBoss>
  );
};

export default function ClanBattleRotation() {
  const {
    data: clanBattleInfo,
    isLoading,
    isFetching,
    isSuccess,
  } = useGetLatestClanBattleQuery();

  let bosses;
  if (isSuccess) {
    bosses = clanBattleInfo["bosses"];
  }

  return isLoading || isFetching ? (
    <div>Loading is happening</div>
  ) : (
    <div className="grid grid-cols-1 2xl:grid-cols-5 gap-3 px-4 pt-6 flex-wrap">
      {bosses.map(ClanBattleRotationBossSection)}
    </div>
  );
}
