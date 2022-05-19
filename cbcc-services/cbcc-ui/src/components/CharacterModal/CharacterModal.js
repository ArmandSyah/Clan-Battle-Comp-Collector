import { Dialog } from "@headlessui/react";
import React, { useEffect, useState } from "react";
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
  usedCharacterIds,
  editCharacterHandle,
  editMode,
  index,
  character,
}) {
  const [characterModalState, setCharacterModalState] = useState(character);

  useEffect(() => {
    console.log(
      "Use Effect has been fired due to a change in the character prop"
    );
    setCharacterModalState(character);
  }, [character]);

  const handleInputChange = (key) => (event) => {
    setCharacterModalState((prevCharacterModalState) => {
      return { ...prevCharacterModalState, [key]: event.target.value };
    });
  };

  const handleCharacterClick = (character) => () => {
    if (usedCharacterIds.includes(character.unit_id)) {
      console.log(`Character ${character.unit_name_en} is already in the list`);
      return;
    }

    setCharacterModalState((prevCharacterModalState) => {
      const characterId =
        prevCharacterModalState.characterId === character.unit_id
          ? prevCharacterModalState.characterId
          : character.unit_id;
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

  const handleNonSubmitClose = () => {
    setCharacterModalState(initialState);
    closeModal();
  };

  const handleSubmitCharacter = () => {
    if (editMode) {
      editCharacterHandle(characterModalState, index);
    } else {
      addCharacterHandle(characterModalState);
    }
    setCharacterModalState(initialState);
    closeModal();
  };

  const isCharacterModalValid = () => {
    const numberRegex = /^[0-9\b]+$/;

    const characterSelected = characterModalState.characterId !== 0;
    const starValid =
      characterModalState.star !== "" &&
      numberRegex.test(characterModalState.star);
    const rankValid =
      characterModalState.rank !== "" &&
      numberRegex.test(characterModalState.rank);
    const levelValid =
      characterModalState.star !== "" &&
      numberRegex.test(characterModalState.star);
    const ueValid =
      characterModalState.level !== "" &&
      numberRegex.test(characterModalState.level);

    return characterSelected && starValid && rankValid && levelValid && ueValid;
  };

  return (
    <Dialog
      open={characterModalIsOpen}
      onClose={handleNonSubmitClose}
      className="absolute z-10 "
    >
      {/* The backdrop, rendered as a fixed sibling to the panel container */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

      {/* Full-screen scrollable container */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        {/* Container to center the panel */}
        <div className="flex h-auto w-auto items-center justify-center">
          {/* The actual dialog panel  */}
          <Dialog.Panel className="max-h-96 w-full max-w-md rounded bg-gradient-to-r from-slate-500 to-slate-800 p-12 overflow-y-auto">
            <Dialog.Title
              as="h2"
              className="flex justify-between text-2xl font-bold leading-6 text-stone-100"
            >
              <span>{editMode ? "Edit" : "Add New"} Character</span>
              <div>
                <button
                  type="button"
                  className="inline-flex justify-center px-2 py-1 text-sm font-medium text-gray-200 bg-gray-900 border border-transparent rounded hover:bg-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                  onClick={closeModal}
                >
                  X
                </button>
              </div>
            </Dialog.Title>

            <div className="flex flex-col mt-4 gap-4">
              <CharacterSelector
                handleClick={handleCharacterClick}
                selectedList={usedCharacterIds}
              />
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
                disabled={!isCharacterModalValid()}
                type="button"
                onClick={handleSubmitCharacter}
                className="flex disabled:opacity-20 items-center justify-center h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400"
              >
                <span className="font-semi-bold text-2xl">
                  {editMode ? "Edit" : "Add New"} Character
                </span>
              </button>
            </div>
          </Dialog.Panel>
        </div>
      </div>
    </Dialog>
  );
}
