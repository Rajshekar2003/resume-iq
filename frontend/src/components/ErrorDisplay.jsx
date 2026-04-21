export default function ErrorDisplay({ error, onDismiss }) {
  const message = error instanceof Error ? error.message : String(error ?? "Unknown error");
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
      <span className="text-red-500 text-lg mt-0.5 shrink-0">✕</span>
      <p className="text-sm text-red-700 font-mono flex-1 break-words">{message}</p>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-red-400 hover:text-red-600 text-sm shrink-0 transition-colors"
        >
          Dismiss
        </button>
      )}
    </div>
  );
}
