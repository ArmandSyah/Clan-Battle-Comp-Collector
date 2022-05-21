import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAddTeamCompMutation } from "../../app/api/apiSlice";
import AddingTeamComp from "../../components/Gif/AddingTeamComp";
import TeamComp from "./TeamComp";

export default function AddTeamComp() {
  const location = useLocation();
  const { bossId, bossName, icon } = location.state;

  const navigate = useNavigate();

  const [
    addNewTeamComp,
    { isLoading: addingTeamComp, isSuccess: teamCompAdded },
  ] = useAddTeamCompMutation();

  const onAddTeamCompClicked = async (state) => {
    try {
      const characters = state.characters
        .filter((character) => character.characterId !== 0)
        .map((character) => {
          return {
            character_id: character.characterId,
            star: Number(character.star),
            rank: Number(character.rank),
            ue: Number(character.ue),
            level: Number(character.level),
            notes: character.notes,
          };
        });

      const teamComp = {
        ...state,
        boss_id: bossId,
        video_url: state.videoUrl,
        teamcomp_characters: characters,
        phase: state.phase.value,
        playstyle: state.playstyle.value,
        expected_damage: Number(state.expectedDamage),
      };
      await addNewTeamComp(teamComp).unwrap();
    } catch (err) {
      console.log("Failed to save team comp: ", err);
    }
  };

  if (addingTeamComp) {
    return (
      <div className="absolute top-2/4 left-2/4">
        <AddingTeamComp />
      </div>
    );
  } else if (teamCompAdded) {
    console.log("Team comp has been added");
    return navigate("/clanBattle");
  }

  return (
    <TeamComp
      bossName={bossName}
      icon={icon}
      handleSubmitClick={onAddTeamCompClicked}
      submitText="Add Team Comp"
    />
  );
}
