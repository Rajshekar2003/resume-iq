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
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-gray-800">
          {matched_role_title || "Market Analysis"}
        </h2>
        <p className="text-sm text-gray-500 mt-0.5">
          Analyzed {jobs_analyzed} job{jobs_analyzed !== 1 ? "s" : ""}
          {avg_similarity_score != null && (
            <span className="ml-2 text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
              avg similarity {(avg_similarity_score * 100).toFixed(0)}%
            </span>
          )}
        </p>
      </div>

      {similarity_floor_triggered && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-amber-700 mb-1">⚠ Limited Market Match</p>
          <p className="text-sm text-amber-800">
            Few closely matching jobs were found in the database. The insights below are based on
            the closest available matches and may not fully reflect demand for this specific profile.
          </p>
        </div>
      )}

      {top_required_skills?.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-700">Top Required Skills</h3>
          <ul className="space-y-3">
            {top_required_skills.map((skill, i) => (
              <li key={i} className="border border-gray-100 rounded-lg p-4 space-y-2">
                <p className="text-sm text-gray-800">{skill.insight}</p>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                    {skill.evidence_count} / {jobs_analyzed || "?"} jobs
                  </span>
                  {skill.user_has_this ? (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-medium">
                      ✓ You have this
                    </span>
                  ) : (
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-medium">
                      ✗ Gap identified
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {candidate_gap_summary && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
          <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-1">💡 Summary</p>
          <p className="text-sm text-gray-800">{candidate_gap_summary}</p>
        </div>
      )}
    </div>
  );
}
