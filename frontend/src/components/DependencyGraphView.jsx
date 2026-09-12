import React from 'react';
import { Network, Server, HardDrive, Shield, AlertTriangle, ArrowRight } from 'lucide-react';

export default function DependencyGraphView({ graphData, state }) {
  const dependencies = [
    {
      source: "ImageProcessingService",
      targetResource: "ObjectStorage",
      perm: "storage.read",
      criticality: "critical",
      highlight: true,
      reason: "Worker pipeline reads source images for thumbnail generation"
    },
    {
      source: "ImageProcessingService",
      targetResource: "ObjectStorage",
      perm: "storage.write",
      criticality: "critical",
      highlight: false,
      reason: "Worker uploads converted assets back to storage"
    },
    {
      source: "PaymentService",
      targetResource: "Database",
      perm: "database.write",
      criticality: "critical",
      highlight: false,
      reason: "Records billing transactions to main database"
    },
    {
      source: "AnalyticsService",
      targetResource: "Database",
      perm: "database.read",
      criticality: "critical",
      highlight: false,
      reason: "Queries aggregated customer metrics"
    }
  ];

  return (
    <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-cyan-900/40 rounded-2xl p-5 shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800/80 pb-3.5">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-400">
            <Network className="w-4 h-4" />
          </div>
          <h2 className="font-bold text-gray-100 text-sm tracking-wide">Cloud Microservice Dependency Topology</h2>
        </div>
        <span className="text-xs font-mono text-cyan-300 bg-cyan-950/80 border border-cyan-700/60 px-2.5 py-0.5 rounded-full font-semibold shadow-[0_0_10px_rgba(6,182,212,0.2)]">
          NetworkX Topology Visualizer
        </span>
      </div>

      {/* Dependency Map Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {dependencies.map((dep, idx) => (
          <div 
            key={idx}
            className={`border rounded-xl p-4 transition-all duration-300 ${
              dep.highlight 
                ? 'bg-gradient-to-br from-amber-950/30 via-[#1E1B18] to-[#2A1E17] border-amber-500/60 shadow-[0_0_20px_rgba(245,158,11,0.2)]' 
                : 'bg-gray-900/70 border-gray-800 hover:border-gray-700'
            }`}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Server className="w-4 h-4 text-cyan-400" />
                <span className="font-extrabold text-xs text-gray-100 font-mono">{dep.source}</span>
              </div>
              {dep.highlight && (
                <span className="bg-amber-500/20 text-amber-300 border border-amber-500/50 text-[10px] font-mono px-2.5 py-0.5 rounded-full flex items-center gap-1 font-extrabold animate-pulse shadow-[0_0_8px_rgba(245,158,11,0.3)]">
                  <AlertTriangle className="w-3 h-3" /> HIDDEN DEPENDENCY
                </span>
              )}
            </div>

            {/* Path visualization */}
            <div className="flex items-center gap-2 text-xs font-mono bg-[#0B0F19] p-2.5 rounded-lg border border-gray-800/80 mb-2.5 shadow-inner">
              <span className="text-cyan-300 font-bold">{dep.source}</span>
              <ArrowRight className="w-3.5 h-3.5 text-gray-500" />
              <div className="flex items-center gap-1 text-purple-300 font-medium">
                <HardDrive className="w-3 h-3" />
                <span>{dep.targetResource}</span>
              </div>
              <ArrowRight className="w-3.5 h-3.5 text-gray-500" />
              <div className="flex items-center gap-1 text-emerald-400 font-bold">
                <Shield className="w-3 h-3" />
                <span>{dep.perm}</span>
              </div>
            </div>

            <p className="text-[11px] text-gray-300 leading-tight font-sans">
              {dep.reason}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
