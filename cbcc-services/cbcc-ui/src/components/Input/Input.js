import React from "react";

export default function Input({
  id,
  label,
  value,
  type,
  handleChange,
  disabled,
}) {
  return (
    <div>
      <label
        htmlFor={id}
        className="form-label inline-block mb-2 text-stone-100 text-2xl font-semibold"
      >
        {label}
      </label>
      <input
        className={`input-main ${
          disabled ? "text-stone-100 bg-gray-700 bg-clip-padding" : ""
        }`}
        value={value}
        onChange={handleChange}
        type={type}
        id={id}
        disabled={disabled}
        onWheel={(e) => e.target.blur()}
      />
    </div>
  );
}
