import { Sparkles, Database, Atom } from "lucide-react";
import Logo from "./Logo";

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 pb-56">
      {/* Top nav with logo */}
      <div className="max-w-6xl mx-auto px-4 pt-6">
        <Logo />
      </div>

      {/* Hero content */}
      <div className="max-w-4xl mx-auto px-4 py-16 md:py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-slate-900 leading-[1.05]">
          See your resume the way{" "}
          <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            recruiter algorithms
          </span>{" "}
          do.
        </h1>

        <p className="text-lg text-slate-600 max-w-2xl mx-auto mt-6">
          ATS scoring, JD matching, and market intelligence powered by LLMs and a vector database of real job descriptions.
        </p>

        {/* Tech badges */}
        <div className="flex flex-wrap items-center justify-center gap-3 mt-8">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 rounded-full text-sm font-medium text-slate-700 shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-blue-500" />
            Groq
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 rounded-full text-sm font-medium text-slate-700 shadow-sm">
            <Database className="w-3.5 h-3.5 text-emerald-500" />
            ChromaDB
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 rounded-full text-sm font-medium text-slate-700 shadow-sm">
            <Atom className="w-3.5 h-3.5 text-cyan-500" />
            React
          </span>
        </div>

        {/* Stats bar — concrete proof of substance */}
        <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 mt-10 pt-6 border-t border-slate-200/60 max-w-2xl mx-auto">
          <Stat value="6" label="AI endpoints" />
          <Divider />
          <Stat value="53" label="JDs indexed" />
          <Divider />
          <Stat value="15" label="eval test cases" />
          <Divider />
          <Stat value="2-stage" label="RAG pipeline" />
        </div>
      </div>
    </div>
  );
}

function Stat({ value, label }) {
  return (
    <div className="text-center">
      <div className="text-2xl font-bold text-slate-900">{value}</div>
      <div className="text-xs uppercase tracking-wide text-slate-500 font-medium mt-0.5">
        {label}
      </div>
    </div>
  );
}

function Divider() {
  return <div className="hidden sm:block w-px h-8 bg-slate-200" />;
}