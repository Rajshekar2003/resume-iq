import { Sparkles, Database, Atom } from "lucide-react";

const badges = [
  { icon: <Sparkles className="w-3.5 h-3.5" />, label: "Groq" },
  { icon: <Database className="w-3.5 h-3.5" />, label: "ChromaDB" },
  { icon: <Atom className="w-3.5 h-3.5" />, label: "React" },
];

export default function Hero() {
  return (
    <div className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 w-full">
      <div className="max-w-4xl mx-auto px-4 py-16 md:py-24 text-center">
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-slate-900">
          AI Resume Analyzer
        </h1>
        <p className="text-xl text-slate-600 max-w-2xl mx-auto mt-6 leading-relaxed">
          Production-grade resume analysis powered by LLMs and RAG. Get ATS scores,
          keyword gap analysis, and market insights from a vector database of real job
          descriptions.
        </p>
        <div className="flex flex-wrap justify-center gap-3 mt-8">
          {badges.map((b) => (
            <span
              key={b.label}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/70 border border-slate-200 text-slate-600 text-sm font-medium shadow-sm"
            >
              {b.icon}
              {b.label}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
