import AtsScoreCard from "./AtsScoreCard";
import ErrorDisplay from "./ErrorDisplay";
import LoadingSpinner from "./LoadingSpinner";

export default function ResultsPanel({ atsResult, atsError, atsLoading, onDismissError }) {
  if (atsLoading) return <LoadingSpinner label="Analyzing resume..." />;
  if (atsError) return <ErrorDisplay error={atsError} onDismiss={onDismissError} />;
  if (atsResult) return <AtsScoreCard result={atsResult} />;

  return (
    <div className="text-center py-12 text-gray-400">
      <p className="text-4xl mb-3">📋</p>
      <p className="text-sm">Upload a resume and click Analyze to get started</p>
    </div>
  );
}
