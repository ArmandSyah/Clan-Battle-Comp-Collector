import React from "react";

import { MdEdit, MdDelete } from "react-icons/md";

const TierBadge = new Map([
  [
    1,
    <div className="text-stone-100 bg-sky-300 rounded-xl px-5 py-1 text-center text-sm">
      Tier 1
    </div>,
  ],
  [
    2,
    <div className="text-stone-100 bg-green-500 rounded-xl px-5 py-1 text-center text-sm">
      Tier 2
    </div>,
  ],
  [
    3,
    <div className="text-stone-100 bg-fuchsia-400 rounded-xl px-5 py-1 text-center text-sm">
      Tier 3
    </div>,
  ],
  [
    4,
    <div className="text-stone-100 bg-rose-600 rounded-xl px-5 py-1 text-center text-sm">
      Tier 4
    </div>,
  ],
  [
    5,
    <div className="text-stone-100 bg-fuchsia-800 rounded-xl px-5 py-1 text-center text-sm">
      Tier 5
    </div>,
  ],
]);

const PlaystyleBadge = new Map([
  [
    "auto",
    <div className="text-stone-100 bg-sky-300 rounded-xl px-5 py-1 text-center text-sm">
      Auto
    </div>,
  ],
  [
    "semi",
    <div className="text-stone-100 bg-green-500 rounded-xl px-5 py-1 text-center text-sm">
      Semi
    </div>,
  ],
  [
    "manual",
    <div className="text-stone-100 bg-blue-700 rounded-xl px-5 py-1 text-center text-sm">
      Manual
    </div>,
  ],
]);

const ExpectedDamageBadge = (damage) => {
  return (
    <div className="flex flex-col">
      <div className="text-stone-100 bg-sky-600 rounded-xl text-center px-6 py-1 text-sm">
        Expected Damage
      </div>
      <span className="text-3xl drop-shadow-xl">{damage}</span>
    </div>
  );
};

const TierPlaystyle = (tier, playstyle) => {
  return (
    <div className="flex flex-col gap-1">
      {TierBadge.get(tier)}
      {PlaystyleBadge.get(playstyle.toLowerCase())}
    </div>
  );
};

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
