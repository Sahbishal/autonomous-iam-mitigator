const API_BASE = 'http://localhost:8000/api';

export async function fetchEnvironment() {
  const res = await fetch(`${API_BASE}/environment`);
  if (!res.ok) throw new Error('Failed to fetch environment state');
  return res.json();
}

export async function fetchRoleDetails(roleId) {
  const res = await fetch(`${API_BASE}/roles/${roleId}`);
  if (!res.ok) throw new Error(`Failed to fetch role '${roleId}'`);
  return res.json();
}

export async function fetchScenarios() {
  const res = await fetch(`${API_BASE}/scenarios`);
  if (!res.ok) throw new Error('Failed to fetch scenarios');
  return res.json();
}

export async function resetEnvironment() {
  const res = await fetch(`${API_BASE}/environment/reset`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to reset environment');
  return res.json();
}

export async function runAgentSync(scenarioId = 'scenario_b', roleId = 'Developer') {
  const res = await fetch(`${API_BASE}/agent/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: scenarioId, role_id: roleId })
  });
  if (!res.ok) throw new Error('Failed to run agent');
  return res.json();
}

export function subscribeAgentStream(sessionId, scenarioId = 'scenario_b', roleId = 'Developer', onStep, onComplete, onError) {
  const url = `${API_BASE}/agent/stream/${sessionId}?scenario_id=${scenarioId}&role_id=${roleId}`;
  const eventSource = new EventSource(url);

  eventSource.addEventListener('step', (e) => {
    try {
      const data = JSON.parse(e.data);
      if (onStep) onStep(data);
    } catch (err) {
      console.error("Error parsing step data", err);
    }
  });

  eventSource.addEventListener('complete', (e) => {
    try {
      const data = JSON.parse(e.data);
      if (onComplete) onComplete(data);
      eventSource.close();
    } catch (err) {
      console.error("Error parsing complete data", err);
    }
  });

  eventSource.onerror = (err) => {
    console.error("SSE Connection error", err);
    if (onError) onError(err);
    eventSource.close();
  };

  return () => eventSource.close();
}
