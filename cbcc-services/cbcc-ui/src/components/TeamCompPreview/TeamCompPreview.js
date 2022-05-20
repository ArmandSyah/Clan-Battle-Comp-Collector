import React, { useMemo, useState } from "react";
import emptyIcon from "../../image/default.png";
import { MdAddCircleOutline, MdDeleteOutline } from "react-icons/md";
import CharacterModal from "../CharacterModal/CharacterModal";

const checkDisabledButton = (characters) => {
  return (
    characters.filter((character) => character.characterId !== 0).length === 5
  );
};

const initialCharacterState = {
  characterId: 0,
  icon: "",
  star: 0,
  rank: 0,
  ue: 0,
  level: 0,
  range: 0,
  notes: "",
};

export default function TeamCompPreview({
  characters,
  addCharacterHandle,
  deleteCharacterHandle,
  editCharacterHandle,
}) {
  const [characterModalIsOpen, setCharacterModalIsOpen] = useState(false);
  const [characterModalInEditMode, setCharacterModalInEditMode] =
    useState(false);
  const [currentCharacter, setCurrentCharacter] = useState(
    initialCharacterState
  );
  const [currentIndex, setCurrentIndex] = useState(-1);

  const usedCharacterIds = useMemo(() => {
    const usedCharacters = characters.filter(
      (character) =>
        character.characterId !== 0 &&
        character.characterId !== currentCharacter.characterId
    );
    if (usedCharacters.length > 0) {
      return usedCharacters.map((character) => character.characterId);
    }
    return [];
  }, [characters, currentCharacter]);

  const closeModal = () => {
    setCharacterModalInEditMode(false);
    setCurrentCharacter(initialCharacterState);
    setCurrentIndex(-1);
    setCharacterModalIsOpen(false);
  };

  const openModal = (editMode, character, index) => () => {
    setCharacterModalInEditMode(editMode);
    if (editMode) {
      setCurrentCharacter(character);
      setCurrentIndex(index);
    } else {
      setCurrentCharacter(initialCharacterState);
      setCurrentIndex(-1);
    }
    setCharacterModalIsOpen(true);
  };

  const openModalInEditMode = (editMode, character, index) => (event) => {
    if (character?.characterId !== 0) {
      openModal(editMode, character, index)(event);
    }
  };

  const onDeleteButtonClicked = (index) => () => {
    deleteCharacterHandle(index);
  };

  const characterPreviewElement = (character, index) => {
    const { icon, star, rank, level, ue } = character;
    return (
      <div key={`character-${index}`} className="flex flex-col">
        <div className="text-stone-100 text-lg">
          <img
            onClick={openModalInEditMode(true, character, index)}
            alt="icon"
            src={icon ? icon : emptyIcon}
            className="min-w-0"
          />
          <div>Star: {star ? star : "-"}</div>
          <div>Rank: {rank ? rank : "-"}</div>
          <div>Level: {level ? level : "-"}</div>
          <div>UE: {ue ? ue : "-"}</div>
          {icon && (
            <button
              type="button"
              onClick={onDeleteButtonClicked(index)}
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
      <div className="flex flex-row-reverse gap-4">
        {characters.map(characterPreviewElement)}
      </div>
      <button
        disabled={checkDisabledButton(characters)}
        type="button"
        onClick={openModal(false)}
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
        editCharacterHandle={editCharacterHandle}
        editMode={characterModalInEditMode}
        character={currentCharacter}
        index={currentIndex}
      />
    </div>
  );
}
