"use client";

import { useEffect, useRef } from "react";
import { Bot, Terminal } from "lucide-react";

export default function AgentConsole({ logs }: { logs: any[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden shadow-2xl flex flex-col h-full bg-opacity-70 backdrop-blur-md">
      <div className="bg-neutral-950 border-b border-neutral-800 p-4 flex items-center justify-between">
        <h2 className="text-xl font-bold flex items-center text-emerald-400">
          <Bot className="mr-2" /> Agent Intelligence
        </h2>
        <div className="flex gap-1">
          <span className="w-3 h-3 rounded-full bg-red-500"></span>
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
          <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
        </div>
      </div>
      <div ref={scrollRef} className="p-4 flex-1 overflow-y-auto space-y-4 font-mono text-sm max-h-[600px]">
        {logs.length === 0 ? (
          <div className="text-neutral-500 flex items-center h-full justify-center opacity-50">
            <Terminal className="mr-2" /> Waiting for events...
          </div>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="animate-fade-in-up border-l-2 pl-3 border-emerald-900 leading-relaxed">
              <span className={`font-bold mr-2 uppercase ${log.agent === "System" ? "text-neutral-500" : log.agent === "Interpreter" ? "text-purple-400" : log.agent === "Matcher" ? "text-blue-400" : log.agent === "Negotiator" ? "text-amber-400" : log.agent === "Evaluator" ? "text-emerald-400" : "text-white"}`}>
                [{log.agent}]
              </span>
              <span className="text-neutral-300">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
