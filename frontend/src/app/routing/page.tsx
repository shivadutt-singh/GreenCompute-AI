"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { Globe, Server, Activity, Terminal } from "lucide-react";

interface GridNode {
  region: string;
  provider: string;
  load: number;
  carbonIntensity: number;
  status: "ACTIVE" | "SUSPENDED" | "OPTIMIZED";
}

export default function WorkloadRouting() {
  const [lastRefreshed, setLastRefreshed] = useState<string>("");
  const [nodes, setNodes] = useState<GridNode[]>([
    { region: "us-east-1 (N. Virginia)", provider: "AWS", load: 20, carbonIntensity: 420, status: "SUSPENDED" },
    { region: "europe-west1 (Belgium)", provider: "GCP", load: 80, carbonIntensity: 110, status: "OPTIMIZED" },
    { region: "westus2 (Washington)", provider: "Azure", load: 45, carbonIntensity: 190, status: "ACTIVE" },
    { region: "asia-east1 (Taiwan)", provider: "GCP", load: 15, carbonIntensity: 360, status: "ACTIVE" }
  ]);

  const terminalLogs = [
    "[GreenOps Agent] Checking regional grid carbon intensity...",
    "[Grid Telemetry] us-east-1: 420g CO2/kWh (High carbon footprint)",
    "[Grid Telemetry] europe-west1: 110g CO2/kWh (Low carbon footprint, renewable mix)",
    "[GreenOps Agent] Initiating load shifting sequence...",
    "[GreenOps Agent] Scaling down us-east-1 replicas in deployment.yaml: 10 -> 2",
    "[GreenOps Agent] Scaling up europe-west1 replicas in deployment.yaml: 2 -> 10",
    "[GreenOps Agent] Re-routing ingress traffic weight: us-east-1 (20%), europe-west1 (80%)",
    "[GreenOps Agent] Applying configurations: kubectl apply -f deployment.yaml",
    "[System] Workloads re-routed successfully. Real-time Carbon saved: 68%"
  ];

  useEffect(() => {
    setLastRefreshed(new Date().toLocaleTimeString());
  }, []);

  return (
    <div className="flex min-h-screen bg-neutral-950 text-neutral-100 relative font-sans">
      {/* Background glow accents */}
      <div className="absolute top-[-10%] left-[20%] w-[400px] h-[400px] rounded-full bg-emerald-950/5 blur-[120px] pointer-events-none" />

      {/* Sidebar */}
      <Sidebar activeRoute="/routing" lastSync={lastRefreshed} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-screen overflow-y-auto">
        {/* Header */}
        <header className="border-b border-neutral-900 bg-neutral-950/80 backdrop-blur-md sticky top-0 z-10 h-16 shrink-0">
          <div className="px-6 h-full flex items-center justify-between">
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white flex items-center space-x-2">
                <Globe className="w-4 h-4 text-emerald-400" />
                <span>Workload Routing</span>
              </h1>
              <p className="text-[10px] text-neutral-400 font-mono">Carbon-Aware Infrastructure Dispatch</p>
            </div>
            <div className="flex items-center space-x-2 bg-neutral-900 border border-neutral-800 rounded px-2.5 py-1 text-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span className="text-neutral-300 font-mono text-[10px]">Optimal Region: GCP europe-west1</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-7xl mx-auto flex flex-col">
          {/* Carbon Intensity Comparison Card */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-neutral-900/50 border border-neutral-800/80 rounded-lg p-6 flex items-start justify-between">
              <div className="space-y-2">
                <p className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider">
                  Current Grid Intensity
                </p>
                <p className="text-3xl font-bold tracking-tight text-red-400 font-mono">
                  340 <span className="text-xs font-sans text-neutral-400">g CO₂e/kWh</span>
                </p>
                <p className="text-[10px] text-neutral-500 font-mono">
                  Weighted average of active regions
                </p>
              </div>
              <div className="p-2 border border-neutral-800 rounded-md bg-neutral-950 text-red-400">
                <Activity className="w-4 h-4" />
              </div>
            </div>

            <div className="bg-neutral-900/50 border border-neutral-800/80 rounded-lg p-6 flex items-start justify-between">
              <div className="space-y-2">
                <p className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider">
                  Optimized Grid Intensity
                </p>
                <p className="text-3xl font-bold tracking-tight text-emerald-400 font-mono">
                  120 <span className="text-xs font-sans text-neutral-400">g CO₂e/kWh</span>
                </p>
                <p className="text-[10px] text-neutral-500 font-mono">
                  Projected target after load shift
                </p>
              </div>
              <div className="p-2 border border-neutral-800 rounded-md bg-neutral-950 text-emerald-400">
                <Activity className="w-4 h-4" />
              </div>
            </div>
          </div>

          {/* Regional Grid Status */}
          <div className="bg-neutral-900/20 border border-neutral-900 rounded-lg p-6 space-y-4">
            <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider flex items-center space-x-2">
              <Server className="w-3.5 h-3.5" />
              <span>Regional Grid Nodes</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {nodes.map((node) => (
                <div key={node.region} className="bg-neutral-950 border border-neutral-900 rounded p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-300">
                      {node.provider}
                    </span>
                    <span className={`text-[9px] font-mono px-1 rounded ${
                      node.status === "OPTIMIZED" 
                        ? "bg-emerald-950/80 border border-emerald-800/80 text-emerald-400"
                        : node.status === "SUSPENDED"
                        ? "bg-red-950/80 border border-red-800/80 text-red-400"
                        : "bg-neutral-900 border border-neutral-800 text-neutral-400"
                    }`}>
                      {node.status}
                    </span>
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-white truncate">{node.region}</h4>
                    <p className="text-[10px] text-neutral-400 mt-1">Intensity: {node.carbonIntensity}g/kWh</p>
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between text-[9px] font-mono text-neutral-500">
                      <span>Load</span>
                      <span>{node.load}%</span>
                    </div>
                    <div className="w-full bg-neutral-900 rounded-full h-1">
                      <div 
                        className={`h-1 rounded-full ${
                          node.status === "SUSPENDED" ? "bg-red-500" : "bg-emerald-500"
                        }`}
                        style={{ width: `${node.load}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Terminal Console Logs */}
          <div className="bg-neutral-900/20 border border-neutral-900 rounded-lg p-6 space-y-4 flex-1 flex flex-col">
            <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider flex items-center space-x-2">
              <Terminal className="w-3.5 h-3.5" />
              <span>Shifting Logs Terminal</span>
            </h2>
            <div className="flex-1 bg-neutral-950 border border-neutral-900 rounded p-4 font-mono text-xs text-neutral-300 space-y-2 overflow-y-auto max-h-[300px]">
              {terminalLogs.map((log, idx) => (
                <div key={idx} className="leading-relaxed">
                  <span className="text-emerald-500">~</span> {log}
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
