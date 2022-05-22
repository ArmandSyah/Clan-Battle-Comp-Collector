import React from "react";
import { TierPlaystyle } from "../components/Badges/Badges";
import BossHeader from "../components/BossHeader/BossHeader";
import { useGetTeamCompQuery } from "../app/api/apiSlice";
import { useLocation, useParams } from "react-router-dom";
import ReactPlayer from "react-player";
import MDEditor from "@uiw/react-md-editor";
import { Disclosure } from "@headlessui/react";
import { IoChevronUp } from "react-icons/io5";
import NoVideoFound from "../components/Gif/NoVideoFound";
import NoNotesfound from "../components/Gif/NoNotesFound";
import Loading from "../components/Gif/Loading";
import Error from "../components/Gif/Error";

const isValidUrl = (possibleUrl) => {
  let url;

  try {
    url = new URL(possibleUrl);
  } catch (_) {
    return false;
  }

  return url.protocol === "http:" || url.protocol === "https:";
};

const createChracterDisplay = (teamCompCharacter) => {
  const {
    star,
    rank,
    ue,
    level,
    notes,
    icon,
    unit_name_en: unitName,
    thematic_en: thematic,
  } = teamCompCharacter;

  return (
    <Disclosure key={unitName}>
      {({ open }) => (
        <>
          <Disclosure.Button className="flex justify-between rounded-lg bg-slate-500 px-2 py-1 text-left font-semibold text-stone-100 hover:bg-slate-800 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75">
            <span className="flex w-full items-center">
              <img
                src={icon}
                className="p-0.5 bg-black border rounded object-contain relative"
                alt={unitName}
              />{" "}
              <span className="ml-2 text-2xl">
                {unitName} {thematic ? `(${thematic})` : ""}
              </span>
              <IoChevronUp
                className={`${
                  open ? "rotate-180 transform" : ""
                } h-5 w-5 text-stone-100 ml-auto`}
              />
            </span>
          </Disclosure.Button>
          <Disclosure.Panel className="flex flex-col px-4 pt-4 pb-2 text-lg text-stone-100">
            <div>Star: {star ? star : "-"}</div>
            <div>Rank: {rank ? rank : "-"}</div>
            <div>Level: {level ? level : "-"}</div>
            <div>UE: {ue ? ue : "-"}</div>
            <div>Notes: {notes ? notes : "-"}</div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};

const createTeamCompDisplay = (teamCompCharacters) => {
  return (
    <div className="flex flex-col rounded-2xl bg-slate-900 p-2 gap-4">
      {teamCompCharacters.map(createChracterDisplay)}
    </div>
  );
};

export default function ViewTeamComp() {
  const { teamCompId } = useParams();
  const location = useLocation();
  const { bossName, icon } = location.state;

  const {
    data: teamComp,
    isFetching,
    isLoading,
    isSuccess,
  } = useGetTeamCompQuery(teamCompId);

  if (isSuccess) {
    const {
      video_url: videoUrl,
      expected_damage: expectedDamage,
      notes,
      phase,
      playstyle,
      team_comp_characters: teamCompCharacters,
    } = teamComp;

    const TeamCompInfo = (
      <div className="grid grid-cols-2 gap-4 content-center">
        <div className="flex flex-col text-stone-100 text-3xl">
          <div className="bg-sky-600 rounded-xl text-center px-6 py-1">
            Expected Damage
          </div>
          <span className="drop-shadow-xl">{expectedDamage}</span>
        </div>
        <div className="w-1/2">{TierPlaystyle(phase, playstyle)}</div>
      </div>
    );

    const video = <ReactPlayer url={videoUrl} controls={true} width="100%" />;

    const NotesSection = (
      <MDEditor.Markdown
        source={notes}
        className="max-h-96 overflow-auto"
        linkTarget="_blank"
      />
    );

    const TeamComp = createTeamCompDisplay(teamCompCharacters);

    return (
      <div className="flex flex-col lg:grid lg:grid-cols-2 gap-4 p-8">
        <BossHeader bossName={bossName} icon={icon} />
        {TeamCompInfo}
        <div className="flex flex-col gap-4">
          {isValidUrl(videoUrl) ? video : <NoVideoFound />}
          {TeamComp}
        </div>
        {notes ? NotesSection : <NoNotesfound />}
      </div>
    );
  } else if (isFetching || isLoading) {
    return (
      <div className="absolute top-2/4 left-2/4">
        <Loading />
      </div>
    );
  }
  return (
    <div className="absolute top-2/4 left-2/4">
      <Error />
    </div>
  );
}
