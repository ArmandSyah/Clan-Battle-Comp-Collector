import { Tab } from "@headlessui/react";
import React, { useMemo } from "react";
import { useGetCharactersQuery } from "../../app/api/apiSlice";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const characterGrid = (characters, handleClick, selectedList) => {
  console.log(selectedList);
  return (
    <div className="grid grid-cols-6 overflow-y-scroll max-h-32 gap-1">
      {characters.map((character) => {
        const characterId = character.unit_id;
        const isAlreadySelected = selectedList.includes(characterId);

        return (
          <img
            src={character.icon}
            alt={character.unit_id}
            className={classNames(
              "bg-black border rounded",
              isAlreadySelected
                ? "grayscale"
                : "cursor-pointer hover:drop-shadow-xl"
            )}
            onClick={handleClick(character)}
          />
        );
      })}
    </div>
  );
};

export default function CharacterSelector({ handleClick, selectedList }) {
  const { data: allCharacters, isSuccess } = useGetCharactersQuery();

  const frontCharacters = useMemo(
    () =>
      allCharacters?.filter(
        (character) => character.range >= 100 && character.range < 300
      ),
    [allCharacters]
  );
  const midCharacters = useMemo(
    () =>
      allCharacters?.filter(
        (character) => character.range >= 300 && character.range < 600
      ),
    [allCharacters]
  );
  const backCharacters = useMemo(
    () =>
      allCharacters?.filter(
        (character) => character.range >= 600 && character.range < 900
      ),
    [allCharacters]
  );

  let content;

  if (isSuccess) {
    content = (
      <Tab.Group>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
          <Tab
            className={({ selected }) =>
              classNames(
                "w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700",
                "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2",
                selected
                  ? "bg-white shadow"
                  : "text-blue-100 hover:bg-white/[0.12] hover:text-white"
              )
            }
          >
            All
          </Tab>
          <Tab
            className={({ selected }) =>
              classNames(
                "w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700",
                "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2",
                selected
                  ? "bg-white shadow"
                  : "text-blue-100 hover:bg-white/[0.12] hover:text-white"
              )
            }
          >
            Front
          </Tab>
          <Tab
            className={({ selected }) =>
              classNames(
                "w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700",
                "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2",
                selected
                  ? "bg-white shadow"
                  : "text-blue-100 hover:bg-white/[0.12] hover:text-white"
              )
            }
          >
            Mid
          </Tab>
          <Tab
            className={({ selected }) =>
              classNames(
                "w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700",
                "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2",
                selected
                  ? "bg-white shadow"
                  : "text-blue-100 hover:bg-white/[0.12] hover:text-white"
              )
            }
          >
            Back
          </Tab>
        </Tab.List>
        <Tab.Panels>
          <Tab.Panel
            className={classNames(
              "rounded-xl bg-white",
              "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400"
            )}
          >
            {characterGrid(allCharacters, handleClick, selectedList)}
          </Tab.Panel>
          <Tab.Panel
            className={classNames(
              "rounded-xl bg-white",
              "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400"
            )}
          >
            {characterGrid(frontCharacters, handleClick, selectedList)}
          </Tab.Panel>
          <Tab.Panel
            className={classNames(
              "rounded-xl bg-white",
              "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400"
            )}
          >
            {characterGrid(midCharacters, handleClick, selectedList)}
          </Tab.Panel>
          <Tab.Panel
            className={classNames(
              "rounded-xl bg-white",
              "ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400"
            )}
          >
            {characterGrid(backCharacters, handleClick, selectedList)}
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    );
  } else {
    content = <div>Loading</div>;
  }

  return content;
}
