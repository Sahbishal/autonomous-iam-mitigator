import React from 'react';
import { Award, CheckCircle, X, Shield, ArrowRight, Activity, AlertTriangle } from 'lucide-react';

export default function EvaluationReportModal({ evaluation, onClose }) {
  if (!evaluation) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#111827] border border-gray-800 rounded-xl max-w-2xl w-full p-6 shadow-2xl relative">
        
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-200"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 border-b border-gray-800 pb-4 mb-5">
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400">
            <Award className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-gray-100">Hackathon Evaluation Report</h2>
              <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-xs font-mono font-bold">
                {evaluation.verdict}
              </span>
            </div>
            <p className="text-xs text-gray-400">Autonomous Cloud IAM Least-Privilege Mitigator Assessment</p>
          </div>
        </div>

        {/* Summary Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5 font-mono text-center">
          <div className="bg-gray-900/80 p-3 rounded-lg border border-gray-800">
            <span className="text-[10px] text-gray-400 uppercase block">Security Score</span>
            <span className="text-xl font-bold text-emerald-400">+{evaluation.security_improvement_pct}%</span>
          </div>
          <div className="bg-gray-900/80 p-3 rounded-lg border border-gray-800">
            <span className="text-[10px] text-gray-400 uppercase block">Functionality</span>
            <span className="text-xl font-bold text-emerald-400">{evaluation.final_functionality_score}%</span>
          </div>
          <div className="bg-gray-900/80 p-3 rounded-lg border border-gray-800">
            <span className="text-[10px] text-gray-400 uppercase block">Sim Failures</span>
            <span className="text-xl font-bold text-amber-400">{evaluation.simulation_failures_encountered}</span>
          </div>
          <div className="bg-gray-900/80 p-3 rounded-lg border border-gray-800">
            <span className="text-[10px] text-gray-400 uppercase block">Adaptations</span>
            <span className="text-xl font-bold text-blue-400">{evaluation.replanning_iterations}</span>
          </div>
        </div>

        {/* Permissions Breakdown */}
        <div className="space-y-3 text-xs mb-5 font-mono">
          <div className="bg-gray-900 p-3 rounded-lg border border-gray-800">
            <span className="text-red-400 font-bold block mb-1">Permissions Removed ({evaluation.permissions_removed?.length}):</span>
            <div className="flex flex-wrap gap-1">
              {evaluation.permissions_removed?.map((p, i) => (
                <span key={i} className="bg-red-950 text-red-300 border border-red-800 px-2 py-0.5 rounded text-[11px]">
                  {p}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 p-3 rounded-lg border border-gray-800">
            <span className="text-amber-300 font-bold block mb-1">Permissions Preserved via Dependency Recovery ({evaluation.permissions_preserved?.length}):</span>
            <div className="flex flex-wrap gap-1">
              {evaluation.permissions_preserved?.map((p, i) => (
                <span key={i} className="bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded text-[11px]">
                  {p} (ImageProcessingService)
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Narrative Summary */}
        <div className="bg-gray-900 p-4 rounded-lg border border-gray-800 text-xs text-gray-300 leading-relaxed mb-6 font-sans">
          <strong className="text-gray-100 block mb-1 font-mono">Agent Performance Summary:</strong>
          {evaluation.summary}
        </div>

        {/* Action Button */}
        <div className="flex justify-end">
          <button 
            onClick={onClose}
            className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition"
          >
            Close Report
          </button>
        </div>

      </div>
    </div>
  );
}
