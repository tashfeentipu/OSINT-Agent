from typing import Any, Dict


class RiskAgent:
    """Rule-based risk scoring from analysis output."""

    def assess(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        threat_type = str(analysis.get("threat_type", "unknown")).lower()
        indicators = analysis.get("risk_indicators", [])
        analysis_confidence = float(analysis.get("confidence_score", 0.0))

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

        # Include upstream analysis confidence so risk confidence reflects signal quality.
        confidence = min(0.3 + (score * 0.03) + (analysis_confidence * 0.4), 0.98)
        return {
            "risk_level": level,
            "confidence_score": round(confidence, 2),
        }
