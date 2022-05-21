import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_SERVICE_URL,
    prepareHeaders: (headers) => {
      headers.set("Content-Type", "application/json");

      return headers;
    },
  }),
  tagTypes: ["ClanBattle", "TeamComp"],
  endpoints: (builder) => ({
    getCharacters: builder.query({
      query: () => "/characters",
    }),
    getCharacter: builder.query({
      query: (unitId) => `/characters/${unitId}`,
    }),
    getTeamComp: builder.query({
      query: (teamCompId) => `/teamcomp/${teamCompId}`,
      transformResponse: (responseData) => {
        const teamCompCharacters = responseData["team_comp_characters"].map(
          (teamCompCharacter) => {
            const { character: specificCharacterInfo, ...rest } =
              teamCompCharacter;
            return {
              ...rest,
              ...specificCharacterInfo,
            };
          }
        );

        return {
          ...responseData,
          team_comp_characters: teamCompCharacters,
        };
      },
      providesTags: (result, error, arg) => [{ type: "TeamComp", id: arg }],
    }),
    addTeamComp: builder.mutation({
      query: (teamComp) => ({
        url: "/teamcomp",
        method: "POST",
        body: teamComp,
      }),
      invalidatesTags: ["ClanBattle", "TeamComp"],
    }),
    updateTeamComp: builder.mutation({
      query: ({ teamCompId, ...data }) => {
        const teamComp = data["teamComp"];
        return {
          url: `/teamcomp/${teamCompId}`,
          method: "PUT",
          body: teamComp,
        };
      },
      invalidatesTags: (result, error, arg) => [
        "ClanBattle",
        { type: "TeamComp", id: arg.teamCompId },
      ],
    }),
    deleteTeamComp: builder.mutation({
      query: (teamCompId) => ({
        url: `/teamcomp/${teamCompId}`,
        method: "DELETE",
      }),
      invalidatesTags: ["ClanBattle", "TeamComp"],
    }),
    getLatestClanBattle: builder.query({
      query: () => "/clanbattle/latest",
      providesTags: ["ClanBattle"],
    }),
  }),
});

export const {
  useGetCharactersQuery,
  useGetCharacterQuery,
  useGetTeamCompQuery,
  useAddTeamCompMutation,
  useUpdateTeamCompMutation,
  useDeleteTeamCompMutation,
  useGetLatestClanBattleQuery,
} = apiSlice;
