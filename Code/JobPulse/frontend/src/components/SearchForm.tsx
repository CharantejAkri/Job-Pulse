"use client";

import { useState } from "react";
import { scrapingApi } from "@/lib/api";
import { Loader2, Search } from "lucide-react";

const SOURCES = [
  { id: "linkedin", label: "LinkedIn", disabled: false },
  { id: "naukri", label: "Naukri", disabled: false },
  { id: "indeed", label: "Indeed", disabled: false },
];

const DATE_OPTIONS = [
  { value: "past_24h", label: "Past 24 hours" },
  { value: "past_week", label: "Past week" },
  { value: "past_month", label: "Past month" },
];

export function SearchForm() {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [selectedSources, setSelectedSources] = useState<string[]>(["indeed"]);
  const [datePosted, setDatePosted] = useState("past_24h");
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const toggleSource = (source: string) => {
    setSelectedSources((prev) =>
      prev.includes(source) ? prev.filter((s) => s !== source) : [...prev, source]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await scrapingApi.startScrape({
        job_title: jobTitle,
        location: location || undefined,
        sources: selectedSources,
        date_posted: datePosted,
      });
      setTaskId(response.data.task_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to start scrape");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">New Job Search</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Job Title *</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="e.g. React Developer, SDE-2"
              className="input-field"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Mumbai, Bangalore"
              className="input-field"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">Sources</label>
          <div className="flex gap-4">
            {SOURCES.map((source) => (
              <label
                key={source.id}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg border cursor-pointer transition-colors ${
                  selectedSources.includes(source.id)
                    ? "border-primary-500 bg-primary-50"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedSources.includes(source.id)}
                  onChange={() => toggleSource(source.id)}
                  className="w-4 h-4 text-primary-600"
                />
                <span className="text-sm font-medium">{source.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Date Posted</label>
          <select
            value={datePosted}
            onChange={(e) => setDatePosted(e.target.value)}
            className="input-field"
          >
            {DATE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">{error}</div>
        )}

        {taskId && (
          <div className="bg-green-50 text-green-600 p-3 rounded-lg text-sm">
            Task queued! Task ID: {taskId}
          </div>
        )}

        <button type="submit" disabled={loading || selectedSources.length === 0} className="btn-primary flex items-center gap-2">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
          {loading ? "Starting..." : "Start Scrape"}
        </button>
      </form>
    </div>
  );
}
