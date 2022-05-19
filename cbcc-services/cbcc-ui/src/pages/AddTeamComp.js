import MDEditor from "@uiw/react-md-editor";
import { MdAddCircleOutline } from "react-icons/md";
import React, { useReducer } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import BossHeader from "../components/BossHeader/BossHeader";
import Input from "../components/Input/Input";
import ListboxComponent from "../components/ListboxComponent/ListboxComponent";
import TeamCompPreview from "../components/TeamCompPreview/TeamCompPreview";
import { useAddTeamCompMutation } from "../app/api/apiSlice";

const phases = [
  { id: 1, label: "Tier 1", value: 1 },
  { id: 2, label: "Tier 2", value: 2 },
  { id: 3, label: "Tier 3", value: 3 },
  { id: 4, label: "Tier 4", value: 4 },
  { id: 5, label: "Tier 5", value: 5 },
];

const playstyles = [
  { id: 1, label: "Auto", value: "auto" },
  { id: 2, label: "Semi", value: "semi" },
  { id: 3, label: "Manual", value: "manual" },
];

const actionTypes = {
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
  let characters;
  switch (action.type) {
    case actionTypes.FORMINPUT:
      return {
        ...state,
        [action.payload.key]: action.payload.value,
      };
    case actionTypes.ADDCHARACTER:
      const newCharacter = action.payload.value;
      const [firstCharacter, ...rest] = state.characters;
      characters = [...rest, newCharacter].sort((a, b) => b.range - a.range);
      return {
        ...state,
        characters,
      };
    case actionTypes.REMOVECHARACTER:
      const index = action.payload.index;
      const filteredCharacter = state.characters.filter(
        (_, characterIndex) => index !== characterIndex
      );
      characters = [initialCharacter, ...filteredCharacter].sort(
        (a, b) => b.range - a.range
      );
      return { ...state, characters };
    default:
      return state;
  }
};

export default function AddTeamComp() {
  const location = useLocation();
  const { bossId, bossName, icon } = location.state;
  const navigate = useNavigate();

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

  const deleteCharacter = (index) => () => {
    dispatch({
      type: actionTypes.REMOVECHARACTER,
      payload: { index },
    });
  };

  const [
    addNewTeamComp,
    { isLoading: addingTeamComp, isSuccess: teamCompAdded },
  ] = useAddTeamCompMutation();

  const canSave =
    state.characters.filter((character) => character.characterId !== 0).length >
    0;

  const onAddTeamCompClicked = async () => {
    if (canSave) {
      try {
        const characters = state.characters
          .filter((character) => character.characterId !== 0)
          .map((character) => {
            return {
              character_id: character.characterId,
              star: Number(character.star),
              rank: Number(character.rank),
              ue: Number(character.ue),
              level: Number(character.level),
              notes: character.notes,
            };
          });

        const teamComp = {
          ...state,
          boss_id: bossId,
          teamcomp_characters: characters,
          phase: state.phase.value,
          playstyle: state.playstyle.value,
          expected_damage: Number(state.expectedDamage),
        };
        await addNewTeamComp(teamComp).unwrap();
      } catch (err) {
        console.log("Failed to save team comp: ", err);
      }
    }
  };

  if (addingTeamComp) {
    return <div>"Loading Adding Team Comp"</div>;
  } else if (teamCompAdded) {
    console.log("Team comp has been added");
    return navigate("/clanBattle");
  }

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
    <div className="flex flex-col lg:grid lg:grid-col-2 gap-4 px-10 py-10">
      {teamCompInfo}
      <div className="justify-self-center">
        <TeamCompPreview
          characters={state.characters}
          addCharacterHandle={addCharacter}
          deleteCharacterHandle={deleteCharacter}
        />
      </div>
      <div className="lg:col-span-2">
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
      <div className="lg:col-span-2 justify-self-center">
        <button
          disabled={!canSave}
          onClick={onAddTeamCompClicked}
          type="button"
          className="flex items-center justify-center p-3 h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400"
        >
          <MdAddCircleOutline size={24} />
          <span className="font-semi-bold text-stone-900 text-2xl">
            Add Team Comp
          </span>
        </button>
      </div>
    </div>
  );
}
