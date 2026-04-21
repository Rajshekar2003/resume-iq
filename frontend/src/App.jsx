import { useState } from "react";
import { analyzeResume, matchJobDescription, extractKeywords, analyzeMarket } from "./lib/api";
import BulletImproverTool from "./components/BulletImproverTool";
import ResumeUpload from "./components/ResumeUpload";
import TabNav from "./components/TabNav";
import JobDescriptionInput from "./components/JobDescriptionInput";
import AtsScoreCard from "./components/AtsScoreCard";
import JdMatchPanel from "./components/JdMatchPanel";
import KeywordPanel from "./components/KeywordPanel";
import MarketAnalysisPanel from "./components/MarketAnalysisPanel";
import ErrorDisplay from "./components/ErrorDisplay";
import LoadingSpinner from "./components/LoadingSpinner";
import "./index.css";

const TABS = [
  { id: "ats", label: "ATS Analysis" },
  { id: "match", label: "JD Match" },
  { id: "keywords", label: "Keyword Extractor" },
  { id: "market", label: "Market Insights" },
];

function NoFileNotice() {
  return (
    <p className="text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
      ⚠ Upload a resume above first.
    </p>
  );
}

function AtsTab({ file }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleAnalyze() {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      setResult(await analyzeResume(file));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  if (!file) return <NoFileNotice />;

  return (
    <div className="space-y-4">
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Analyzing…" : "Analyze Resume"}
      </button>
      {loading && <LoadingSpinner label="Analyzing resume…" />}
      {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}
      {result && <AtsScoreCard result={result} />}
      {!loading && !result && !error && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-3">📋</p>
          <p className="text-sm">Click Analyze Resume to get your ATS score.</p>
        </div>
      )}
    </div>
  );
}

function JdMatchTab({ file }) {
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  if (!file) return <NoFileNotice />;

  async function handleMatch() {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      setResult(await matchJobDescription(file, jd));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const canSubmit = jd.trim().length >= 50 && !loading;

  return (
    <div className="space-y-4">
      <JobDescriptionInput
        value={jd}
        onChange={setJd}
        placeholder="Paste the job description here…"
        disabled={loading}
      />
      <button
        onClick={handleMatch}
        disabled={!canSubmit}
        className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Matching…" : "Match JD"}
      </button>
      {loading && <LoadingSpinner label="Matching job description…" />}
      {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}
      {result && <JdMatchPanel result={result} />}
    </div>
  );
}

function KeywordsTab() {
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleExtract() {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      setResult(await extractKeywords(jd));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  const canSubmit = jd.trim().length >= 50 && !loading;

  return (
    <div className="space-y-4">
      <JobDescriptionInput
        value={jd}
        onChange={setJd}
        placeholder="Paste a job description to extract keywords…"
        disabled={loading}
      />
      <button
        onClick={handleExtract}
        disabled={!canSubmit}
        className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Extracting…" : "Extract Keywords"}
      </button>
      {loading && <LoadingSpinner label="Extracting keywords…" />}
      {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}
      {result && <KeywordPanel result={result} />}
    </div>
  );
}

function MarketTab({ file }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  if (!file) return <NoFileNotice />;

  async function handleAnalyze() {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      setResult(await analyzeMarket(file));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Analyzing…" : "Analyze Market"}
      </button>
      {loading && <LoadingSpinner label="Fetching market insights…" />}
      {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}
      {result && <MarketAnalysisPanel result={result} />}
      {!loading && !result && !error && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-3">📊</p>
          <p className="text-sm">Click Analyze Market to see how your resume positions in the job market.</p>
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeTab, setActiveTab] = useState("ats");

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-3xl mx-auto px-4 py-5">
          <h1 className="text-2xl font-bold text-gray-900">AI Resume Analyzer</h1>
          <p className="text-sm text-gray-500 mt-1">
            ATS scoring, JD matching, keyword extraction, and market insights
          </p>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8 space-y-6">
        {/* Resume upload — hidden on Keywords tab since it doesn't need a file */}
        {activeTab !== "keywords" && (
          <ResumeUpload
            onFileSelected={setSelectedFile}
            persistMessage="This resume will be used for: ATS Analysis, JD Match, and Market Insights."
          />
        )}

        <TabNav tabs={TABS} activeTab={activeTab} onTabChange={setActiveTab} />

        <div>
          {activeTab === "ats" && <AtsTab file={selectedFile} />}
          {activeTab === "match" && <JdMatchTab file={selectedFile} />}
          {activeTab === "keywords" && <KeywordsTab />}
          {activeTab === "market" && <MarketTab file={selectedFile} />}
        </div>

        <hr className="border-gray-200" />

        <section>
          <BulletImproverTool />
        </section>
      </main>
    </div>
  );
}
