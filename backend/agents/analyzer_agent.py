import json
from typing import Any, Dict, List

from services.llm import call_llm


class AnalyzerAgent:
    """Extracts threat type, entities, and risk indicators from text."""

    def analyze(self, text: str, transparency_note: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        system_role = (
            "You are an AI threat analysis engine. "
            "Return strict JSON only with keys: threat_type, entities, risk_indicators."
        )

        output = call_llm(prompt=prompt, system_role=system_role)
        parsed = self._parse_output(output)

        entities = parsed.get("entities", [])
        indicators = parsed.get("risk_indicators", [])
        threat_type = parsed.get("threat_type", "unknown")
        confidence = self._estimate_confidence(indicators)

        return {
            "threat_type": threat_type,
            "entities": entities if isinstance(entities, list) else [],
            "risk_indicators": indicators if isinstance(indicators, list) else [],
            "confidence_score": confidence,
            "transparency_note": transparency_note,
        }

    def _build_prompt(self, text: str) -> str:
        return (
            "Analyze this cybersecurity text and return JSON only.\\n"
            "Output format:\\n"
            "{\\n"
            '  "threat_type": "string",\\n'
            '  "entities": ["string"],\\n'
            '  "risk_indicators": ["string"]\\n'
            "}\\n"
            f"Text: {text}"
        )

    def _parse_output(self, raw_output: str) -> Dict[str, Any]:
        if not raw_output:
            return self._fallback_analysis()

        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return self._fallback_analysis()

    def _fallback_analysis(self) -> Dict[str, Any]:
        return {
            "threat_type": "unknown",
            "entities": [],
            "risk_indicators": [],
        }

    def _estimate_confidence(self, indicators: List[str]) -> float:
        base = 0.35
        bonus = min(0.12 * len(indicators), 0.55)
        return round(min(base + bonus, 0.95), 2)
