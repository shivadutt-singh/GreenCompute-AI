"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { Sliders, HelpCircle } from "lucide-react";

export default function AgentRules() {
  const [lastRefreshed, setLastRefreshed] = useState<string>("");
  const [optimizeLoops, setOptimizeLoops] = useState<boolean>(true);
  const [refactorData, setRefactorData] = useState<boolean>(true);
  const [strictWcag, setStrictWcag] = useState<boolean>(false);
  const [minSavings, setMinSavings] = useState<number>(0.05);
  const [maxSearchDepth, setMaxSearchDepth] = useState<number>(25);

  useEffect(() => {
    setLastRefreshed(new Date().toLocaleTimeString());
  }, []);

  return (
    <div className="flex min-h-screen bg-neutral-950 text-neutral-100 relative font-sans">
      {/* Background glow accents */}
      <div className="absolute top-[-10%] left-[20%] w-[400px] h-[400px] rounded-full bg-emerald-950/5 blur-[120px] pointer-events-none" />

      {/* Sidebar */}
      <Sidebar activeRoute="/rules" lastSync={lastRefreshed} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-screen overflow-y-auto">
        {/* Header */}
        <header className="border-b border-neutral-900 bg-neutral-950/80 backdrop-blur-md sticky top-0 z-10 h-16 shrink-0">
          <div className="px-6 h-full flex items-center justify-between">
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white flex items-center space-x-2">
                <Sliders className="w-4 h-4 text-neutral-400" />
                <span>Agent Rules</span>
              </h1>
              <p className="text-[10px] text-neutral-400 font-mono">AST Parser Rules Configuration</p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-3xl mx-auto flex flex-col justify-start">
          
          {/* Rules Configuration */}
          <div className="bg-neutral-900/20 border border-neutral-900 rounded-lg p-6 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider">
                Parser Optimization Rules
              </h2>
            </div>

            {/* Checklist of toggles */}
            <div className="space-y-4">
              
              {/* Rule 1: Optimize Loops */}
              <div className="flex items-start justify-between py-3 border-b border-neutral-900 select-none">
                <div className="space-y-1 pr-4">
                  <h4 className="text-xs font-semibold text-white flex items-center space-x-1.5">
                    <span>Optimize O(n²) Loops</span>
                    <span className="text-[8px] font-mono px-1 py-0.25 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 uppercase rounded">AST</span>
                  </h4>
                  <p className="text-[10px] text-neutral-500 font-mono">
                    Identify nested loops, inefficient indexing, and translate to linear lookup structures
                  </p>
                </div>
                <button 
                  onClick={() => setOptimizeLoops(!optimizeLoops)}
                  className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer shrink-0 ${
                    optimizeLoops ? "bg-emerald-500" : "bg-neutral-800"
                  }`}
                >
                  <div className={`bg-neutral-950 w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 ${
                    optimizeLoops ? "translate-x-4" : "translate-x-0"
                  }`} />
                </button>
              </div>

              {/* Rule 2: Refactor Heavy Data Structures */}
              <div className="flex items-start justify-between py-3 border-b border-neutral-900 select-none">
                <div className="space-y-1 pr-4">
                  <h4 className="text-xs font-semibold text-white flex items-center space-x-1.5">
                    <span>Refactor Heavy Data Structures</span>
                    <span className="text-[8px] font-mono px-1 py-0.25 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 uppercase rounded">Memory</span>
                  </h4>
                  <p className="text-[10px] text-neutral-500 font-mono">
                    Warn on large memory allocations and optimize generator representations (e.g. range vs list generators)
                  </p>
                </div>
                <button 
                  onClick={() => setRefactorData(!refactorData)}
                  className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer shrink-0 ${
                    refactorData ? "bg-emerald-500" : "bg-neutral-800"
                  }`}
                >
                  <div className={`bg-neutral-950 w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 ${
                    refactorData ? "translate-x-4" : "translate-x-0"
                  }`} />
                </button>
              </div>

              {/* Rule 3: Strict WCAG Compliance */}
              <div className="flex items-start justify-between py-3 border-b border-neutral-900 select-none">
                <div className="space-y-1 pr-4">
                  <h4 className="text-xs font-semibold text-white flex items-center space-x-1.5">
                    <span>Strict WCAG Compliance</span>
                    <span className="text-[8px] font-mono px-1 py-0.25 bg-neutral-900 border border-neutral-800 text-neutral-400 uppercase rounded">Accessibility</span>
                  </h4>
                  <p className="text-[10px] text-neutral-500 font-mono">
                    Scan DOM nodes in frontend files and enforce accessibility standards on generated code
                  </p>
                </div>
                <button 
                  onClick={() => setStrictWcag(!strictWcag)}
                  className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer shrink-0 ${
                    strictWcag ? "bg-emerald-500" : "bg-neutral-800"
                  }`}
                >
                  <div className={`bg-neutral-950 w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 ${
                    strictWcag ? "translate-x-4" : "translate-x-0"
                  }`} />
                </button>
              </div>
            </div>

            {/* Threshold Sliders */}
            <div className="space-y-6 pt-4">
              <h3 className="text-xs font-semibold text-neutral-400 font-mono uppercase tracking-wider">Optimization Thresholds</h3>
              
              {/* Threshold 1: Carbon Savings */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-neutral-300">Min Carbon Savings Threshold</span>
                  <span className="font-mono text-emerald-400 font-bold">{minSavings.toFixed(2)} g CO₂e</span>
                </div>
                <input 
                  type="range" 
                  min="0.01" 
                  max="1.00" 
                  step="0.01"
                  value={minSavings}
                  onChange={(e) => setMinSavings(parseFloat(e.target.value))}
                  className="w-full h-1 bg-neutral-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
                <p className="text-[9px] text-neutral-500 font-mono">Ignore optimizations predicting less than this carbon threshold.</p>
              </div>

              {/* Threshold 2: Search Depth */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-neutral-300">Max AST Search Depth</span>
                  <span className="font-mono text-white font-bold">{maxSearchDepth} nodes</span>
                </div>
                <input 
                  type="range" 
                  min="5" 
                  max="100" 
                  step="5"
                  value={maxSearchDepth}
                  onChange={(e) => setMaxSearchDepth(parseInt(e.target.value))}
                  className="w-full h-1 bg-neutral-800 rounded-lg appearance-none cursor-pointer accent-neutral-200"
                />
                <p className="text-[9px] text-neutral-500 font-mono">Maximum recursion depth for analyzing code syntax structures.</p>
              </div>
            </div>

            {/* Save Button */}
            <div className="flex justify-end pt-4 border-t border-neutral-900">
              <button 
                className="px-4 py-2 bg-white text-neutral-950 hover:bg-neutral-100 rounded text-xs font-semibold cursor-pointer transition-colors"
                onClick={() => alert("Rules updated successfully.")}
              >
                Apply Agent Rules
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
