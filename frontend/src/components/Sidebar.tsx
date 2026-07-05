"use client";

import React from "react";
import Link from "next/link";
import { Leaf, Zap, GitPullRequest, Cpu, Globe, Settings, Sliders } from "lucide-react";

interface SidebarProps {
  activeRoute: string;
  lastSync?: string;
}

export default function Sidebar({ activeRoute, lastSync = "N/A" }: SidebarProps) {
  const navItems = [
    { href: "/", label: "Command Center", icon: Zap },
    { href: "/routing", label: "Workload Routing", icon: Globe },
    { href: "/integrations", label: "Git Integrations", icon: Settings },
    { href: "/rules", label: "Agent Rules", icon: Sliders },
  ];

  return (
    <aside className="w-64 border-r border-neutral-900 bg-neutral-950 flex flex-col z-20 shrink-0 select-none">
      <div className="p-6 border-b border-neutral-900 h-16 flex items-center space-x-3">
        <div className="p-1.5 bg-emerald-950/30 border border-emerald-900/40 rounded text-emerald-400">
          <Leaf className="w-4 h-4" />
        </div>
        <span className="text-sm font-semibold tracking-tight text-white font-mono">
          GreenCompute AI
        </span>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        <div className="text-[9px] uppercase font-mono text-neutral-500 tracking-wider px-3 mb-2">
          Operations
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeRoute === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-2.5 px-3 py-2 text-xs font-mono rounded transition-colors ${
                isActive
                  ? "bg-neutral-900 text-white border border-neutral-800"
                  : "text-neutral-400 hover:text-neutral-200 hover:bg-neutral-900/30 border border-transparent"
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? "text-emerald-400" : ""}`} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-neutral-900 space-y-3">
        <div className="flex items-center justify-between text-[10px] font-mono text-neutral-500">
          <span>Engine Status</span>
          <span className="flex items-center space-x-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            <span className="text-emerald-500 font-semibold">ACTIVE</span>
          </span>
        </div>
        <div className="flex items-center justify-between text-[10px] font-mono text-neutral-500">
          <span>Poll Interval</span>
          <span>3s</span>
        </div>
        <div className="flex items-center justify-between text-[10px] font-mono text-neutral-500">
          <span>Last Sync</span>
          <span>{lastSync}</span>
        </div>
      </div>
    </aside>
  );
}
