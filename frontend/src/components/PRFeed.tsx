"use client";

import React, { useState, useEffect } from "react";
import { GitPullRequest, Leaf, Clock, RefreshCw } from "lucide-react";

interface PRFix {
  id: number;
  pr_number: number;
  repo_name: string;
  pr_title: string;
  author: string;
  file_path: string;
  original_code: string;
  optimized_code: string;
  explanation: string;
  cpu_cycles_saved: number;
  co2_saved_g: number;
  status: string;
  created_at: string;
}

interface PRFeedProps {
  onSelectFix: (fix: PRFix) => void;
  selectedFixId: number | null;
}

export default function PRFeed({ onSelectFix, selectedFixId }: PRFeedProps) {
  const [fixes, setFixes] = useState<PRFix[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFixes = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/prs/fixes");
        if (!response.ok) {
          throw new Error("Failed to fetch PR fixes from backend");
        }
        const data = await response.json();
        setFixes(data);
        if (data.length > 0 && selectedFixId === null) {
          onSelectFix(data[0]);
        }
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Failed to load PR fixes");
      } finally {
        setIsLoading(false);
      }
    };

    fetchFixes();
  }, [onSelectFix, selectedFixId]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-neutral-500 space-y-3 font-mono text-[10px]">
        <RefreshCw className="w-5 h-5 animate-spin text-neutral-600" />
        <span>Loading PR telemetry feed...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 border border-neutral-900 bg-neutral-950 text-red-400 rounded text-xs font-mono">
        Error loading feed: {error}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {fixes.map((fix) => {
        const isSelected = selectedFixId === fix.id;
        return (
          <div
            key={fix.id}
            onClick={() => onSelectFix(fix)}
            className={`p-3 rounded border text-left cursor-pointer transition-all duration-150 ${
              isSelected
                ? "bg-neutral-900 border-neutral-700 shadow-md"
                : "bg-transparent border-neutral-900 hover:bg-neutral-900/20 hover:border-neutral-800"
            }`}
          >
            <div className="flex items-center justify-between text-[10px] font-mono text-neutral-450 select-none">
              <span className="truncate max-w-[170px]">{fix.repo_name}</span>
              <span>#{fix.pr_number}</span>
            </div>
            <h4 className="text-xs font-medium text-white truncate mt-1">{fix.pr_title}</h4>
            
            <div className="flex items-center justify-between mt-3 select-none">
              <div className="flex items-center space-x-1.5">
                <span className="w-4 h-4 rounded-full bg-neutral-800 border border-neutral-750 flex items-center justify-center text-[9px] font-semibold text-neutral-300">
                  {fix.author[0]?.toUpperCase()}
                </span>
                <span className="text-[10px] text-neutral-400 font-mono truncate max-w-[80px]">@{fix.author}</span>
              </div>

              <div className="flex items-center space-x-2">
                <div className="bg-emerald-950/40 border border-emerald-900/60 rounded px-1.5 py-0.5 text-[9px] font-mono text-emerald-400 flex items-center space-x-0.5">
                  <Leaf className="w-2.5 h-2.5" />
                  <span>{fix.co2_saved_g.toFixed(2)}g</span>
                </div>

                <span className="flex items-center space-x-0.5 text-[9px] uppercase font-mono px-1 rounded bg-neutral-900 border border-neutral-800 text-neutral-400">
                  <Clock className="w-2.5 h-2.5" />
                  <span>{fix.status}</span>
                </span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
