import React from "react";
import { MdAddCircleOutline } from "react-icons/md";
import { Link } from "react-router-dom";
import BossHeader from "../BossHeader/BossHeader";

export default function ClanBattleRotationBoss({
  bossId,
  bossName,
  icon,
  children,
}) {
  return (
    <div className="flex flex-col gap-9">
      <BossHeader bossName={bossName} icon={icon} />
      {children}
      <div className="justify-self-center">
        <Link
          to={{
            pathname: "/addTeamComp",
          }}
          state={{ bossId: bossId, bossName: bossName, icon: icon }}
        >
          <button className="flex items-center justify-center h-12 bg-stone-100 hover:bg-stone-300 rounded-3xl shadow-xl border-2 border-indigo-400">
            <MdAddCircleOutline size={24} />
            <span className="font-semi-bold text-2xl">New Team Comp</span>
          </button>
        </Link>
      </div>
    </div>
  );
}
