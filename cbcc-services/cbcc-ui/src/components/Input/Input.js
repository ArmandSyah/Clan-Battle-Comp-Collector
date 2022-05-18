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
        for={id}
        className="form-label inline-block mb-2 text-stone-100 text-2xl font-semibold"
      >
        {label}
      </label>
      <input
        className={`input-main ${
          disabled ? "text-gray-700 bg-gray-100 bg-clip-padding" : ""
        }`}
        value={value}
        onChange={handleChange}
        type={type}
        id={id}
        disabled={disabled}
      />
    </div>
  );
}
