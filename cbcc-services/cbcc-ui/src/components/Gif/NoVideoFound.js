import React from "react";
import kokkoroWoried from "../../image/kokkoworried.gif";

export default function NoVideoFound() {
  return (
    <div className="flex flex-col items-center">
      <img src={kokkoroWoried} alt="no video found" />
      <span className="text-2xl text-stone-100">
        Kokkoro couldn't find a video URL for this team comp, sorry
      </span>
    </div>
  );
}
