import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

export default function LoadingSpinner({ label = "Loading...", variant = "default" }) {
  const [stage, setStage] = useState(0);

  useEffect(() => {
    if (variant !== "progressive") return;
    const t1 = setTimeout(() => setStage(1), 5000);
    const t2 = setTimeout(() => setStage(2), 15000);
    const t3 = setTimeout(() => setStage(3), 45000);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, [variant]);

  const messages = variant === "progressive" ? [
    label,
    "Running AI analysis...",
    "Server is waking up — first request can take up to 60 seconds. Hang tight...",
    "Almost there — finalizing results..."
  ] : [label];

  const currentMessage = messages[stage] || messages[0];

  return (
    <div className="flex flex-col items-center gap-3 py-8">
      <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
      <span className="text-sm text-slate-600 text-center max-w-md px-4">
        {currentMessage}
      </span>
      {variant === "progressive" && stage >= 1 && (
        <div className="w-48 h-1 bg-slate-200 rounded-full overflow-hidden">
          <div className="h-full bg-blue-500 animate-pulse" style={{
            width: stage === 1 ? "30%" : stage === 2 ? "60%" : "90%",
            transition: "width 0.5s ease-out"
          }} />
        </div>
      )}
    </div>
  );
}
