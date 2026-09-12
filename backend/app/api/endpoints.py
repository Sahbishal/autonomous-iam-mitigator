import json
import asyncio
import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.access_logs import AccessLogEngine
from backend.app.simulator.dependency_graph import CloudDependencyGraph
from backend.app.simulator.policy_simulator import PolicySimulator
from backend.app.agent.loop import AgentOrchestrator

router = APIRouter(prefix="/api")

# Shared singletons for synthetic cloud simulation
env = SyntheticCloudEnvironment()
log_engine = AccessLogEngine()
dep_graph = CloudDependencyGraph(env)
simulator = PolicySimulator(env, dep_graph)
orchestrator = AgentOrchestrator(env, log_engine, dep_graph, simulator)

# Active streaming sessions
sessions_data: Dict[str, Dict[str, Any]] = {}
session_queues: Dict[str, asyncio.Queue] = {}

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Autonomous Cloud IAM Least-Privilege Mitigator API", "version": "1.0.0"}

@router.get("/environment")
def get_environment_state():
    roles = [r.dict() for r in env.list_roles()]
    deps = [d.dict() for d in env.dependencies]
    perms = [p.dict() for p in env.permissions.values()]
    graph = dep_graph.get_full_graph_structure()
    return {
        "roles": roles,
        "permissions": perms,
        "dependencies": deps,
        "graph": graph
    }

@router.get("/roles/{role_id}")
def get_role_details(role_id: str, days: int = 90):
    role = env.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")
    
    analytics = log_engine.analyze_role_usage(role_id, days)
    logs = [l.dict() for l in log_engine.get_logs_for_role(role_id, days)]
    
    perm_details = []
    for pid in role.permissions:
        p = env.get_permission(pid)
        if p:
            impact = dep_graph.get_permission_impact(pid)
            usage = analytics.get(pid, {"direct_calls": 0, "service_calls": 0, "total_calls": 0})
            perm_details.append({
                "permission": p.dict(),
                "usage": usage,
                "dependency_impact": impact
            })

    return {
        "role": role.dict(),
        "permissions_count": len(role.permissions),
        "permission_details": perm_details,
        "access_logs_count": len(logs),
        "access_analytics": analytics
    }

@router.get("/scenarios")
def get_scenarios():
    return [
        {
            "id": "scenario_a",
            "name": "Scenario A: Direct Safe Removal",
            "role_id": "Developer",
            "description": "Unused permissions can safely be removed with 0 service dependencies.",
            "difficulty": "Easy"
        },
        {
            "id": "scenario_b",
            "name": "Scenario B: Hidden Service Dependency Failure & Recovery (Core Demo)",
            "role_id": "Developer",
            "description": "storage.read has 0 direct user activity, but is a critical dependency for ImageProcessingService. Agent initially proposes removal, detects simulation failure, inspects dependency, adapts policy, and passes verification.",
            "difficulty": "Mandatory Hackathon Demo"
        },
        {
            "id": "scenario_c",
            "name": "Scenario C: Multi-Stage Replanning & Dynamic Discovery",
            "role_id": "Developer",
            "description": "Complex multi-stage candidate evaluation with multi-service dependency checking.",
            "difficulty": "Advanced"
        }
    ]

@router.post("/environment/reset")
def reset_environment():
    env.reset()
    dep_graph.build_graph()
    log_engine._generate_synthetic_logs()
    return {"status": "success", "message": "Synthetic cloud environment reset to baseline seed state."}

@router.post("/agent/run")
def run_agent(payload: Dict[str, Any]):
    scenario_id = payload.get("scenario_id", "scenario_b")
    role_id = payload.get("role_id", "Developer")
    session_id = payload.get("session_id", f"session_{uuid.uuid4().hex[:8]}")

    env.reset()
    dep_graph.build_graph()

    result = orchestrator.run_agent_loop(
        session_id=session_id,
        scenario_id=scenario_id,
        role_id=role_id
    )

    sessions_data[session_id] = result
    return {"session_id": session_id, "result": result}

@router.get("/agent/stream/{session_id}")
async def stream_agent(session_id: str, request: Request, scenario_id: str = "scenario_b", role_id: str = "Developer"):
    """
    Server-Sent Events (SSE) endpoint for real-time agent execution visualizer.
    """
    async def event_generator():
        q = asyncio.Queue()
        session_queues[session_id] = q

        loop = asyncio.get_event_loop()

        def sync_callback(step_data):
            loop.call_soon_threadsafe(q.put_nowait, step_data)

        # Run agent in background executor
        def execute_agent():
            env.reset()
            dep_graph.build_graph()
            res = orchestrator.run_agent_loop(
                session_id=session_id,
                scenario_id=scenario_id,
                role_id=role_id,
                callback=sync_callback
            )
            loop.call_soon_threadsafe(q.put_nowait, {"type": "COMPLETE", "result": res})

        loop.run_in_executor(None, execute_agent)

        while True:
            if await request.is_disconnected():
                break

            try:
                data = await asyncio.wait_for(q.get(), timeout=1.0)
                if isinstance(data, dict) and data.get("type") == "COMPLETE":
                    yield f"event: complete\ndata: {json.dumps(data['result'])}\n\n"
                    break
                else:
                    yield f"event: step\ndata: {json.dumps(data)}\n\n"
            except asyncio.TimeoutError:
                yield f"event: ping\ndata: {{}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/simulator/simulate")
def manual_simulate(payload: Dict[str, Any]):
    role_id = payload.get("role_id", "Developer")
    permissions = payload.get("permissions", [])
    version_id = payload.get("version_id", "manual_v1")

    res = simulator.simulate_role_policy(role_id, permissions, version_id)
    return res.dict()
