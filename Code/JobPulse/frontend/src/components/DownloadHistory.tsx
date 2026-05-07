"use client";

import { useState, useEffect } from "react";
import { exportsApi } from "@/lib/api";
import { Download, FileSpreadsheet } from "lucide-react";

interface DownloadEntry {
  id: string;
  file_name: string;
  file_format: string;
  job_count: number;
  created_at: string;
  expires_at: string | null;
}

export function DownloadHistory() {
  const [downloads, setDownloads] = useState<DownloadEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    exportsApi.getHistory().then((res) => setDownloads(res.data)).finally(() => setLoading(false));
  }, []);

  const handleDownload = async (entry: DownloadEntry) => {
    window.open(exportsApi.download(entry.file_name), "_blank");
  };

  if (loading) return <div className="card">Loading...</div>;

  if (downloads.length === 0) {
    return (
      <div className="card text-center py-12">
        <FileSpreadsheet className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">No downloads yet</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Download History</h2>
      <div className="space-y-3">
        {downloads.map((entry) => (
          <div key={entry.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <FileSpreadsheet className="w-8 h-8 text-green-600" />
              <div>
                <p className="font-medium text-gray-900">{entry.file_name}</p>
                <p className="text-sm text-gray-500">
                  {entry.job_count} jobs • {entry.file_format.toUpperCase()} • {new Date(entry.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <button onClick={() => handleDownload(entry)} className="btn-primary flex items-center gap-2 text-sm">
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
