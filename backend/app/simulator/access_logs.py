import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from backend.app.models.iam import AccessLog

class AccessLogEngine:
    """
    Generates and queries 30-90 days of synthetic cloud access logs.
    Includes direct user activity and service-to-service execution logs.
    """
    def __init__(self):
        self.logs: List[AccessLog] = []
        self._generate_synthetic_logs()

    def _generate_synthetic_logs(self):
        """Generates realistic access logs over the last 60 days."""
        self.logs.clear()
        now = datetime.now()

        # Generate logs for Developer role (Scenario B context)
        # 1. Direct User calls (Alice)
        # database.read (45 calls)
        for i in range(45):
            dt = now - timedelta(days=random.randint(1, 59), hours=random.randint(0, 23))
            self.logs.append(AccessLog(
                timestamp=dt.isoformat(),
                user="Alice",
                role="Developer",
                permission="database.read",
                resource="Database",
                action="read",
                status="success",
                service="DirectUser",
                source="10.0.1.42"
            ))

        # database.write (30 calls)
        for i in range(30):
            dt = now - timedelta(days=random.randint(1, 59), hours=random.randint(0, 23))
            self.logs.append(AccessLog(
                timestamp=dt.isoformat(),
                user="Alice",
                role="Developer",
                permission="database.write",
                resource="Database",
                action="write",
                status="success",
                service="DirectUser",
                source="10.0.1.42"
            ))

        # storage.write (22 calls)
        for i in range(22):
            dt = now - timedelta(days=random.randint(1, 59), hours=random.randint(0, 23))
            self.logs.append(AccessLog(
                timestamp=dt.isoformat(),
                user="Alice",
                role="Developer",
                permission="storage.write",
                resource="ObjectStorage",
                action="write",
                status="success",
                service="DirectUser",
                source="10.0.1.42"
            ))

        # 2. Service-to-service indirect calls executed under Developer workflow
        # ImageProcessingService invoking storage.read on behalf of Developer app (120 calls)
        for i in range(120):
            dt = now - timedelta(days=random.randint(1, 59), hours=random.randint(0, 23))
            self.logs.append(AccessLog(
                timestamp=dt.isoformat(),
                user="Alice",
                role="Developer",
                permission="storage.read",
                resource="ObjectStorage",
                action="read",
                status="success",
                service="ImageProcessingService",
                source="10.0.2.105"
            ))

        # Note: ZERO direct calls for storage.delete and iam.modify!

        # Sort logs by timestamp
        self.logs.sort(key=lambda x: x.timestamp)

    def get_logs_for_role(self, role_id: str, days: int = 90) -> List[AccessLog]:
        """Returns log entries for a given role within the specified lookback days."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        return [log for log in self.logs if log.role == role_id and log.timestamp >= cutoff]

    def analyze_role_usage(self, role_id: str, days: int = 90) -> Dict[str, Dict[str, Any]]:
        """
        Analyzes log history for a role.
        Returns detailed stats per permission: direct_calls, service_calls, total_calls, services.
        """
        role_logs = self.get_logs_for_role(role_id, days)
        usage_stats: Dict[str, Dict[str, Any]] = {}

        for log in role_logs:
            perm = log.permission
            if perm not in usage_stats:
                usage_stats[perm] = {
                    "direct_calls": 0,
                    "service_calls": 0,
                    "total_calls": 0,
                    "services": set(),
                    "last_used": log.timestamp
                }

            if log.service == "DirectUser":
                usage_stats[perm]["direct_calls"] += 1
            else:
                usage_stats[perm]["service_calls"] += 1
                usage_stats[perm]["services"].add(log.service)

            usage_stats[perm]["total_calls"] += 1
            if log.timestamp > usage_stats[perm]["last_used"]:
                usage_stats[perm]["last_used"] = log.timestamp

        # Format services sets as lists for JSON serialization
        for perm in usage_stats:
            usage_stats[perm]["services"] = list(usage_stats[perm]["services"])

        return usage_stats
