import React from 'react';
import { Shield, CheckCircle2, Lock, Activity, TrendingUp, Zap } from 'lucide-react';

export default function OverviewCards({ state, evaluation }) {
  const initialRisk = state?.initial_risk_score ?? 0;
  const currentRisk = state?.current_risk_score ?? 0;
  const initialFunc = state?.initial_functionality_score ?? 100;
  const currentFunc = state?.current_functionality_score ?? 100;

  const initialPermCount = state?.initial_permissions?.length ?? 6;
  const currentPermCount = state?.current_permissions?.length ?? 6;
  const permsRemoved = initialPermCount - currentPermCount;

  const riskReduction = Math.max(0, currentRisk - initialRisk);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
      
      {/* Card 1: Security Risk Score */}
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-blue-900/40 hover:border-blue-500/50 rounded-2xl p-5 flex flex-col justify-between shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-all duration-300 hover:shadow-[0_0_25px_rgba(59,130,246,0.15)] group">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-blue-400 font-mono">Security Score</span>
          <div className="p-2.5 bg-blue-500/10 border border-blue-500/30 rounded-xl text-blue-400 group-hover:scale-110 transition-transform">
            <Shield className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-extrabold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">{currentRisk.toFixed(1)}</span>
            <span className="text-xs text-gray-400 font-mono">/ 100</span>
          </div>
          <div className="flex items-center gap-1.5 mt-1.5 text-xs text-emerald-400 font-semibold font-mono">
            <TrendingUp className="w-3.5 h-3.5" />
            <span>+{riskReduction.toFixed(1)}% improvement</span>
          </div>
        </div>
        <div className="w-full bg-gray-800/80 h-2 rounded-full mt-4 overflow-hidden p-0.5 border border-gray-700/50">
          <div className="bg-gradient-to-r from-blue-600 to-cyan-400 h-full rounded-full transition-all duration-700 shadow-[0_0_10px_rgba(6,182,212,0.5)]" style={{ width: `${Math.min(100, currentRisk)}%` }}></div>
        </div>
      </div>

      {/* Card 2: Functionality Score */}
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-emerald-900/40 hover:border-emerald-500/50 rounded-2xl p-5 flex flex-col justify-between shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-all duration-300 hover:shadow-[0_0_25px_rgba(16,185,129,0.15)] group">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-400 font-mono">Service Health</span>
          <div className={`p-2.5 rounded-xl border group-hover:scale-110 transition-transform ${currentFunc === 100 ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-amber-500/10 border-amber-500/30 text-amber-400'}`}>
            <CheckCircle2 className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-2">
            <span className={`text-4xl font-extrabold ${currentFunc === 100 ? 'bg-gradient-to-r from-emerald-200 to-teal-400 bg-clip-text text-transparent' : 'text-amber-400'}`}>
              {currentFunc.toFixed(1)}%
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-1.5 font-medium">100% service health constraint</p>
        </div>
        <div className="w-full bg-gray-800/80 h-2 rounded-full mt-4 overflow-hidden p-0.5 border border-gray-700/50">
          <div className={`h-full rounded-full transition-all duration-700 ${currentFunc === 100 ? 'bg-gradient-to-r from-emerald-500 to-teal-300 shadow-[0_0_10px_rgba(20,184,166,0.5)]' : 'bg-amber-500'}`} style={{ width: `${currentFunc}%` }}></div>
        </div>
      </div>

      {/* Card 3: Permissions Mitigated */}
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-purple-900/40 hover:border-purple-500/50 rounded-2xl p-5 flex flex-col justify-between shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-all duration-300 hover:shadow-[0_0_25px_rgba(139,92,246,0.15)] group">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-purple-400 font-mono">IAM Privileges</span>
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/30 rounded-xl text-purple-400 group-hover:scale-110 transition-transform">
            <Lock className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-white">{currentPermCount}</span>
            <span className="text-xs text-gray-400 font-mono">from {initialPermCount} initial</span>
          </div>
          <p className="text-xs text-purple-400 mt-1.5 font-semibold font-mono">
            {permsRemoved > 0 ? `${permsRemoved} excessive permissions removed` : 'Baseline active privileges'}
          </p>
        </div>
        <div className="w-full bg-gray-800/80 h-2 rounded-full mt-4 overflow-hidden p-0.5 border border-gray-700/50">
          <div className="bg-gradient-to-r from-purple-600 to-pink-400 h-full rounded-full transition-all duration-700 shadow-[0_0_10px_rgba(217,70,239,0.5)]" style={{ width: `${(currentPermCount / Math.max(1, initialPermCount)) * 100}%` }}></div>
        </div>
      </div>

      {/* Card 4: Agent Loop Status */}
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-cyan-900/40 hover:border-cyan-500/50 rounded-2xl p-5 flex flex-col justify-between shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-all duration-300 hover:shadow-[0_0_25px_rgba(6,182,212,0.15)] group">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-400 font-mono">Agent Status</span>
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400 group-hover:scale-110 transition-transform">
            <Activity className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-center gap-2.5">
            <span className={`w-3 h-3 rounded-full ${
              state?.status === 'running' ? 'bg-amber-400 animate-ping' :
              state?.status === 'completed' ? 'bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.8)]' : 'bg-gray-500'
            }`}></span>
            <span className="text-xl font-bold text-white capitalize tracking-tight">
              {state?.status || 'Idle / Ready'}
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-1.5 font-medium">
            {state?.verification_passed ? '✓ Policy verified & applied' : 'Ready to execute agentic loop'}
          </p>
        </div>
        <div className="text-[11px] text-cyan-400 font-mono mt-4 flex items-center justify-between pt-2 border-t border-gray-800/60">
          <span>Iter: <strong>{state?.iteration ?? 0}</strong></span>
          <span className="flex items-center gap-1"><Zap className="w-3 h-3" /> Recoveries: <strong>{evaluation?.simulation_failures_encountered ?? 0}</strong></span>
        </div>
      </div>

    </div>
  );
}
