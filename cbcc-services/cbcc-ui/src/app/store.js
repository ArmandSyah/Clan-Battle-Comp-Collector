import { configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./api/apiSlice";
import settingsReducer from "./api/settingsSlice";

export const store = configureStore({
  reducer: {
    [apiSlice.reducerPath]: apiSlice.reducer,
    settings: settingsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});
