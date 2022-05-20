import React from "react";
import { ExpectedDamageBadge, TierPlaystyle } from "../Badges/Badges";
import { MdEdit, MdDelete } from "react-icons/md";

const ActionButtons = () => {
  return (
    <div className="flex ml-auto">
      <MdEdit size={36} className="text-indigo-400" />
      <MdDelete size={36} className="text-indigo-400" />
    </div>
  );
};

export default function TeamCompEntry(props) {
  const { expected_damage, phase, playstyle, team_comp_characters } =
    props.teamComp;

  const characterIcons = team_comp_characters.map(
    (team_comp_character) => team_comp_character.character
  );

  return (
    <div className="flex flex-col bg-stone-300 hover:bg-stone-400 rounded-3xl shadow-xl border-2 border-indigo-400 p-3">
      <div className="flex gap-2">
        {ExpectedDamageBadge(expected_damage)}
        {TierPlaystyle(phase, playstyle)}
        {ActionButtons()}
      </div>
      <div className="grid grid-cols-5">
        {characterIcons.map((character) => (
          <img
            src={character.icon}
            className="scale-75 p-0.5 bg-black border rounded object-contain relative"
            alt={character.unit_name_en}
          />
        ))}
      </div>
    </div>
  );
}
