import MDEditor from "@uiw/react-md-editor";
import React, { useReducer } from "react";
import { useLocation } from "react-router-dom";
import BossHeader from "../components/BossHeader/BossHeader";
import Input from "../components/Input/Input";
import ListboxComponent from "../components/ListboxComponent/ListboxComponent";
import TeamCompPreview from "../components/TeamCompPreview/TeamCompPreview";

const phases = [
  { id: 1, label: "Tier 1", value: 1 },
  { id: 2, label: "Tier 2", value: 2 },
  { id: 3, label: "Tier 3", value: 3 },
  { id: 4, label: "Tier 4", value: 4 },
  { id: 5, label: "Tier 5", value: 5 },
];

const playstyles = [
  { id: 1, label: "Auto", value: "Auto" },
  { id: 2, label: "Semi", value: "Semi" },
  { id: 3, label: "Manual", value: "Manual" },
];

const actionTypes = {
  PHASE: "PHASE",
  PLAYSTYLE: "PLAYSTYLE",
  NOTES: "NOTES",
  ADDCHARACTER: "ADDCHARACTER",
  REMOVECHARACTER: "REMOVECHARACTER",
  FORMINPUT: "FORMINPUT",
};

const initialState = {
  videoUrl: "",
  expectedDamage: 0,
  phase: phases[0],
  playstyle: playstyles[0],
  notes: "",
  characters: [
    {
      characterId: 0,
      icon: "",
      star: 0,
      rank: 0,
      ue: 0,
      level: 0,
      range: 0,
      notes: "",
    },
    {
      characterId: 0,
      icon: "",
      star: 0,
      rank: 0,
      ue: 0,
      level: 0,
      range: 0,
      notes: "",
    },
    {
      characterId: 0,
      icon: "",
      star: 0,
      rank: 0,
      ue: 0,
      level: 0,
      range: 0,
      notes: "",
    },
    {
      characterId: 0,
      icon: "",
      star: 0,
      rank: 0,
      ue: 0,
      level: 0,
      range: 0,
      notes: "",
    },
    {
      characterId: 0,
      icon: "",
      star: 0,
      rank: 0,
      ue: 0,
      level: 0,
      notes: "",
    },
  ],
};

const initialCharacter = {
  characterId: 0,
  icon: "",
  star: 0,
  rank: 0,
  ue: 0,
  level: 0,
  range: 0,
  notes: "",
};

const reducer = (state, action) => {
  switch (action.type) {
    case actionTypes.FORMINPUT:
      return {
        ...state,
        [action.payload.key]: action.payload.value,
      };
    case actionTypes.ADDCHARACTER:
      const newCharacter = action.payload.value;
      const [firstCharacter, ...rest] = state.characters;
      const characters = [...rest, newCharacter].sort(
        (a, b) => b.range - a.range
      );
      return {
        ...state,
        characters,
      };
    default:
      return state;
  }
};

export default function AddTeamComp() {
  const location = useLocation();
  const { bossId, bossName, icon } = location.state;

  const [state, dispatch] = useReducer(reducer, initialState);

  const handleChange = (key) => (event) =>
    dispatch({
      type: actionTypes.FORMINPUT,
      payload: { key, value: event.target.value },
    });

  const handleSelectChange = (key) => (value) =>
    dispatch({
      type: actionTypes.FORMINPUT,
      payload: { key, value },
    });

  const addCharacter = (character) => {
    dispatch({
      type: actionTypes.ADDCHARACTER,
      payload: { value: character },
    });
  };

  const teamCompInfo = (
    <div className="flex flex-col gap-2 mb-3 xl:w-96 justify-self-center">
      <BossHeader bossName={bossName} icon={icon} />
      <Input
        id="videoUrlInput"
        label="Video URL"
        type="url"
        value={state.videoUrl}
        handleChange={handleChange("videoUrl")}
      />
      <Input
        id="expectedDamageInput"
        label="Damage"
        type="number"
        value={state.expectedDamage}
        handleChange={handleChange("expectedDamage")}
      />
      <ListboxComponent
        label="Tier"
        value={state.phase}
        options={phases}
        handleChange={handleSelectChange("phase")}
      />
      <ListboxComponent
        label="Playstyle"
        value={state.playstyle}
        options={playstyles}
        handleChange={handleSelectChange("playstyle")}
      />
    </div>
  );

  return (
    <div className="grid grid-cols-2 grid-rows-2 gap-4 px-10 py-10">
      {teamCompInfo}
      <div className="justify-self-center">
        <TeamCompPreview
          characters={state.characters}
          addCharacterHandle={addCharacter}
        />
      </div>
      <div className="col-span-2">
        <div className="grid justify-items-center items-center">
          <div className="container flex flex-col gap-4">
            <label className="form-label inline-block text-stone-100 text-2xl font-semibold">
              Notes
            </label>
            <MDEditor
              value={state.notes}
              onChange={handleSelectChange("notes")}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
