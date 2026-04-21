import { Loader2 } from "lucide-react";

function Skeleton() {
  return (
    <div className="space-y-3 animate-pulse py-4">
      <div className="h-4 bg-slate-200 rounded w-3/4" />
      <div className="h-4 bg-slate-200 rounded w-1/2" />
      <div className="h-4 bg-slate-200 rounded w-5/6" />
      <div className="h-4 bg-slate-200 rounded w-2/3" />
    </div>
  );
}

export default function LoadingSpinner({ label = "Loading...", variant }) {
  if (variant === "skeleton") return <Skeleton />;
  return (
    <div className="flex flex-col items-center gap-3 py-8">
      <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
      <span className="text-sm text-slate-500">{label}</span>
    </div>
  );
}
