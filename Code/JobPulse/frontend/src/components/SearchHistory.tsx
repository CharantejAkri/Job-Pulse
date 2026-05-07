"use client";

import { useState, useEffect } from "react";
import { scrapingApi } from "@/lib/api";
import { Clock, RotateCcw } from "lucide-react";

interface SearchLog {
  id: string;
  job_title: string;
  location: string | null;
  sources: string[];
  date_posted: string | null;
  created_at: string;
}

export function SearchHistory() {
  const [history, setHistory] = useState<SearchLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    scrapingApi.getHistory().then((res) => setHistory(res.data)).finally(() => setLoading(false));
  }, []);

  const rerun = (log: SearchLog) => {
    console.log("Rerun search:", log);
  };

  if (loading) return <div className="card">Loading...</div>;

  if (history.length === 0) {
    return (
      <div className="card text-center py-12">
        <Clock className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">No previous searches</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Search History</h2>
      <div className="space-y-3">
        {history.map((log) => (
          <div key={log.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">{log.job_title}</p>
              <p className="text-sm text-gray-500">
                {log.location || "All India"} • {log.sources.join(", ")} • {new Date(log.created_at).toLocaleDateString()}
              </p>
            </div>
            <button onClick={() => rerun(log)} className="btn-secondary flex items-center gap-2 text-sm">
              <RotateCcw className="w-4 h-4" />
              Re-run
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
