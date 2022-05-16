import React from "react";
import { MdAddCircleOutline } from "react-icons/md";

export default function ClanBattleRotationBoss({ unitName, icon, children }) {
  return (
    <div className="flex flex-col gap-9">
      <div className="flex gap-2 items-end">
        <img
          src={icon}
          alt={`${unitName}-icon`}
          className="p-1 bg-black border rounded .max-w-full .h-auto"
        />
        <span className="text-stone-100 uppercase font-bold italic text-3xl truncate">
          {unitName}
        </span>
      </div>
      {children}
      <button className="flex items-center justify-center h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400">
        <MdAddCircleOutline size={24} />
        <span className="font-semi-bold text-2xl">New Team Comp</span>
      </button>
    </div>
  );
}
