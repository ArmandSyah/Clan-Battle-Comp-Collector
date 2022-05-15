import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"


export const apiSlice = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({ 
        baseUrl: process.env.REACT_APP_API_SERVICE_URL,
        prepareHeaders: (headers) => {
            headers.set('Content-Type', 'application/json')

            return headers
        }
    }),
    tagTypes: ['ClanBattle'],
    endpoints: (builder) => ({
        getCharacters: builder.query({
            query: () => '/characters'
        }),
        getTeamComp: builder.query({
            query: (teamCompId) => `/teamcomp/${teamCompId}`
        }),
        addTeamComp: builder.mutation({
            query: (teamComp) => ({
                url: '/teamcomp',
                method: 'POST',
                body: teamComp
            }),
            invalidatesTags: ['ClanBattle']
        }),
        getLatestClanBattle: builder.query({
            query: () => '/clanbattle/latest',
            providesTags: ['ClanBattle']
        })
    })
});

export const {
    useGetCharactersQuery,
    useGetTeamCompQuery,
    useAddTeamCompMutation,
    useGetLatestClanBattleQuery
} = apiSlice