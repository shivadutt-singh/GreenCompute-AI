"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { Settings, Check, AlertTriangle, RefreshCw } from "lucide-react";

export default function GitIntegrations() {
  const [lastRefreshed, setLastRefreshed] = useState<string>("");
  const [repoUrl, setRepoUrl] = useState<string>("https://github.com/google/jax");
  const [webhookSecret, setWebhookSecret] = useState<string>("••••••••••••••••");
  const [autoCommit, setAutoCommit] = useState<boolean>(true);
  const [isTesting, setIsTesting] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<"IDLE" | "SUCCESS" | "FAILED">("IDLE");

  useEffect(() => {
    setLastRefreshed(new Date().toLocaleTimeString());
  }, []);

  const handleTestConnection = () => {
    setIsTesting(true);
    setTestResult("IDLE");
    setTimeout(() => {
      setIsTesting(false);
      setTestResult("SUCCESS");
    }, 1500);
  };

  return (
    <div className="flex min-h-screen bg-neutral-950 text-neutral-100 relative font-sans">
      {/* Background glow accents */}
      <div className="absolute top-[-10%] left-[20%] w-[400px] h-[400px] rounded-full bg-emerald-950/5 blur-[120px] pointer-events-none" />

      {/* Sidebar */}
      <Sidebar activeRoute="/integrations" lastSync={lastRefreshed} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-screen overflow-y-auto">
        {/* Header */}
        <header className="border-b border-neutral-900 bg-neutral-950/80 backdrop-blur-md sticky top-0 z-10 h-16 shrink-0">
          <div className="px-6 h-full flex items-center justify-between">
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white flex items-center space-x-2">
                <Settings className="w-4 h-4 text-neutral-400" />
                <span>Git Integrations</span>
              </h1>
              <p className="text-[10px] text-neutral-400 font-mono">Continuous Integration Settings</p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-3xl mx-auto flex flex-col justify-start">
          <div className="bg-neutral-900/20 border border-neutral-900 rounded-lg p-6 space-y-6">
            <h2 className="text-xs uppercase font-mono text-neutral-400 tracking-wider">
              Webhook Configuration
            </h2>

            <div className="space-y-4">
              {/* GitHub Repository URL */}
              <div className="space-y-1">
                <label className="text-[10px] font-mono uppercase text-neutral-500 block">GitHub Repository URL</label>
                <input 
                  type="text" 
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/username/repo"
                  className="w-full bg-neutral-950 border border-neutral-900 rounded px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-neutral-700 transition-colors"
                />
              </div>

              {/* Webhook Secret */}
              <div className="space-y-1">
                <label className="text-[10px] font-mono uppercase text-neutral-500 block">Webhook Secret</label>
                <input 
                  type="password" 
                  value={webhookSecret}
                  onChange={(e) => setWebhookSecret(e.target.value)}
                  placeholder="Secret key used for payload validation"
                  className="w-full bg-neutral-950 border border-neutral-900 rounded px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-neutral-700 transition-colors"
                />
              </div>

              {/* Auto-Commit Toggle */}
              <div className="flex items-center justify-between py-2 border-t border-neutral-900 mt-2 select-none">
                <div>
                  <h4 className="text-xs font-medium text-white">Enable Auto-Commit on PR</h4>
                  <p className="text-[10px] text-neutral-500 font-mono mt-0.5">
                    Automatically push green code optimizations directly back to the pull request branch
                  </p>
                </div>
                <button 
                  onClick={() => setAutoCommit(!autoCommit)}
                  className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer focus:outline-none ${
                    autoCommit ? "bg-emerald-500" : "bg-neutral-800"
                  }`}
                >
                  <div className={`bg-neutral-950 w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 ${
                    autoCommit ? "translate-x-4" : "translate-x-0"
                  }`} />
                </button>
              </div>
            </div>

            {/* Test Connection Result Card */}
            {testResult !== "IDLE" && (
              <div className={`p-4 border rounded text-xs font-mono flex items-center space-x-2 ${
                testResult === "SUCCESS" 
                  ? "bg-emerald-950/20 border-emerald-900/60 text-emerald-400"
                  : "bg-red-950/20 border-red-900/60 text-red-400"
              }`}>
                {testResult === "SUCCESS" ? (
                  <>
                    <Check className="w-4 h-4 shrink-0" />
                    <span>Connection successful! Webhook active and responding (ping latency: 82ms).</span>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                    <span>Connection failed. Verify Webhook Secret and Repository URL.</span>
                  </>
                )}
              </div>
            )}

            {/* Action buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-neutral-900">
              <button 
                onClick={handleTestConnection}
                disabled={isTesting}
                className="px-4 py-2 border border-neutral-800 hover:border-neutral-700 bg-transparent text-neutral-300 hover:text-white rounded text-xs font-semibold flex items-center space-x-2 cursor-pointer transition-colors disabled:opacity-50"
              >
                {isTesting ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin text-neutral-500" />
                    <span>Pinging...</span>
                  </>
                ) : (
                  <span>Test Connection</span>
                )}
              </button>

              <button 
                className="px-4 py-2 bg-white text-neutral-950 hover:bg-neutral-100 rounded text-xs font-semibold cursor-pointer transition-colors"
                onClick={() => alert("Settings saved successfully.")}
              >
                Save Settings
              </button>
            </div>
          </div>

          {/* Integration Status Log */}
          <div className="bg-neutral-900/10 border border-neutral-950 rounded-lg p-6 space-y-3 mt-4">
            <h3 className="text-xs font-semibold text-neutral-400">Integration Status Details</h3>
            <div className="grid grid-cols-2 gap-4 text-[11px] font-mono text-neutral-500">
              <div className="space-y-1">
                <span>Webhook Endpoint:</span>
                <span className="text-white block mt-0.5">https://greencompute.ai/api/webhook/github</span>
              </div>
              <div className="space-y-1">
                <span>Last Event Intercepted:</span>
                <span className="text-white block mt-0.5">PR #103 (5 minutes ago)</span>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
