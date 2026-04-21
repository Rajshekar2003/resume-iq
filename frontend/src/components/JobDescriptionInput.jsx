export default function JobDescriptionInput({
  value,
  onChange,
  minChars = 50,
  maxChars = 20000,
  placeholder = "Paste the job description here…",
  disabled = false,
}) {
  const len = value.length;
  const tooShort = len > 0 && len < minChars;

  return (
    <div className="w-full">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        rows={8}
        maxLength={maxChars}
        disabled={disabled}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 resize-y focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
      />
      <div className="flex justify-between mt-1">
        {tooShort ? (
          <span className="text-xs text-amber-600">⚠ At least {minChars} characters required</span>
        ) : (
          <span className="text-xs text-gray-400" />
        )}
        <span className={`text-xs ${len > maxChars * 0.95 ? "text-amber-500" : "text-gray-400"}`}>
          {len} / {maxChars}
        </span>
      </div>
    </div>
  );
}
