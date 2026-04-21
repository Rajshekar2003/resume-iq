const IMPORTANCE_ORDER = ["critical", "important", "nice-to-have"];

const PILL_CLASSES = {
  critical: "bg-rose-50 text-rose-700 border border-rose-200",
  important: "bg-blue-50 text-blue-700 border border-blue-200",
  "nice-to-have": "bg-slate-50 text-slate-600 border border-slate-200",
};

export default function KeywordPanel({ result }) {
  const keywords = result?.keywords ?? [];

  const grouped = keywords.reduce((acc, kw) => {
    const cat = kw.category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(kw);
    return acc;
  }, {});

  Object.values(grouped).forEach((arr) => {
    arr.sort(
      (a, b) =>
        IMPORTANCE_ORDER.indexOf(a.importance) - IMPORTANCE_ORDER.indexOf(b.importance)
    );
  });

  const categories = Object.keys(grouped);

  if (!categories.length) {
    return (
      <div className="text-center py-8 text-slate-400 text-sm">No keywords extracted.</div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-800">Extracted Keywords</h2>
        <div className="flex flex-wrap gap-2 text-xs">
          <span className="px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200 font-medium">critical</span>
          <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-medium">important</span>
          <span className="px-2 py-0.5 rounded-full bg-slate-50 text-slate-600 border border-slate-200 font-medium">nice-to-have</span>
        </div>
      </div>

      {categories.map((cat) => (
        <div key={cat}>
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 capitalize mb-2">
            {cat} ({grouped[cat].length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {grouped[cat].map((kw, i) => (
              <span
                key={i}
                className={`px-3 py-1 rounded-full text-xs font-medium ${
                  PILL_CLASSES[kw.importance] ?? PILL_CLASSES["nice-to-have"]
                }`}
              >
                {kw.keyword}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
