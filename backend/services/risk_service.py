from typing import Dict, List


class RiskScoringService:
    """Converts detections into normalized risk scores."""

    CATEGORY_WEIGHT = {
        "malware": 25,
        "phishing": 20,
        "vulnerability": 22,
        "data-breach": 28,
        "ddos": 18,
        "unknown": 8,
    }

    def score(self, matched_keywords: List[str], category: str) -> Dict[str, float | str]:
        base = self.CATEGORY_WEIGHT.get(category, self.CATEGORY_WEIGHT["unknown"])
        keyword_bonus = min(len(matched_keywords) * 6, 42)
        risk_score = float(min(base + keyword_bonus, 100))

        if risk_score >= 75:
            severity = "critical"
        elif risk_score >= 55:
            severity = "high"
        elif risk_score >= 35:
            severity = "medium"
        else:
            severity = "low"

        return {"risk_score": risk_score, "severity": severity}
