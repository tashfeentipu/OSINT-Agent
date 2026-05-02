from typing import Any, Dict


class RiskAgent:
    """Simple rule-based risk scoring from analysis output."""

    def assess(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        threat_type = str(analysis.get("threat_type", "unknown")).lower()
        indicators = analysis.get("risk_indicators", [])

        score = 0
        score += len(indicators) * 2

        if threat_type in {"ransomware", "data breach", "zero-day", "apt"}:
            score += 5
        elif threat_type in {"phishing", "malware", "ddos", "vulnerability"}:
            score += 3
        else:
            score += 1

        if score >= 10:
            level = "High"
        elif score >= 6:
            level = "Medium"
        else:
            level = "Low"

        confidence = min(0.5 + (score * 0.04), 0.98)
        return {
            "risk_level": level,
            "confidence_score": round(confidence, 2),
        }
