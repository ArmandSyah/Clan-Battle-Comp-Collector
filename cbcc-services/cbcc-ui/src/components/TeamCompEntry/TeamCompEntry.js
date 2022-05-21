import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ExpectedDamageBadge, TierPlaystyle } from "../Badges/Badges";
import { MdEdit, MdDelete, MdDescription } from "react-icons/md";
import DeleteModal from "../DeleteModal/DeleteModal";

export default function TeamCompEntry({ teamComp, bossName, icon }) {
  const {
    id: teamCompId,
    expected_damage,
    phase,
    playstyle,
    team_comp_characters,
  } = teamComp;
  const [deleteModalIsOpen, setDeleteModalIsOpen] = useState(false);

  const closeModal = () => {
    setDeleteModalIsOpen(false);
  };

  const openModal = (event) => {
    setDeleteModalIsOpen(true);
  };

  const characterIcons = team_comp_characters.map(
    (team_comp_character) => team_comp_character.character
  );

  const ActionButtons = () => {
    return (
      <div className="flex flex-wrap ml-auto text-indigo-400">
        <Link
          to={{ pathname: `/viewTeamComp/${teamComp["id"]}` }}
          state={{ bossName: bossName, icon: icon }}
        >
          <MdDescription size={36} />
        </Link>
        <Link
          to={{ pathname: `/editTeamComp/${teamComp["id"]}` }}
          state={{ bossName: bossName, icon: icon }}
        >
          <MdEdit size={36} />
        </Link>
        <MdDelete
          size={36}
          onClick={openModal}
          className="hover:cursor-pointer"
        />
      </div>
    );
  };

  return (
    <div className="flex flex-col bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400 p-3">
      <div className="flex gap-2">
        {ExpectedDamageBadge(expected_damage)}
        {TierPlaystyle(phase, playstyle)}
        {ActionButtons()}
      </div>
      <div className="grid grid-cols-5">
        {characterIcons.map((character) => (
          <img
            key={`${teamCompId}-${character.unit_name_en}`}
            src={character.icon}
            className="scale-75 p-0.5 bg-black border rounded object-contain relative"
            alt={character.unit_name_en}
          />
        ))}
      </div>
      <DeleteModal
        deleteModalIsOpen={deleteModalIsOpen}
        closeModal={closeModal}
        teamCompId={teamCompId}
      />
    </div>
  );
}
