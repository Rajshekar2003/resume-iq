const IMPORTANCE_ORDER = ["critical", "important", "nice-to-have"];

const IMPORTANCE_COLORS = {
  critical: "bg-red-100 text-red-700",
  important: "bg-blue-100 text-blue-700",
  "nice-to-have": "bg-gray-100 text-gray-700",
};

export default function KeywordPanel({ result }) {
  const keywords = result?.keywords ?? [];

  // Group by category preserving insertion order
  const grouped = keywords.reduce((acc, kw) => {
    const cat = kw.category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(kw);
    return acc;
  }, {});

  // Sort each group by importance
  Object.values(grouped).forEach((arr) => {
    arr.sort(
      (a, b) =>
        IMPORTANCE_ORDER.indexOf(a.importance) - IMPORTANCE_ORDER.indexOf(b.importance)
    );
  });

  const categories = Object.keys(grouped);

  if (!categories.length) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">No keywords extracted.</div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-5">
      <h2 className="text-lg font-semibold text-gray-800">Extracted Keywords</h2>

      {/* Legend */}
      <div className="flex flex-wrap gap-3 text-xs">
        <span className="px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-medium">critical</span>
        <span className="px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 font-medium">important</span>
        <span className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-700 font-medium">nice-to-have</span>
      </div>

      {categories.map((cat) => (
        <div key={cat}>
          <h3 className="text-sm font-semibold text-gray-700 capitalize mb-2">
            {cat} ({grouped[cat].length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {grouped[cat].map((kw, i) => (
              <span
                key={i}
                className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                  IMPORTANCE_COLORS[kw.importance] ?? "bg-gray-100 text-gray-700"
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
