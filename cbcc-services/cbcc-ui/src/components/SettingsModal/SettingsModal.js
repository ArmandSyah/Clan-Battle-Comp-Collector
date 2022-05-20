import { Dialog } from "@headlessui/react";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  addMissingCharacter,
  changePlaystyle,
  removeMissingCharacter,
} from "../../app/api/settingsSlice";
import CharacterSelector from "../CharacterSelector/CharacterSelector";
import ListboxComponent from "../ListboxComponent/ListboxComponent";

const playstyles = [
  { id: 0, label: "All", value: "all" },
  { id: 1, label: "Auto", value: "auto" },
  { id: 2, label: "Semi", value: "semi" },
  { id: 3, label: "Manual", value: "manual" },
];

export default function SettingsModal({ settingsModalIsOpen, closeModal }) {
  const missingCharacters = useSelector(
    (state) => state.settings.missingCharacterIds
  );
  const filteredPlaystyle = useSelector((state) => state.settings.playstyle);

  const currentPlaystyle = playstyles.filter(
    (playstyle) => playstyle.value === filteredPlaystyle
  )[0];

  const dispatch = useDispatch();

  const handleClick = (character) => () => {
    const characterId = character.unit_id;

    if (missingCharacters.includes(characterId)) {
      dispatch(removeMissingCharacter({ characterId }));
    } else {
      dispatch(addMissingCharacter({ characterId }));
    }
  };

  const handleSelectChange = (value) =>
    dispatch(changePlaystyle({ playstyle: value.value }));

  return (
    <Dialog
      open={settingsModalIsOpen}
      onClose={closeModal}
      className="absolute z-10"
    >
      {/* The backdrop, rendered as a fixed sibling to the panel container */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      {/* Full-screen scrollable container */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        {/* Container to center the panel */}
        <div className="flex h-auto w-auto items-center justify-center">
          <Dialog.Panel className="max-h-96 w-full max-w-md rounded bg-gradient-to-r from-slate-500 to-slate-800 p-12 overflow-y-auto">
            <Dialog.Title
              as="h2"
              className="flex justify-between text-2xl font-bold leading-6 text-stone-100"
            >
              <span>Settings</span>
              <button
                type="button"
                className="inline-flex justify-center px-2 py-1 text-sm font-medium text-gray-300 border border-transparent rounded hover:bg-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                onClick={closeModal}
              >
                X
              </button>
            </Dialog.Title>
            <div className="flex flex-col mt-4 gap-4">
              <h3 className="text-stone-100 italic">Filter Charactrers</h3>
              <CharacterSelector
                handleClick={handleClick}
                selectedList={missingCharacters}
              />
              <ListboxComponent
                label="Playstyle"
                value={currentPlaystyle}
                options={playstyles}
                handleChange={handleSelectChange}
              />
            </div>
          </Dialog.Panel>
        </div>
      </div>
    </Dialog>
  );
}
