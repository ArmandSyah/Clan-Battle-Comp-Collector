import React from "react";

export default function BossHeader({ bossName, icon }) {
  return (
    <div className="flex gap-2 items-end">
      <img
        src={icon}
        alt={`${bossName}-icon`}
        className="p-1 bg-black border rounded .max-w-full .h-auto"
      />
      <span className="text-stone-100 uppercase font-bold italic text-3xl truncate">
        {bossName}
      </span>
    </div>
  );
}
