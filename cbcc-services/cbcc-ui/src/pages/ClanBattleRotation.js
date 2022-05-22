import React from "react";
import { useSelector } from "react-redux";
import ClanBattleRotationBoss from "../components/ClanBattleRotationBoss/ClanBattleRotationBoss";
import TeamCompEntry from "../components/TeamCompEntry/TeamCompEntry";
import { useGetLatestClanBattleQuery } from "../app/api/apiSlice";
import Loading from "../components/Gif/Loading";
import Error from "../components/Gif/Error";

export default function ClanBattleRotation() {
  const {
    data: clanBattleInfo,
    isLoading,
    isFetching,
    isSuccess,
  } = useGetLatestClanBattleQuery();

  const missingCharacters = useSelector(
    (state) => state.settings.missingCharacterIds
  );
  const filteredPlaystyle = useSelector((state) => state.settings.playstyle);

  const TeamCompEntries = (bossName, icon) => (teamComp) => {
    return (
      <TeamCompEntry
        key={teamComp.id}
        teamComp={teamComp}
        bossName={bossName}
        icon={icon}
      />
    );
  };

  const ClanBattleRotationBossSection = (bossData) => {
    const teamComps = bossData["team_comps"];

    const { id, unit_name_en, icon } = bossData;

    const filterOutTeamComps = teamComps.filter((teamComp) => {
      const { team_comp_characters: teamCompCharacters, playstyle } = teamComp;

      const teampCompCharacterIds = teamCompCharacters.map(
        (teamCompCharacter) => teamCompCharacter.character_id
      );

      const containsMissingCharacter =
        teampCompCharacterIds.filter((characterId) =>
          missingCharacters.includes(characterId)
        ).length > 0;

      const isFilteredPlaystyle =
        filteredPlaystyle.toLowerCase() === "all" ||
        playstyle.toLowerCase() === filteredPlaystyle.toLowerCase();

      return !containsMissingCharacter && isFilteredPlaystyle;
    });

    const teamCompElements = filterOutTeamComps.map(
      TeamCompEntries(unit_name_en, icon)
    );

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

  if (isLoading || isFetching) {
    return (
      <div className="absolute top-2/4 left-2/4">
        <Loading />
      </div>
    );
  } else if (isSuccess) {
    const bosses = clanBattleInfo["bosses"];
    return bosses ? (
      <div className="grid grid-cols-1 3xl:grid-cols-5 gap-3 px-4 pt-6 flex-wrap">
        {bosses.map(ClanBattleRotationBossSection)}
      </div>
    ) : (
      <Error />
    );
  }
}
