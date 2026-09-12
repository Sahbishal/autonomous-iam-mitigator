import React, { useState } from 'react';
import { Eye, Search, FileCode, Play, AlertOctagon, RefreshCw, CheckCircle, ChevronDown, ChevronRight, Terminal, Sparkles } from 'lucide-react';

const PHASE_ICONS = {
  OBSERVE: <Eye className="w-3.5 h-3.5 text-blue-400" />,
  ANALYZE: <Search className="w-3.5 h-3.5 text-purple-400" />,
  PLAN: <FileCode className="w-3.5 h-3.5 text-indigo-400" />,
  ACT: <Play className="w-3.5 h-3.5 text-emerald-400" />,
  EVALUATE: <AlertOctagon className="w-3.5 h-3.5 text-amber-400" />,
  ADAPT: <RefreshCw className="w-3.5 h-3.5 text-rose-400" />,
  VERIFY: <CheckCircle className="w-3.5 h-3.5 text-teal-400" />,
};

const PHASE_COLORS = {
  OBSERVE: 'bg-blue-500/10 border-blue-500/40 text-blue-300 shadow-[0_0_8px_rgba(59,130,246,0.2)]',
  ANALYZE: 'bg-purple-500/10 border-purple-500/40 text-purple-300 shadow-[0_0_8px_rgba(168,85,247,0.2)]',
  PLAN: 'bg-indigo-500/10 border-indigo-500/40 text-indigo-300 shadow-[0_0_8px_rgba(99,102,241,0.2)]',
  ACT: 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300 shadow-[0_0_8px_rgba(16,185,129,0.2)]',
  EVALUATE: 'bg-amber-500/10 border-amber-500/40 text-amber-300 shadow-[0_0_8px_rgba(245,158,11,0.2)]',
  ADAPT: 'bg-rose-500/10 border-rose-500/40 text-rose-300 shadow-[0_0_8px_rgba(244,63,94,0.2)]',
  VERIFY: 'bg-teal-500/10 border-teal-500/40 text-teal-300 shadow-[0_0_8px_rgba(20,184,166,0.2)]',
};

export default function AgentTimeline({ stepHistory }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  if (!stepHistory || stepHistory.length === 0) {
    return (
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-blue-900/30 rounded-2xl p-8 text-center text-gray-500 shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
        <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-2xl w-fit mx-auto mb-3 text-blue-400">
          <Terminal className="w-8 h-8" />
        </div>
        <p className="font-semibold text-sm text-gray-300">Agent Loop Standing By</p>
        <p className="text-xs text-gray-500 mt-1">Click "Run Demo Scenario" to launch the live autonomous loop.</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-blue-900/40 rounded-2xl p-5 shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
      <div className="flex items-center justify-between mb-5 border-b border-gray-800/80 pb-3.5">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-400">
            <Terminal className="w-4 h-4" />
          </div>
          <h2 className="font-bold text-gray-100 text-sm tracking-wide">Autonomous Agent Loop Execution Timeline</h2>
        </div>
        <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2.5 py-0.5 rounded-full">
          {stepHistory.length} Steps Recorded
        </span>
      </div>

      <div className="relative pl-6 space-y-4 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-gradient-to-b before:from-blue-500 before:via-purple-500 before:to-emerald-500">
        {stepHistory.map((step, idx) => {
          const isExpanded = expandedIndex === idx;
          const phase = step.phase || 'OBSERVE';

          return (
            <div key={idx} className="relative group">
              
              {/* Dot Icon */}
              <div className={`absolute -left-6 top-1 w-5 h-5 rounded-full border flex items-center justify-center bg-[#0F172A] transition-transform group-hover:scale-110 ${
                step.status === 'failure' ? 'border-red-500 text-red-400 shadow-[0_0_10px_rgba(239,68,68,0.5)]' :
                step.status === 'warning' ? 'border-amber-500 text-amber-400 shadow-[0_0_10px_rgba(245,158,11,0.5)]' :
                step.status === 'success' ? 'border-emerald-500 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'border-blue-500 text-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.5)]'
              }`}>
                {PHASE_ICONS[phase] || <Eye className="w-3 h-3" />}
              </div>

              {/* Step Card */}
              <div className={`border rounded-xl p-3.5 transition-all duration-200 ${
                step.status === 'failure' ? 'bg-red-950/20 border-red-800/60 shadow-[0_0_15px_rgba(239,68,68,0.1)]' :
                step.status === 'warning' ? 'bg-amber-950/20 border-amber-800/60 shadow-[0_0_15px_rgba(245,158,11,0.1)]' : 'bg-gray-900/70 border-gray-800 hover:border-gray-700'
              }`}>
                
                {/* Header Row */}
                <div className="flex items-center justify-between gap-2 cursor-pointer" onClick={() => setExpandedIndex(isExpanded ? null : idx)}>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-md border font-mono ${PHASE_COLORS[phase]}`}>
                      {phase}
                    </span>
                    {step.tool_called && (
                      <span className="text-xs font-mono text-cyan-300 bg-cyan-950/60 border border-cyan-800/60 px-2.5 py-0.5 rounded-md">
                        tool: {step.tool_called}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 text-xs text-gray-400 font-mono">
                    <span>Step #{step.step_number || idx + 1}</span>
                    {isExpanded ? <ChevronDown className="w-4 h-4 text-cyan-400" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}
                  </div>
                </div>

                {/* Thought Text */}
                <div className="mt-2 text-xs text-gray-200 leading-relaxed font-sans font-medium">
                  {step.thought}
                </div>

                {/* Simulation Failure Callout */}
                {step.status === 'failure' && (
                  <div className="mt-2.5 text-xs bg-red-900/30 border border-red-700/60 text-red-300 p-2.5 rounded-lg font-mono flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-400 animate-ping"></span>
                    <span>⚠️ SERVICE FAILURE DETECTED DURING SIMULATION WORKLOAD</span>
                  </div>
                )}

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="mt-3.5 pt-3 border-t border-gray-800/80 text-xs font-mono space-y-2.5">
                    {step.tool_args && (
                      <div>
                        <span className="text-gray-400 block mb-1 text-[11px]">Tool Arguments:</span>
                        <pre className="bg-[#0B0F19] p-2.5 rounded-lg border border-gray-800 text-emerald-400 overflow-x-auto text-[11px] shadow-inner">
                          {JSON.stringify(step.tool_args, null, 2)}
                        </pre>
                      </div>
                    )}
                    {step.observation && (
                      <div>
                        <span className="text-gray-400 block mb-1 text-[11px]">Observation Output:</span>
                        <pre className="bg-[#0B0F19] p-2.5 rounded-lg border border-gray-800 text-cyan-300 overflow-x-auto text-[11px] max-h-48 shadow-inner">
                          {JSON.stringify(step.observation, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}

              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
}
