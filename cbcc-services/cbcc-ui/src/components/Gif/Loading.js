import React from "react";
import kokkoroLoading from "../../image/kokkomairimashou.gif";

export default function Loading() {
  return (
    <div className="flex flex-col items-center">
      <img src={kokkoroLoading} alt="Loading" />
      <span className="text-2xl text-stone-100">Kokkoro is on her way!</span>
    </div>
  );
}
