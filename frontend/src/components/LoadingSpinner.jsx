export default function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="flex flex-col items-center gap-3 py-8">
      <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
      <span className="text-sm text-gray-500">{label}</span>
    </div>
  );
}
