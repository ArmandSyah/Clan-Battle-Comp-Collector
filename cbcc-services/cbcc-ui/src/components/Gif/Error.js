import React from "react";
import pecoCry from "../../image/pecohuwaa.gif";

export default function Error() {
  return (
    <div className="flex flex-col items-center">
      <img src={pecoCry} alt="Error occured during page load" />
      <span className="text-2xl text-stone-100">Something went wrong.</span>
    </div>
  );
}
