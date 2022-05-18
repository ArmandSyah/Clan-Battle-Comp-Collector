import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  missingCharacterIds: [],
  sortBy: "",
  showOnly: "All",
};

const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    addMissingCharacter: (state, action) => {
      state.missingCharacterIds.push(action.payload);
    },
    removeMissingCharacter: (state, action) => {
      state.missingCharacterIds = state.missingCharacterIds.filter(
        (missingCharacterId) => missingCharacterId !== action.payload
      );
    },
    changeSort: (state, action) => {
      state.sortBy = action.payload;
    },
    changeShowOnly: (state, action) => {
      state.showOnly = action.payload;
    },
  },
});

export const {
  addMissingCharacter,
  removeMissingCharacter,
  changeSort,
  changeShowOnly,
} = settingsSlice.actions;

export default settingsSlice.reducer;
