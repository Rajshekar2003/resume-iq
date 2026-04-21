import { CheckCircle2, AlertCircle, Lightbulb } from "lucide-react";

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
      <span className="text-xs text-slate-500 font-medium uppercase tracking-wide">Match</span>
    </div>
  );
}

function PillList({ keywords, pillClass }) {
  if (!keywords?.length) return <p className="text-xs text-slate-400 italic">None</p>;
  return (
    <div className="flex flex-wrap gap-2">
      {keywords.map((kw, i) => (
        <span key={i} className={`px-3 py-1 rounded-full text-xs font-medium border ${pillClass}`}>
          {kw}
        </span>
      ))}
    </div>
  );
}

export default function JdMatchPanel({ result }) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-5">
      <h2 className="text-lg font-semibold text-slate-800">JD Match Results</h2>

      <div className="flex flex-col md:flex-row gap-8">
        <div className="flex justify-center md:justify-start md:items-start pt-1">
          <ScoreCircle score={result.match_percentage} />
        </div>

        <div className="flex flex-col gap-4 flex-1 min-w-0">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Matched Skills ({result.matched_keywords?.length ?? 0})
            </h3>
            <PillList
              keywords={result.matched_keywords}
              pillClass="bg-emerald-50 text-emerald-700 border-emerald-200"
            />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2 flex items-center gap-1.5">
              <AlertCircle className="w-4 h-4 text-amber-500" />
              Missing Skills ({result.missing_keywords?.length ?? 0})
            </h3>
            <PillList
              keywords={result.missing_keywords}
              pillClass="bg-amber-50 text-amber-700 border-amber-200"
            />
          </div>
        </div>
      </div>

      {result.recommendation && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex gap-3">
          <Lightbulb className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
          <p className="text-sm text-slate-700">{result.recommendation}</p>
        </div>
      )}
    </div>
  );
}
