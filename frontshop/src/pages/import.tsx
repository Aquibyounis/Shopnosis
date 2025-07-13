import React from "react";
import { Button } from "@/components/ui/button";

export default function ImportSection({
  handleFileChange,
  handleUpload,
  selectedFiles,
  uploadStatus
}) {
  return (
    <div className="w-full px-12 flex flex-col items-center justify-center">
    <br />
    <h2 className="text-3xl font-black mb-8 w-full text-left text-blue-900">
      Import Product Data
    </h2>
    <div className="w-full max-w-4xl bg-white/80 rounded-xl shadow-lg p-12">
        <h3 className="text-2xl font-bold mb-4 text-blue-900 w-full text-left">Upload Product Data</h3>
        <p className="text-lg text-gray-600 mb-6 w-full text-left">
          Upload a CSV or Excel file.
        </p>
        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
          className="mb-4 w-full border-2 border-blue-200 rounded px-4 py-3 text-lg bg-white focus:border-blue-400 focus:outline-none"
          multiple
        />
        <Button
          className="w-full py-4 text-xl bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition font-bold"
          onClick={handleUpload}
          disabled={selectedFiles.length === 0}
          type="button"
        >
          Upload
        </Button>
        {uploadStatus && (
          <div className="mt-6 text-green-700 font-bold text-lg text-center w-full">{uploadStatus}</div>
        )}
      </div>
    </div>
  );
}
