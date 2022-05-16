import React, { useMemo } from "react";
import { IoSettingsSharp } from "react-icons/io5";

import { useGetLatestClanBattleQuery } from "../../app/api/apiSlice";

const convertDate = (date) =>
  new Date(date).toLocaleDateString("en", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

export default function NavBar() {
  const {
    data: clanBattleInfo,
    isLoading,
    isFetching,
    isSuccess,
  } = useGetLatestClanBattleQuery();

  let content;
  if (isLoading || isFetching) {
    content = <div>Loading clan battle data</div>;
  } else if (isSuccess) {
    content = (
      <>
        <div className="text-2xl text-white font-bold self-center ml-auto flex flex-col text-center">
          <p>Clan Battle Period</p>
          <p>
            {convertDate(clanBattleInfo["main_start_date"])} -{" "}
            {convertDate(clanBattleInfo["main_end_date"])}
          </p>
        </div>
        <IoSettingsSharp
          className="text-neutral-600 hover:text-neutral-700 self-center ml-auto cursor-pointer"
          size={36}
        />
      </>
    );
  }

  return <nav className="bg-stone-900 h-20 p-5 flex">{content}</nav>;
}
