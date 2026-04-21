function ScoreCircle({ score }) {
  // CSS-only circular progress using conic-gradient
  const color = score >= 70 ? "#16a34a" : score >= 50 ? "#d97706" : "#dc2626";
  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className="w-28 h-28 rounded-full flex items-center justify-center text-white font-bold text-2xl"
        style={{
          background: `conic-gradient(${color} ${score * 3.6}deg, #e5e7eb ${score * 3.6}deg)`,
        }}
      >
        <div className="w-20 h-20 rounded-full bg-white flex items-center justify-center">
          <span className="font-bold text-2xl" style={{ color }}>{score}</span>
        </div>
      </div>
      <span className="text-xs text-gray-500 font-medium uppercase tracking-wide">ATS Score</span>
    </div>
  );
}

function ListSection({ icon, title, items, itemClass }) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-2">{icon} {title}</h3>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className={`text-sm flex gap-2 ${itemClass}`}>
            <span className="shrink-0 mt-0.5">{icon}</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function AtsScoreCard({ result }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-5">ATS Analysis</h2>
      <div className="flex flex-col md:flex-row gap-8">
        {/* Score column */}
        <div className="flex justify-center md:justify-start md:items-start pt-1 shrink-0">
          <ScoreCircle score={result.score} />
        </div>

        {/* Details column */}
        <div className="flex flex-col gap-5 flex-1 min-w-0">
          <ListSection
            icon="✓"
            title="Strengths"
            items={result.strengths}
            itemClass="text-green-700"
          />
          <ListSection
            icon="⚠"
            title="Weaknesses"
            items={result.weaknesses}
            itemClass="text-amber-700"
          />
          <ListSection
            icon="💡"
            title="ATS Tips"
            items={result.ats_tips}
            itemClass="text-blue-700"
          />
        </div>
      </div>
    </div>
  );
}
