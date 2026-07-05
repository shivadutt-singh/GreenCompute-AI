"use client";

import React, { useState, useEffect } from "react";
import MetricsPanel from "../components/MetricsPanel";
import CodeDiffViewer from "../components/CodeDiffViewer";
import PRFeed from "../components/PRFeed";
import Sidebar from "../components/Sidebar";
import { 
  Cpu, 
  Leaf, 
  GitPullRequest, 
  RefreshCw, 
  Zap, 
  AlertTriangle, 
  FileCode
} from "lucide-react";

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

interface Stats {
  total_cpu_cycles_saved: number;
  total_co2_prevented_g: number;
  total_prs_intercepted: number;
  optimized_prs_count: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({
    total_cpu_cycles_saved: 4210984,
    total_co2_prevented_g: 143.25,
    total_prs_intercepted: 3,
    optimized_prs_count: 3
  });
  const [selectedFix, setSelectedFix] = useState<PRFix | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<string>("");

  const backendUrl = "http://localhost:8000";

  const fetchStats = async () => {
    try {
      const statsRes = await fetch(`${backendUrl}/api/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
      setLastRefreshed(new Date().toLocaleTimeString());
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  useEffect(() => {
    fetchStats();
    // Poll stats dynamically
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  const triggerSimulation = async () => {
    setIsSimulating(true);
    try {
      const res = await fetch(`${backendUrl}/api/simulate`, { method: "POST" });
      if (res.ok) {
        await fetchStats();
      }
    } catch (err) {
      console.error("Failed to run webhook simulation:", err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-neutral-950 text-neutral-100 relative font-sans">
      {/* Background glow accents */}
      <div className="absolute top-[-10%] left-[20%] w-[400px] h-[400px] rounded-full bg-emerald-950/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[10%] right-[10%] w-[500px] h-[500px] rounded-full bg-neutral-900/10 blur-[150px] pointer-events-none" />

      {/* Sidebar */}
      <Sidebar activeRoute="/" lastSync={lastRefreshed} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-screen overflow-y-auto">
        {/* Main Header */}
        <header className="border-b border-neutral-900 bg-neutral-950/80 backdrop-blur-md sticky top-0 z-10 h-16 shrink-0">
          <div className="px-6 h-full flex items-center justify-between">
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white">
                Command Center
              </h1>
              <p className="text-[10px] text-neutral-400 font-mono">Carbon-Aware Continuous Integration</p>
            </div>

            <div className="flex items-center space-x-4">
              {/* Live Grid Status Badge */}
              <div className="flex items-center space-x-2 bg-neutral-900 border border-neutral-800 rounded px-2.5 py-1 text-xs select-none">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <span className="text-neutral-300 font-mono text-[10px]">Grid Carbon: 140g CO2/kWh</span>
              </div>

              <button
                onClick={triggerSimulation}
                disabled={isSimulating}
                className="bg-white text-neutral-950 hover:bg-neutral-100 disabled:opacity-50 px-3 py-1.5 rounded text-xs font-semibold flex items-center space-x-2 cursor-pointer transition-colors"
              >
                {isSimulating ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Intercepting PR...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
                    <span>Simulate Webhook Intercept</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Container */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-7xl mx-auto flex flex-col">
          {/* Metrics Panel Component */}
          <MetricsPanel
            cpuSaved={stats.total_cpu_cycles_saved}
            co2Prevented={stats.total_co2_prevented_g}
          />

          {/* Dashboard Split View */}
          <section className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[500px]">
            
            {/* Left Column: Intercepted PRs List (4 cols) */}
            <div className="lg:col-span-4 flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider flex items-center space-x-2">
                  <GitPullRequest className="w-3.5 h-3.5" />
                  <span>PR Interception Feed</span>
                </h2>
              </div>

              <div className="flex-1 bg-neutral-900/20 border border-neutral-900 rounded-lg overflow-y-auto max-h-[600px] p-2 space-y-2">
                <PRFeed
                  onSelectFix={setSelectedFix}
                  selectedFixId={selectedFix ? selectedFix.id : null}
                />
              </div>
            </div>

            {/* Right Column: Code Scan Detail & Monaco Diff (8 cols) */}
            <div className="lg:col-span-8 flex flex-col space-y-4">
              
              <div className="flex items-center justify-between">
                <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider flex items-center space-x-2">
                  <FileCode className="w-3.5 h-3.5" />
                  <span>AST Node Inspection</span>
                </h2>
              </div>

              {selectedFix ? (
                <div className="flex-1 bg-neutral-900/20 border border-neutral-900 rounded-lg p-6 flex flex-col space-y-6 min-h-[500px]">
                  
                  {/* Info Header */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-neutral-950/80 border border-neutral-900 rounded p-4 select-none">
                    <div>
                      <span className="text-[10px] font-mono text-neutral-550 block uppercase">Target File</span>
                      <span className="text-xs font-mono text-white mt-1 block truncate">
                        {selectedFix.file_path}
                      </span>
                    </div>

                    <div>
                      <span className="text-[10px] font-mono text-neutral-550 block uppercase">CPU Savings</span>
                      <span className="text-xs font-mono text-white mt-1 block flex items-center space-x-1">
                        <Cpu className="w-3.5 h-3.5 text-neutral-400" />
                        <span>{selectedFix.cpu_cycles_saved.toLocaleString()} cycles</span>
                      </span>
                    </div>

                    <div>
                      <span className="text-[10px] font-mono text-neutral-550 block uppercase">Carbon Prevented</span>
                      <span className="text-xs font-mono text-emerald-400 mt-1 block flex items-center space-x-1">
                        <Leaf className="w-3.5 h-3.5" />
                        <span>{selectedFix.co2_saved_g.toFixed(3)} g CO₂e</span>
                      </span>
                    </div>
                  </div>

                  {/* Explanation card */}
                  <div className="bg-neutral-900/50 border border-neutral-900 rounded p-4">
                    <div className="flex items-center space-x-2 text-xs font-semibold text-white select-none">
                      <AlertTriangle className="w-4 h-4 text-amber-500" />
                      <span>Inefficient AST Node Found ({selectedFix.status})</span>
                    </div>
                    <p className="text-xs text-neutral-400 mt-2 leading-relaxed font-sans">
                      {selectedFix.explanation}
                    </p>
                  </div>

                  {/* Monaco Diff Viewer Component */}
                  <CodeDiffViewer
                    originalCode={selectedFix.original_code}
                    optimizedCode={selectedFix.optimized_code}
                    filePath={selectedFix.file_path}
                  />
                </div>
              ) : (
                <div className="flex-1 bg-neutral-900/20 border border-neutral-900 rounded-lg flex flex-col items-center justify-center py-24 text-center text-neutral-550 space-y-4 select-none">
                  <div className="p-4 bg-neutral-900 border border-neutral-800 rounded-full text-neutral-600">
                    <GitPullRequest className="w-8 h-8" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-neutral-400">Select a PR Interception</h3>
                    <p className="text-xs text-neutral-500 max-w-xs mt-1">
                      Select a repository pull request from the left-hand panel to review specific AST code optimizations.
                    </p>
                  </div>
                </div>
              )}

            </div>

          </section>

        </main>

        <footer className="border-t border-neutral-900 bg-neutral-950 py-6 text-center text-xs text-neutral-500 font-mono select-none">
          <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0">
            <span>🌿 GreenCompute AI — Making DevOps carbon-neutral, one PR at a time.</span>
            <span>© 2026 GreenCompute Engine</span>
          </div>
        </footer>
      </div>
    </div>
  );
}
