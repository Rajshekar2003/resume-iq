import { useState } from "react";
import { analyzeResume } from "./lib/api";
import BulletImproverTool from "./components/BulletImproverTool";
import ResultsPanel from "./components/ResultsPanel";
import ResumeUpload from "./components/ResumeUpload";
import "./index.css";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [atsResult, setAtsResult] = useState(null);
  const [atsError, setAtsError] = useState(null);
  const [atsLoading, setAtsLoading] = useState(false);

  async function handleAnalyze() {
    if (!selectedFile) return;
    setAtsError(null);
    setAtsResult(null);
    setAtsLoading(true);
    try {
      const data = await analyzeResume(selectedFile);
      setAtsResult(data);
    } catch (err) {
      setAtsError(err);
    } finally {
      setAtsLoading(false);
    }
  }

  function handleFileSelected(file) {
    setSelectedFile(file);
    // Clear previous results when a new file is selected
    setAtsResult(null);
    setAtsError(null);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-3xl mx-auto px-4 py-5">
          <h1 className="text-2xl font-bold text-gray-900">AI Resume Analyzer</h1>
          <p className="text-sm text-gray-500 mt-1">
            ATS scoring, JD matching, bullet improvement, and market insights
          </p>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 py-8 space-y-8">
        {/* Upload + Analyze section */}
        <section className="space-y-4">
          <ResumeUpload
            onFileSelected={handleFileSelected}
            disabled={atsLoading}
          />
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || atsLoading}
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {atsLoading ? "Analyzing…" : "Analyze Resume"}
          </button>
        </section>

        {/* Results */}
        <ResultsPanel
          atsResult={atsResult}
          atsError={atsError}
          atsLoading={atsLoading}
          onDismissError={() => setAtsError(null)}
        />

        {/* Divider */}
        <hr className="border-gray-200" />

        {/* Bullet Improver — independent tool */}
        <section>
          <BulletImproverTool />
        </section>
      </main>
    </div>
  );
}
