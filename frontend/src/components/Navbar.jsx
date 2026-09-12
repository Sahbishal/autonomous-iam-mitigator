import React from 'react';
import { ShieldCheck, Play, RotateCcw, Cpu, Sparkles } from 'lucide-react';

export default function Navbar({ onRunDemo, onSelectScenario, activeScenario, isRunning, onReset }) {
  return (
    <header className="bg-[#0D1322]/90 backdrop-blur-xl border-b border-blue-900/30 sticky top-0 z-50 px-6 py-3.5 shadow-2xl">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand & Glowing Icon */}
        <div className="flex items-center gap-3.5">
          <div className="p-2.5 bg-gradient-to-br from-blue-600/30 via-cyan-500/20 to-purple-600/20 border border-cyan-500/40 rounded-xl text-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.2)]">
            <ShieldCheck className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-xl bg-gradient-to-r from-white via-blue-100 to-cyan-300 bg-clip-text text-transparent tracking-tight">
                Tech Zephyr 4.0
              </h1>
              <span className="bg-gradient-to-r from-blue-600/30 to-cyan-500/30 border border-cyan-500/40 text-cyan-300 text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider font-mono">
                AI SECURITY AGENT
              </span>
            </div>
            <p className="text-xs text-gray-400 font-medium tracking-wide">
              Autonomous Cloud IAM Least-Privilege Mitigator
            </p>
          </div>
        </div>

        {/* Guardrail Banner */}
        <div className="bg-gradient-to-r from-amber-500/10 via-amber-950/30 to-amber-500/10 border border-amber-500/30 text-amber-300 text-xs px-4 py-1.5 rounded-full flex items-center gap-2.5 font-mono shadow-[0_0_12px_rgba(245,158,11,0.15)]">
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
          SYNTHETIC CLOUD ENVIRONMENT — NO PRODUCTION ACCESS
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <select 
            value={activeScenario}
            onChange={(e) => onSelectScenario(e.target.value)}
            disabled={isRunning}
            className="bg-gray-900/90 border border-blue-900/40 text-gray-200 text-xs font-medium rounded-xl px-3.5 py-2.5 focus:ring-2 focus:ring-cyan-500 focus:outline-none shadow-inner"
          >
            <option value="scenario_b">⭐ Scenario B: Hidden Dependency (Demo)</option>
            <option value="scenario_a">Scenario A: Safe Direct Removal</option>
            <option value="scenario_c">Scenario C: Multi-Service Replanning</option>
          </select>

          <button
            onClick={onReset}
            disabled={isRunning}
            className="p-2.5 text-gray-400 hover:text-gray-100 hover:bg-gray-800/80 rounded-xl border border-gray-700/60 transition shadow-sm hover:border-gray-500"
            title="Reset Synthetic Cloud Environment"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={onRunDemo}
            disabled={isRunning}
            className={`flex items-center gap-2 px-5 py-2.5 text-xs font-bold rounded-xl text-white transition-all shadow-[0_0_20px_rgba(37,99,235,0.4)] ${
              isRunning 
                ? 'bg-blue-900/80 opacity-70 cursor-not-allowed border border-blue-700/50' 
                : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 hover:shadow-[0_0_25px_rgba(6,182,212,0.6)] active:scale-95 border border-cyan-400/40'
            }`}
          >
            {isRunning ? (
              <>
                <Cpu className="w-4 h-4 animate-spin text-cyan-300" />
                <span>Agent Executing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 fill-white" />
                <span>Run Demo Scenario</span>
              </>
            )}
          </button>
        </div>

      </div>
    </header>
  );
}
