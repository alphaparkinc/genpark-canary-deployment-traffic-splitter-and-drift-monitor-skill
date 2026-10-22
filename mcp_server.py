"""MCP server for Canary Deployment Traffic Splitter & Drift Monitor."""
import sys
import json
from client import CanaryTrafficSplitter

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "evaluate_canary_deployment",
                "description": "Calculates error drift between baseline and canary models to trigger rollbacks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "baseline_errors": {"type": "integer"},
                        "baseline_total": {"type": "integer"},
                        "canary_errors": {"type": "integer"},
                        "canary_total": {"type": "integer"},
                        "max_allowed_error_drift": {"type": "number"}
                    },
                    "required": ["baseline_errors", "baseline_total", "canary_errors", "canary_total"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "evaluate_canary_deployment":
            args = params.get("arguments", {})
            res = CanaryTrafficSplitter.evaluate_canary_traffic(
                int(args.get("baseline_errors", 0)),
                int(args.get("baseline_total", 1)),
                int(args.get("canary_errors", 0)),
                int(args.get("canary_total", 1)),
                float(args.get("max_allowed_error_drift", 0.05))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
