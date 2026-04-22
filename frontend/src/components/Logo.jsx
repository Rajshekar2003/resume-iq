export default function Logo({ className = "" }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <svg
        width="36"
        height="36"
        viewBox="0 0 36 36"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="ResumeIQ logo"
      >
        <rect width="36" height="36" rx="8" fill="url(#logoGradient)" />
        <path
          d="M11 12H21M11 17H25M11 22H19"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <circle cx="26" cy="22" r="3.5" fill="white" />
        <defs>
          <linearGradient id="logoGradient" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
            <stop stopColor="#2563EB" />
            <stop offset="1" stopColor="#7C3AED" />
          </linearGradient>
        </defs>
      </svg>
      <span className="text-xl font-bold tracking-tight text-slate-900">
        Resume<span className="text-blue-600">IQ</span>
      </span>
    </div>
  );
}