import React from "react";
import { Cpu, Leaf } from "lucide-react";

interface MetricsPanelProps {
  cpuSaved?: number;
  co2Prevented?: number;
}

export default function MetricsPanel({ cpuSaved = 4210984, co2Prevented = 143.25 }: MetricsPanelProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Total CPU Cycles Saved */}
      <div className="bg-neutral-900/50 border border-neutral-800/80 rounded-lg p-6 flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider">
            Total CPU Cycles Saved
          </p>
          <p className="text-3xl font-bold tracking-tight text-neutral-50 font-mono">
            {cpuSaved.toLocaleString('en-US')}
          </p>
          <p className="text-[10px] text-neutral-500 font-mono">
            Direct CPU cycle reduction across intercept feed
          </p>
        </div>
        <div className="p-2 border border-neutral-800 rounded-md bg-neutral-950 text-neutral-400">
          <Cpu className="w-4 h-4" />
        </div>
      </div>

      {/* Estimated CO2 Prevented */}
      <div className="bg-neutral-900/50 border border-neutral-800/80 rounded-lg p-6 flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider">
            Estimated CO2 Prevented
          </p>
          <p className="text-3xl font-bold tracking-tight text-emerald-400 font-mono">
            {co2Prevented.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} g
          </p>
          <p className="text-[10px] text-neutral-500 font-mono">
            Prevented carbon footprint (scaled per grid status)
          </p>
        </div>
        <div className="p-2 border border-neutral-800 rounded-md bg-neutral-950 text-emerald-400">
          <Leaf className="w-4 h-4" />
        </div>
      </div>
    </div>
  );
}
