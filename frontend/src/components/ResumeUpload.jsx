import { useRef, useState } from "react";
import { Upload, FileText, Trash2 } from "lucide-react";

const ACCEPTED = [".pdf", ".docx"];
const ACCEPTED_MIME = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

function isValidFile(file) {
  return ACCEPTED_MIME.includes(file.type) || ACCEPTED.some((ext) => file.name.endsWith(ext));
}

export default function ResumeUpload({ onFileSelected, disabled, persistMessage }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  function handleFile(file) {
    if (!file) return;
    if (!isValidFile(file)) {
      setValidationError("Only PDF and DOCX files are accepted.");
      return;
    }
    setValidationError(null);
    setSelectedFile(file);
    onFileSelected(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);
    if (disabled) return;
    handleFile(e.dataTransfer.files[0]);
  }

  function handleChange(e) {
    handleFile(e.target.files[0]);
    e.target.value = "";
  }

  function handleClear() {
    setSelectedFile(null);
    setValidationError(null);
    onFileSelected(null);
  }

  const sizeKb = selectedFile ? (selectedFile.size / 1024).toFixed(1) : null;

  return (
    <div className="w-full">
      <div
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); if (!disabled) setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={[
          "border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer select-none",
          dragging ? "border-blue-400 bg-blue-50" : "border-slate-300 hover:border-blue-400 hover:bg-blue-50/50",
          disabled ? "opacity-50 cursor-not-allowed pointer-events-none" : "",
        ].join(" ")}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleChange}
          className="hidden"
          disabled={disabled}
        />

        {selectedFile ? (
          <div className="flex flex-col items-center gap-2">
            <FileText className="w-10 h-10 text-blue-500" />
            <p className="font-semibold text-slate-800 text-sm break-all">{selectedFile.name}</p>
            <p className="text-xs text-slate-500">{sizeKb} KB</p>
            <button
              onClick={(e) => { e.stopPropagation(); handleClear(); }}
              className="mt-1 inline-flex items-center gap-1 text-xs text-red-500 hover:text-red-700 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Remove
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2 text-slate-500">
            <Upload className="w-10 h-10 text-slate-400" />
            <p className="text-sm font-medium">Drop your resume here or click to browse</p>
            <p className="text-xs text-slate-400">PDF or DOCX, any size</p>
          </div>
        )}
      </div>

      {validationError && (
        <p className="mt-2 text-xs text-red-600">{validationError}</p>
      )}
      {persistMessage && (
        <p className="mt-2 text-xs text-slate-400">{persistMessage}</p>
      )}
    </div>
  );
}
