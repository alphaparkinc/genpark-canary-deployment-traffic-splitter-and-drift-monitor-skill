"""Example usage for Canary Deployment Traffic Splitter & Drift Monitor."""
from client import CanaryTrafficSplitter

if __name__ == "__main__":
    res = CanaryTrafficSplitter.evaluate_canary_traffic(2, 100, 15, 100)
    print("Canary Decision:", res["canary_decision"], "Rollback:", res["rollback_recommended"])
