import React from "react";
import { Link } from "react-router-dom";
import ClanBattleRotationBoss from "../components/ClanBattleRotationBoss/ClanBattleRotationBoss";
import TeamCompEntry from "../components/TeamCompEntry/TeamCompEntry";
import { useGetLatestClanBattleQuery } from "../app/api/apiSlice";
import Loading from "../components/Gif/Loading";

const TeamCompEntries = (bossName, icon) => (teamComp) => {
  return (
    <Link
      to={{ pathname: `/viewTeamComp/${teamComp["id"]}` }}
      state={{ bossName: bossName, icon: icon }}
    >
      <TeamCompEntry teamComp={teamComp} />
    </Link>
  );
};

const ClanBattleRotationBossSection = (bossData) => {
  const teamComps = bossData["team_comps"];

  const { id, unit_name_en, icon } = bossData;

  const teamCompElements = teamComps.map(TeamCompEntries(unit_name_en, icon));

  return (
    <ClanBattleRotationBoss
      key={unit_name_en}
      bossId={id}
      bossName={unit_name_en}
      icon={icon}
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
    <div className="absolute top-2/4 left-2/4">
      <Loading />
    </div>
  ) : (
    <div className="grid grid-cols-1 3xl:grid-cols-5 gap-3 px-4 pt-6 flex-wrap">
      {bosses.map(ClanBattleRotationBossSection)}
    </div>
  );
}
