"use client";

import React from "react";
import { DiffEditor } from "@monaco-editor/react";
import { ArrowRight } from "lucide-react";

interface CodeDiffViewerProps {
  originalCode: string;
  optimizedCode: string;
  filePath: string;
}

export default function CodeDiffViewer({ originalCode, optimizedCode, filePath }: CodeDiffViewerProps) {
  const getLanguage = (path: string) => {
    const ext = path.split(".").pop()?.toLowerCase();
    if (ext === "py") return "python";
    if (ext === "js" || ext === "jsx" || ext === "ts" || ext === "tsx") return "javascript";
    return "plaintext";
  };

  return (
    <div className="flex-1 border border-neutral-900 rounded overflow-hidden bg-[#1e1e1e]">
      <div className="bg-neutral-950 px-4 py-2 border-b border-neutral-900 flex justify-between items-center text-xs font-mono text-neutral-450 select-none">
        <div className="flex items-center space-x-4">
          <span className="flex items-center space-x-1 text-red-400">
            <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
            <span>Original Inefficient Node</span>
          </span>
          <ArrowRight className="w-3 h-3 text-neutral-600" />
          <span className="flex items-center space-x-1 text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            <span>Optimized Green Replacement</span>
          </span>
        </div>
        <div className="text-[10px] text-neutral-500 font-mono">{filePath.split("/").pop()}</div>
      </div>
      <div className="h-[280px]">
        <DiffEditor
          original={originalCode}
          modified={optimizedCode}
          language={getLanguage(filePath)}
          theme="vs-dark"
          options={{
            readOnly: true,
            minimap: { enabled: false },
            lineNumbers: "on",
            renderSideBySide: true,
            scrollbar: {
              verticalScrollbarSize: 6,
              horizontalScrollbarSize: 6
            }
          }}
        />
      </div>
    </div>
  );
}
