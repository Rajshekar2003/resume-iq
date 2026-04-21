function ScoreCircle({ score }) {
  const color = score >= 70 ? "#16a34a" : score >= 50 ? "#d97706" : "#dc2626";
  return (
    <div className="flex flex-col items-center gap-2 shrink-0">
      <div
        className="w-28 h-28 rounded-full flex items-center justify-center"
        style={{
          background: `conic-gradient(${color} ${score * 3.6}deg, #e5e7eb ${score * 3.6}deg)`,
        }}
      >
        <div className="w-20 h-20 rounded-full bg-white flex items-center justify-center">
          <span className="font-bold text-2xl" style={{ color }}>{score}%</span>
        </div>
      </div>
      <span className="text-xs text-gray-500 font-medium uppercase tracking-wide">Match</span>
    </div>
  );
}

function PillList({ keywords, colorClass }) {
  if (!keywords?.length) return <p className="text-xs text-gray-400 italic">None</p>;
  return (
    <div className="flex flex-wrap gap-2">
      {keywords.map((kw, i) => (
        <span key={i} className={`px-2 py-0.5 rounded-full text-xs font-medium ${colorClass}`}>
          {kw}
        </span>
      ))}
    </div>
  );
}

export default function JdMatchPanel({ result }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-5">
      <h2 className="text-lg font-semibold text-gray-800">JD Match Results</h2>

      <div className="flex flex-col md:flex-row gap-8">
        {/* Score on left (desktop) */}
        <div className="flex justify-center md:justify-start md:items-start pt-1">
          <ScoreCircle score={result.match_percentage} />
        </div>

        {/* Keywords on right */}
        <div className="flex flex-col gap-4 flex-1 min-w-0">
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              ✓ Matched Keywords ({result.matched_keywords?.length ?? 0})
            </h3>
            <PillList keywords={result.matched_keywords} colorClass="bg-green-100 text-green-700" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              ⚠ Missing Keywords ({result.missing_keywords?.length ?? 0})
            </h3>
            <PillList keywords={result.missing_keywords} colorClass="bg-amber-100 text-amber-700" />
          </div>
        </div>
      </div>

      {/* Recommendation full-width */}
      {result.recommendation && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
          <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-1">💡 Recommendation</p>
          <p className="text-sm text-gray-800">{result.recommendation}</p>
        </div>
      )}
    </div>
  );
}
