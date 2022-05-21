import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import {
  useGetTeamCompQuery,
  useUpdateTeamCompMutation,
} from "../../app/api/apiSlice";
import AddingTeamComp from "../../components/Gif/AddingTeamComp";
import Loading from "../../components/Gif/Loading";
import TeamComp, { initialCharacter, phases, playstyles } from "./TeamComp";

export default function EditTeamComp() {
  const { teamCompId } = useParams();
  const location = useLocation();
  const { bossName, icon } = location.state;

  const navigate = useNavigate();

  const {
    data: teamComp,
    isFetching,
    isLoading,
    isSuccess,
  } = useGetTeamCompQuery(teamCompId);

  const [
    updateTeamComp,
    { isLoading: edittingTeamComp, isSuccess: teamCompEditted },
  ] = useUpdateTeamCompMutation();

  if (isFetching || isLoading) {
    return (
      <div className="absolute top-2/4 left-2/4">
        <Loading />
      </div>
    );
  } else if (isSuccess) {
    let characters = teamComp["team_comp_characters"].map(
      (teamCompCharacter) => ({
        id: teamCompCharacter.id,
        characterId: teamCompCharacter.character_id,
        icon: teamCompCharacter.icon,
        star: teamCompCharacter.star,
        rank: teamCompCharacter.rank,
        ue: teamCompCharacter.ue,
        level: teamCompCharacter.level,
        range: teamCompCharacter.range,
        notes: teamCompCharacter.notes || "",
      })
    );

    while (characters.length < 5) {
      characters = [{ ...initialCharacter }, ...characters];
    }
    const teamCompState = {
      ...teamComp,
      notes: teamComp["notes"] || "",
      videoUrl: teamComp["video_url"] || "",
      expectedDamage: teamComp["expected_damage"],
      phase: phases.filter((phase) => phase.value === teamComp["phase"])[0],
      playstyle: playstyles.filter(
        (playstyle) => playstyle.value === teamComp["playstyle"]
      )[0],
      characters,
    };

    const onEditTeamCompClicked = async (state) => {
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
          video_url: state.videoUrl,
          teamcomp_characters: characters,
          phase: state.phase.value,
          playstyle: state.playstyle.value,
          expected_damage: Number(state.expectedDamage),
          notes: state.notes,
        };
        await updateTeamComp({ teamCompId, teamComp }).unwrap();
      } catch (err) {
        console.log("Failed to save team comp: ", err);
      }
    };

    if (edittingTeamComp) {
      return (
        <div className="absolute top-2/4 left-2/4">
          <AddingTeamComp />
        </div>
      );
    } else if (teamCompEditted) {
      console.log("Team comp has been editted");
      return navigate("/clanBattle");
    }

    return (
      <TeamComp
        bossName={bossName}
        icon={icon}
        handleSubmitClick={onEditTeamCompClicked}
        submitText="Edit Team Comp"
        teamCompState={teamCompState}
      />
    );
  }
}
