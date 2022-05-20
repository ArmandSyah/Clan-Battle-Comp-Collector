import React from "react";
import kokoStamp from "../../image/kokkostamp.gif";

export default function AddingTeamComp() {
  return (
    <div className="flex flex-col items-center">
      <img src={kokoStamp} alt="no video found" />
      <span className="text-2xl text-stone-100">
        Kokkoro is submitting the team comp to the guild
      </span>
    </div>
  );
}
