"use client";

import { useEffect, useState, useRef } from "react";
import Map from "@/components/Map";
import AgentConsole from "@/components/AgentConsole";
import Dashboard from "@/components/Dashboard";
import { Play, RotateCcw, AlertTriangle } from "lucide-react";

export default function Home() {
  const [logs, setLogs] = useState<any[]>([]);
  const [match, setMatch] = useState<any>(null);
  const [industries, setIndustries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Fetch initial map dot data
    fetch("http://localhost:8000/api/industries")
      .then(res => res.json())
      .then(data => {
        setIndustries(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch industries:", err);
        setLoading(false);
      });

    // Connect WS
    connectWebSocket();

    return () => {
      ws.current?.close();
    };
  }, []);

  const connectWebSocket = () => {
    ws.current = new WebSocket("ws://localhost:8000/ws/feed");
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.message === "RESET_DEMO") {
        setLogs([]);
        setMatch(null);
        return;
      }

      setLogs(prev => [...prev.slice(-49), data]); // keep last 50 logs
      
      if (data.match_data) {
        setMatch(data.match_data);
      }
    };

    ws.current.onclose = () => {
      console.log("WS closed, retrying in 2s...");
      setTimeout(connectWebSocket, 2000);
    };
  };

  const fireSimulationEvent = async () => {
    try {
      // Pick a random producer from our local state
      const producers = industries.filter(i => i.role === "producer");
      const randomProducer = producers[Math.floor(Math.random() * producers.length)];
      if(!randomProducer) return;
      
      const sampleEvents = [
        "We have 5 tons of high-moisture organic sludge from our brewing process.",
        "Generating 2000kg of clean wood chips and sawdust.",
        "Emitting 50 tons of CO2 weekly that needs capturing.",
        "We have excess waste heat forming 1000 liters of hot water daily.",
        "Currently disposing of 500kg of recyclable cardboard packaging.",
      ];
      
      await fetch("http://localhost:8000/api/submit-waste", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          producer_id: randomProducer.id,
          raw_text: sampleEvents[Math.floor(Math.random() * sampleEvents.length)]
        })
      });
      
      // Clear previous match visually so we can watch it again
      setMatch(null);
    } catch (e) {
      console.error(e);
    }
  };

  const resetDemo = async () => {
    try {
      await fetch("http://localhost:8000/api/reset", { method: "POST" });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <main className="flex h-screen flex-col overflow-hidden bg-neutral-950 p-4 gap-4">
      {/* Header Bar */}
      <header className="flex justify-between items-center bg-neutral-900 border border-neutral-800 rounded-xl px-6 py-4 shadow-md shrink-0">
        <div className="flex items-center gap-3">
          <div className="bg-emerald-500 rounded p-2 shadow-[0_0_15px_rgba(16,185,129,0.5)]">
            <AlertTriangle className="text-black" size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-tight text-white uppercase drop-shadow-md">WasteLink AI</h1>
            <p className="text-emerald-400 text-xs font-mono font-bold tracking-widest hidden sm:block">AUTONOMOUS SYMBIOSIS NETWORK</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <button 
            onClick={resetDemo}
            className="flex items-center gap-2 px-4 py-2 border border-neutral-700 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded font-mono text-sm uppercase transition-all"
          >
            <RotateCcw size={16} /> Reset State
          </button>
          <button 
            onClick={fireSimulationEvent}
            className="flex items-center gap-2 px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded font-mono text-sm uppercase shadow-[0_0_15px_rgba(16,185,129,0.3)] transition-all transform active:scale-95"
          >
            <Play fill="black" size={16} /> Simulate Event
          </button>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div className="flex flex-col lg:flex-row flex-1 gap-4 min-h-0">
        
        {/* Left Col: Console & Map */}
        <div className="flex flex-col flex-1 gap-4 min-w-0">
          
          <div className="h-1/3 min-h-[250px]">
            <AgentConsole logs={logs} />
          </div>
          
          <div className="flex-1 rounded-xl relative">
             <Map industries={industries} latestMatch={match} />
          </div>
        </div>

        {/* Right Col: Dashboard Match Data */}
        <div className="w-full lg:w-1/3 xl:w-1/4 shrink-0 min-w-[350px]">
          <Dashboard match={match} />
        </div>
        
      </div>
    </main>
  );
}
