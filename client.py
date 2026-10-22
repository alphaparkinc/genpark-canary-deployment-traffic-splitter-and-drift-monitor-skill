"""Canary Deployment Traffic Splitter & Drift Monitor.
100% Python Standard Library.
"""

class CanaryTrafficSplitter:
    """Splits agent traffic across baseline and canary models, monitoring output divergence and error spike drift."""

    @staticmethod
    def evaluate_canary_traffic(baseline_errors: int, baseline_total: int, canary_errors: int, canary_total: int, max_allowed_error_drift: float = 0.05) -> dict:
        base_rate = (baseline_errors / max(1, baseline_total))
        canary_rate = (canary_errors / max(1, canary_total))
        drift = canary_rate - base_rate

        rollback = drift > max_allowed_error_drift
        decision = "ROLLBACK_CANARY" if rollback else ("PROMOTE_CANARY" if canary_rate <= base_rate else "CONTINUE_CANARY")

        return {
            "baseline_error_rate": round(base_rate, 4),
            "canary_error_rate": round(canary_rate, 4),
            "error_rate_drift": round(drift, 4),
            "rollback_recommended": rollback,
            "canary_decision": decision
        }
