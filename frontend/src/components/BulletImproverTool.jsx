import { useState } from "react";
import { improveBullet } from "../lib/api";
import ErrorDisplay from "./ErrorDisplay";
import LoadingSpinner from "./LoadingSpinner";

const MIN = 10;
const MAX = 500;

export default function BulletImproverTool() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const data = await improveBullet(text.trim());
      setResult(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const tooShort = text.trim().length < MIN;
  const tooLong = text.length > MAX;
  const canSubmit = !tooShort && !tooLong && !loading;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-1">Bullet Point Improver</h2>
      <p className="text-sm text-gray-500 mb-4">Paste a resume bullet and get an AI-rewritten version with impact.</p>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g. Worked on the backend team to improve API performance"
            rows={3}
            maxLength={MAX}
            disabled={loading}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
          <div className="flex justify-between mt-1">
            <span className="text-xs text-gray-400">Min {MIN} characters</span>
            <span className={`text-xs ${tooLong ? "text-red-500" : "text-gray-400"}`}>
              {text.length} / {MAX}
            </span>
          </div>
        </div>

        <button
          type="submit"
          disabled={!canSubmit}
          className="w-full sm:w-auto px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Improve This Bullet
        </button>
      </form>

      {loading && <LoadingSpinner label="Rewriting bullet..." />}
      {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}

      {result && (
        <div className="mt-6 space-y-4">
          {/* Score */}
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-600">Impact Score:</span>
            <span className={`text-lg font-bold ${result.strength_score >= 7 ? "text-green-600" : result.strength_score >= 4 ? "text-amber-500" : "text-red-500"}`}>
              {result.strength_score} / 10
            </span>
          </div>

          {/* Side-by-side comparison */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Original</p>
              <p className="text-sm text-gray-700">{result.original}</p>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-xs font-semibold text-green-600 uppercase tracking-wide mb-2">Improved</p>
              <p className="text-sm text-gray-800">{result.improved}</p>
            </div>
          </div>

          {/* Changes */}
          <div>
            <p className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">Changes Made</p>
            <ul className="space-y-1">
              {result.changes_made.map((change, i) => (
                <li key={i} className="text-sm text-gray-700 flex gap-2">
                  <span className="text-blue-500 shrink-0">→</span>
                  <span>{change}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
