import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import OverviewCards from './components/OverviewCards';
import AgentTimeline from './components/AgentTimeline';
import PolicyMatrix from './components/PolicyMatrix';
import DependencyGraphView from './components/DependencyGraphView';
import SimulationConsole from './components/SimulationConsole';
import EvaluationReportModal from './components/EvaluationReportModal';

import { 
  fetchEnvironment, 
  fetchRoleDetails, 
  resetEnvironment, 
  subscribeAgentStream 
} from './services/api';

export default function App() {
  const [activeScenario, setActiveScenario] = useState('scenario_b');
  const [roleDetails, setRoleDetails] = useState(null);
  const [envState, setEnvState] = useState(null);
  const [agentState, setAgentState] = useState(null);
  const [stepHistory, setStepHistory] = useState([]);
  const [simulations, setSimulations] = useState([]);
  const [evidenceList, setEvidenceList] = useState([]);
  const [evaluation, setEvaluation] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [showEvalModal, setShowEvalModal] = useState(false);

  // Load initial data
  const loadData = async () => {
    try {
      const [envData, roleData] = await Promise.all([
        fetchEnvironment(),
        fetchRoleDetails('Developer')
      ]);
      setEnvState(envData);
      setRoleDetails(roleData);
    } catch (err) {
      console.error("Failed to load environment state:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleReset = async () => {
    try {
      await resetEnvironment();
      setAgentState(null);
      setStepHistory([]);
      setSimulations([]);
      setEvidenceList([]);
      setEvaluation(null);
      await loadData();
    } catch (err) {
      console.error("Failed to reset:", err);
    }
  };

  const handleRunDemo = () => {
    setIsRunning(true);
    setStepHistory([]);
    setSimulations([]);
    setEvidenceList([]);
    setEvaluation(null);

    const sessionId = `demo_${Date.now()}`;

    subscribeAgentStream(
      sessionId,
      activeScenario,
      'Developer',
      (stepData) => {
        setStepHistory(prev => [...prev, stepData]);
        if (stepData.observation?.simulation) {
          setSimulations(prev => [...prev, stepData.observation.simulation]);
        }
      },
      async (resultData) => {
        setIsRunning(false);
        if (resultData?.state) {
          setAgentState(resultData.state);
          setSimulations(resultData.state.simulation_history || []);
          setEvidenceList(resultData.state.evidence_list || []);
        }
        if (resultData?.evaluation_report) {
          setEvaluation(resultData.evaluation_report);
          setShowEvalModal(true);
        }
        await loadData();
      },
      (err) => {
        setIsRunning(false);
        console.error("Streaming error:", err);
      }
    );
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 flex flex-col font-sans relative overflow-x-hidden">
      
      {/* High-Tech Background Glows */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[350px] bg-blue-600/10 blur-[130px] rounded-full pointer-events-none"></div>
      <div className="absolute top-1/3 right-10 w-[500px] h-[400px] bg-cyan-500/10 blur-[140px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-10 left-10 w-[400px] h-[400px] bg-purple-600/10 blur-[120px] rounded-full pointer-events-none"></div>

      {/* Header Navbar */}
      <Navbar 
        onRunDemo={handleRunDemo}
        onSelectScenario={setActiveScenario}
        activeScenario={activeScenario}
        isRunning={isRunning}
        onReset={handleReset}
      />

      {/* Main Dashboard Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6 relative z-10">
        
        {/* Executive Metric Cards */}
        <OverviewCards state={agentState} evaluation={evaluation} />

        {/* Core Layout: Grid with Agent Timeline & Interactive Modules */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column: Live Agent Loop Timeline */}
          <div className="lg:col-span-5 space-y-6">
            <AgentTimeline stepHistory={stepHistory} />
          </div>

          {/* Right Column: Policy Matrix, Dependency Graph, Simulation Console */}
          <div className="lg:col-span-7 space-y-6">
            <PolicyMatrix 
              roleDetails={roleDetails}
              evidenceList={evidenceList}
              state={agentState}
            />
            <DependencyGraphView 
              graphData={envState?.graph}
              state={agentState}
            />
            <SimulationConsole 
              simulations={simulations}
            />
          </div>

        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800/80 bg-[#070A12] py-4 text-center text-xs text-gray-500 font-mono relative z-10">
        Tech Zephyr 4.0 Hackathon • Autonomous Cloud IAM Least-Privilege Engine
      </footer>

      {/* Evaluation Report Modal */}
      {showEvalModal && (
        <EvaluationReportModal 
          evaluation={evaluation}
          onClose={() => setShowEvalModal(false)}
        />
      )}

    </div>
  );
}
