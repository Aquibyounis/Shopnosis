import React from "react";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

export default function HistorySection({
  multiDeleteMode,
  setMultiDeleteMode,
  selectedForDelete,
  setSelectedForDelete,
  handleMultiDelete,
  handleDeleteFile,
  handleSelectAll,
  sortAsc,
  setSortAsc,
  sortedFiles
}) {
  return (
    <div className="w-full px-12 flex flex-col items-center justify-center">
  <br />
  <h2 className="text-3xl font-black mb-4 w-full text-left text-blue-900">
    Import History
  </h2>
  <div className="w-full bg-white rounded-2xl shadow-lg p-12">
    <div className="mb-4 flex items-center gap-4">
          <Button
            variant={multiDeleteMode ? "destructive" : "outline"}
            onClick={() => {
              setMultiDeleteMode(!multiDeleteMode);
              setSelectedForDelete([]);
            }}
          >
            {multiDeleteMode ? "Cancel Multi Delete" : "Select Multiple"}
          </Button>
          {multiDeleteMode && (
            <Button
              variant="destructive"
              onClick={handleMultiDelete}
              disabled={selectedForDelete.length === 0}
            >
              Delete Selected
            </Button>
          )}
        </div>
        <div className="mb-6 w-full overflow-x-auto">
          {sortedFiles.length === 0 ? (
            <p className="text-gray-600 text-lg">No files uploaded yet.</p>
          ) : (
            <table className="min-w-full w-full bg-white rounded-xl shadow text-lg">
              <thead>
                <tr>
                  {multiDeleteMode && (
                    <th className="py-3 px-6 text-left font-bold">
                      <input
                        type="checkbox"
                        checked={selectedForDelete.length === sortedFiles.length && sortedFiles.length > 0}
                        onChange={e => handleSelectAll(e.target.checked)}
                        aria-label="Select all files"
                      />
                    </th>
                  )}
                  <th className="py-3 px-6 text-left font-bold">S.No.</th>
                  <th className="py-3 px-6 text-left font-bold">File Name</th>
                  <th className="py-3 px-6 text-left font-bold cursor-pointer select-none" onClick={() => setSortAsc((asc) => !asc)}>
                    <span className="flex items-center gap-2">
                      Upload Date
                      {sortAsc ? (
                        <span title="Sort ascending">↑</span>
                      ) : (
                        <span title="Sort descending">↓</span>
                      )}
                    </span>
                  </th>
                  <th className="py-3 px-6 text-left font-bold">Delete</th>
                </tr>
              </thead>
              <tbody>
                {sortedFiles.map((file, idx) => (
                  <tr key={file._id || idx} className="border-b last:border-b-0">
                    {multiDeleteMode && (
                      <td className="py-3 px-6">
                        <input
                          type="checkbox"
                          checked={selectedForDelete.includes(file._id)}
                          onChange={e => {
                            if (e.target.checked) {
                              setSelectedForDelete(prev => [...prev, file._id]);
                            } else {
                              setSelectedForDelete(prev => prev.filter(id => id !== file._id));
                            }
                          }}
                          aria-label={`Select file ${file.originalname}`}
                        />
                      </td>
                    )}
                    <td className="py-3 px-6 font-semibold">{idx + 1}</td>
                    <td className="py-3 px-6">{file.originalname}</td>
                    <td className="py-3 px-6">{new Date(file.uploadDate).toLocaleString()}</td>
                    <td className="py-3 px-6">
                      <button
                        onClick={() => handleDeleteFile(file._id)}
                        className="text-red-600 hover:text-red-800"
                        title="Delete file"
                        disabled={multiDeleteMode}
                      >
                        <Trash2 className="w-6 h-6" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
