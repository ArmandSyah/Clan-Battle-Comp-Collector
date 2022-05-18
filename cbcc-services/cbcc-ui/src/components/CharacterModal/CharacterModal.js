import { Dialog } from "@headlessui/react";
import React, { useState } from "react";
import CharacterSelector from "../CharacterSelector/CharacterSelector";
import Input from "../Input/Input";
import emptyIcon from "../../image/default.png";

const initialState = {
  characterId: 0,
  icon: "",
  star: 0,
  rank: 0,
  ue: 0,
  level: 0,
  range: 0,
  notes: "",
};

export default function CharacterModal({
  addCharacterHandle,
  characterModalIsOpen,
  closeModal,
}) {
  const [characterModalState, setCharacterModalState] = useState(initialState);

  const handleInputChange = (key) => (event) => {
    setCharacterModalState((prevCharacterModalState) => {
      return { ...prevCharacterModalState, [key]: event.target.value };
    });
  };

  const handleNonSubmitClose = () => {
    setCharacterModalState(initialState);
    closeModal();
  };

  const handleCharacterClick = (character) => () => {
    setCharacterModalState((prevCharacterModalState) => {
      const characterId =
        prevCharacterModalState.unitId === character.unitId
          ? prevCharacterModalState.unitId
          : character.unitId;
      const characterIcon =
        prevCharacterModalState.icon === character.icon
          ? prevCharacterModalState.icon
          : character.icon;
      const characterRange =
        prevCharacterModalState.range === character.range
          ? prevCharacterModalState.range
          : character.range;
      return {
        ...prevCharacterModalState,
        characterId: characterId,
        icon: characterIcon,
        range: characterRange,
      };
    });
  };

  const handleSubmitCharacter = () => {
    addCharacterHandle(characterModalState);
    setCharacterModalState(initialState);
    closeModal();
  };

  return (
    <Dialog
      open={characterModalIsOpen}
      onClose={handleNonSubmitClose}
      className="relative z-50"
    >
      {/* The backdrop, rendered as a fixed sibling to the panel container */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

      {/* Full-screen scrollable container */}
      <div className="fixed inset-0 flex items-center justify-center p-4 overflow-scroll">
        {/* Container to center the panel */}
        <div className="flex min-h-full items-center justify-center">
          {/* The actual dialog panel  */}
          <Dialog.Panel className="mx-auto max-w-sm rounded bg-gradient-to-r from-slate-500 to-slate-800 p-12">
            <Dialog.Title
              as="h2"
              className="text-3xl font-bold leading-6 text-stone-100"
            >
              Add New Character
            </Dialog.Title>
            <div className="flex flex-col mt-4 gap-4">
              <CharacterSelector handleClick={handleCharacterClick} />
              <img
                src={
                  characterModalState.icon
                    ? characterModalState.icon
                    : emptyIcon
                }
                alt={characterModalState.characterId}
                className="h-1/3 w-1/3 bg-black border rounded"
              />
              <Input
                type="number"
                label="Star"
                value={characterModalState.star}
                handleChange={handleInputChange("star")}
                disabled={characterModalState.characterId === 0}
              />
              <Input
                type="number"
                label="Rank"
                value={characterModalState.rank}
                handleChange={handleInputChange("rank")}
                disabled={characterModalState.characterId === 0}
              />
              <Input
                type="number"
                label="Level"
                value={characterModalState.level}
                handleChange={handleInputChange("level")}
                disabled={characterModalState.characterId === 0}
              />
              <Input
                type="number"
                label="UE"
                value={characterModalState.ue}
                handleChange={handleInputChange("ue")}
                disabled={characterModalState.characterId === 0}
              />
              <Input
                type="text"
                label="Notes"
                value={characterModalState.notes}
                handleChange={handleInputChange("notes")}
                disabled={characterModalState.characterId === 0}
              />
              <button
                type="button"
                onClick={handleSubmitCharacter}
                className="flex items-center justify-center h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400"
              >
                <span className="font-semi-bold text-2xl">Add Character</span>
              </button>
            </div>
          </Dialog.Panel>
        </div>
      </div>
    </Dialog>
  );
}
