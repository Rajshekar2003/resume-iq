import { FileText, Target, KeyRound, TrendingUp } from "lucide-react";

const ICONS = {
  ats: <FileText className="w-4 h-4" />,
  match: <Target className="w-4 h-4" />,
  keywords: <KeyRound className="w-4 h-4" />,
  market: <TrendingUp className="w-4 h-4" />,
};

export default function TabNav({ tabs, activeTab, onTabChange }) {
  return (
    <div className="border-b border-slate-200 pb-1 mb-2">
    <div className="flex flex-wrap gap-2" role="tablist">
      {tabs.map((tab) => {
        const isActive = tab.id === activeTab;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            onClick={() => onTabChange(tab.id)}
            onKeyDown={(e) => { if (e.key === "Enter") onTabChange(tab.id); }}
            className={[
              "inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400",
              isActive
                ? "bg-blue-600 text-white shadow-md"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200",
            ].join(" ")}
          >
            {ICONS[tab.id]}
            {tab.label}
          </button>
        );
      })}
    </div>
    </div>
  );
}
