import React, { useEffect, useState } from "react";
import { IoArrowBack, IoSettingsSharp } from "react-icons/io5";
import { Link, useLocation } from "react-router-dom";

import { useGetLatestClanBattleQuery } from "../../app/api/apiSlice";
import SettingsModal from "../SettingsModal/SettingsModal";

const convertDate = (date) =>
  new Date(date).toLocaleDateString("en", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

export default function NavBar() {
  const { data: clanBattleInfo, isSuccess } = useGetLatestClanBattleQuery();

  const location = useLocation();
  const [showBackButton, setShowBackButton] = useState(true);
  const [showSettings, setShowSettings] = useState(true);
  const [settingsModalIsOpen, setSettingsModalIsOpen] = useState(false);

  const closeModal = () => {
    setSettingsModalIsOpen(false);
  };

  const openModal = () => {
    setSettingsModalIsOpen(true);
  };

  useEffect(() => {
    var currentPath = location.pathname;
    setShowBackButton(currentPath !== "/clanBattle");
    setShowSettings(currentPath === "/clanBattle");
  }, [location]);

  let content;
  if (isSuccess) {
    content = (
      <>
        {showBackButton && (
          <Link to="/clanBattle">
            <IoArrowBack
              className="text-neutral-600 hover:text-neutral-700 self-center cursor-pointer"
              size={36}
            />
          </Link>
        )}
        <div className="text-2xl text-white font-bold self-center mx-auto flex flex-col text-center">
          <p>Clan Battle Period</p>
          <p>
            {convertDate(clanBattleInfo["main_start_date"])} -{" "}
            {convertDate(clanBattleInfo["main_end_date"])}
          </p>
        </div>
        {showSettings && (
          <IoSettingsSharp
            onClick={openModal}
            className="text-neutral-600 hover:text-neutral-700 self-center cursor-pointer"
            size={36}
          />
        )}
        <SettingsModal
          settingsModalIsOpen={settingsModalIsOpen}
          closeModal={closeModal}
        />
      </>
    );
  }

  return <nav className="bg-stone-900 h-20 p-5 flex">{content}</nav>;
}
