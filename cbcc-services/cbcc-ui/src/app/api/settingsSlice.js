import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  missingCharacterIds: [],
  playstyle: "all",
};

const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    addMissingCharacter: (state, action) => {
      state.missingCharacterIds.push(action.payload.characterId);
    },
    removeMissingCharacter: (state, action) => {
      state.missingCharacterIds = state.missingCharacterIds.filter(
        (missingCharacterId) =>
          missingCharacterId !== action.payload.characterId
      );
    },
    changePlaystyle: (state, action) => {
      state.playstyle = action.payload.playstyle;
    },
  },
});

export const { addMissingCharacter, removeMissingCharacter, changePlaystyle } =
  settingsSlice.actions;

export default settingsSlice.reducer;
