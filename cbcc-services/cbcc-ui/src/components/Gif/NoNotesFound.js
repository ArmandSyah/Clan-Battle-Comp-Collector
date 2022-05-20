import React from "react";
import kyaruWhy from "../../image/kyarunandeyoo.gif";

export default function NoNotesfound() {
  return (
    <div className="flex flex-col items-center">
      <img src={kyaruWhy} alt="no video found" />
      <span className="text-2xl text-stone-100">
        Kyaru lost the timeline and notes for this team comp, whoops
      </span>
    </div>
  );
}
