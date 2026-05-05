import json
import re
from typing import Any, Dict, List

from services.llm import call_llm


class AnalyzerAgent:
    """Extracts threat type, entities, and risk indicators from text."""

    THREAT_KEYWORDS = {
        "ransomware": ["ransomware", "encrypt files", "ransom note", "double extortion"],
        "phishing": ["phishing", "credential theft", "spoofed login", "business email compromise"],
        "data breach": ["data breach", "exfiltration", "leaked database", "stolen records"],
        "malware": ["malware", "trojan", "loader", "backdoor", "infostealer"],
        "ddos": ["ddos", "denial of service", "botnet traffic", "traffic flood"],
        "vulnerability": ["cve-", "remote code execution", "zero-day", "privilege escalation", "patch"],
        "apt": ["apt", "nation-state", "advanced persistent threat"],
    }

    INDICATOR_KEYWORDS = [
        "cve-",
        "zero-day",
        "rce",
        "exploit",
        "payload",
        "ioc",
        "indicator of compromise",
        "command and control",
        "lateral movement",
        "credential dumping",
        "data exfiltration",
        "botnet",
        "malspam",
    ]

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

        normalized_entities = entities if isinstance(entities, list) else []
        normalized_indicators = indicators if isinstance(indicators, list) else []
        normalized_type = str(threat_type).strip().lower() or "unknown"

        # If model output is weak, enrich with deterministic text heuristics.
        if normalized_type == "unknown":
            normalized_type = self._detect_threat_type(text)
        if not normalized_indicators:
            normalized_indicators = self._extract_indicators(text)
        if not normalized_entities:
            normalized_entities = self._extract_entities(text)

        confidence = self._estimate_confidence(
            indicators=normalized_indicators,
            entities=normalized_entities,
            threat_type=normalized_type,
            text=text,
        )

        return {
            "threat_type": normalized_type,
            "entities": normalized_entities,
            "risk_indicators": normalized_indicators,
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

    def _detect_threat_type(self, text: str) -> str:
        lower_text = text.lower()
        best_type = "unknown"
        best_hits = 0

        for threat_type, keywords in self.THREAT_KEYWORDS.items():
            hits = sum(1 for keyword in keywords if keyword in lower_text)
            if hits > best_hits:
                best_type = threat_type
                best_hits = hits

        return best_type

    def _extract_indicators(self, text: str) -> List[str]:
        lower_text = text.lower()
        indicators = [keyword for keyword in self.INDICATOR_KEYWORDS if keyword in lower_text]

        cve_matches = re.findall(r"\bcve-\d{4}-\d{4,7}\b", lower_text)
        indicators.extend(cve_matches)

        return sorted(set(indicators))

    def _extract_entities(self, text: str) -> List[str]:
        entity_matches = re.findall(r"\b[A-Z][A-Za-z0-9._-]{2,}\b", text)
        return sorted(set(entity_matches[:8]))

    def _estimate_confidence(self, indicators: List[str], entities: List[str], threat_type: str, text: str) -> float:
        base = 0.25
        indicator_bonus = min(0.1 * len(indicators), 0.45)
        entity_bonus = min(0.04 * len(entities), 0.2)
        threat_bonus = 0.12 if threat_type != "unknown" else 0.0
        text_signal_bonus = min(len(text.split()) / 400.0, 0.12)
        return round(min(base + indicator_bonus + entity_bonus + threat_bonus + text_signal_bonus, 0.95), 2)
