import React, { useMemo, useState } from "react";
import emptyIcon from "../../image/default.png";
import { MdAddCircleOutline, MdDeleteOutline } from "react-icons/md";
import CharacterModal from "../CharacterModal/CharacterModal";

const checkDisabledButton = (characters) => {
  return (
    characters.filter((character) => character.characterId !== 0).length === 5
  );
};

export default function TeamCompPreview({
  characters,
  addCharacterHandle,
  deleteCharacterHandle,
}) {
  const [characterModalIsOpen, setCharacterModalIsOpen] = useState(false);

  const usedCharacterIds = useMemo(() => {
    const usedCharacters = characters.filter(
      (character) => character.characterId !== 0
    );
    console.log(usedCharacters);
    if (usedCharacters.length > 0) {
      return usedCharacters.map((character) => character.characterId);
    }
    return [];
  }, [characters]);

  const closeModal = () => {
    setCharacterModalIsOpen(false);
  };

  const openModal = () => {
    setCharacterModalIsOpen(true);
  };

  const characterPreviewElement = ({ icon, star, rank, level, ue }, index) => {
    return (
      <div className="flex flex-col">
        <div className="text-stone-100 text-lg">
          <img alt="icon" src={icon ? icon : emptyIcon} className="min-w-0" />
          <div>Star: {star ? star : "-"}</div>
          <div>Rank: {rank ? rank : "-"}</div>
          <div>Level: {level ? level : "-"}</div>
          <div>UE: {ue ? ue : "-"}</div>
          {icon && (
            <button
              type="button"
              onClick={deleteCharacterHandle(index)}
              className="flex items-center justify-center p-2 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400"
            >
              <MdDeleteOutline size={16} className="text-stone-900" />
              <span className="font-semi-bold text-stone-900 text-lg">
                Delete
              </span>
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-4">
        {characters.map(characterPreviewElement)}
      </div>
      <button
        disabled={checkDisabledButton(characters)}
        type="button"
        onClick={openModal}
        className="flex items-center justify-center h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400"
      >
        <MdAddCircleOutline size={24} />
        <span className="font-semi-bold text-stone-900 text-2xl">
          Add Character
        </span>
      </button>
      <CharacterModal
        characterModalIsOpen={characterModalIsOpen}
        closeModal={closeModal}
        addCharacterHandle={addCharacterHandle}
        usedCharacterIds={usedCharacterIds}
      />
    </div>
  );
}
