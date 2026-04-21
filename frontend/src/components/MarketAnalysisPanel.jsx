import { AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

export default function MarketAnalysisPanel({ result }) {
  const {
    matched_role_title,
    jobs_analyzed,
    avg_similarity_score,
    similarity_floor_triggered,
    top_required_skills,
    candidate_gap_summary,
  } = result;

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">
          {matched_role_title || "Market Analysis"}
        </h2>
        <p className="text-sm text-slate-500 mt-0.5 flex flex-wrap items-center gap-2">
          Analyzed {jobs_analyzed} similar job{jobs_analyzed !== 1 ? "s" : ""}
          {avg_similarity_score != null && (
            <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
              avg similarity {(avg_similarity_score * 100).toFixed(0)}%
            </span>
          )}
        </p>
      </div>

      {similarity_floor_triggered && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex gap-3">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-semibold text-amber-800 mb-1">Limited Market Match</p>
            <p className="text-sm text-amber-700">
              Few closely matching jobs were found in the database. Insights below are based on
              the closest available matches and may not fully represent demand for this profile.
            </p>
          </div>
        </div>
      )}

      {top_required_skills?.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Top Required Skills
          </h3>
          <ul className="space-y-2">
            {top_required_skills.map((skill, i) => (
              <li key={i} className="bg-slate-50 border border-slate-200 rounded-lg p-4">
                <div className="flex items-start justify-between gap-3">
                  <p className="text-sm text-slate-800 flex-1">{skill.insight}</p>
                  <span className="shrink-0 text-xs bg-slate-900 text-white rounded-full px-2 py-0.5 whitespace-nowrap">
                    {skill.evidence_count} / {jobs_analyzed || "?"} jobs
                  </span>
                </div>
                <div className="mt-2 flex items-center gap-1.5">
                  {skill.user_has_this ? (
                    <>
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      <span className="text-xs text-emerald-700 font-medium">You have this</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-4 h-4 text-red-500" />
                      <span className="text-xs text-red-700 font-medium">Gap identified</span>
                    </>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {candidate_gap_summary && (
        <div className="border-l-4 border-blue-500 pl-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">Summary</p>
          <p className="text-sm text-slate-700 italic">{candidate_gap_summary}</p>
        </div>
      )}
    </div>
  );
}
