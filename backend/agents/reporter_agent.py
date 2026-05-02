import json
from typing import Any, Dict

from services.llm import call_llm


class ReporterAgent:
    """Builds business-friendly summaries and actions."""

    def report(self, source: str, analysis: Dict[str, Any], risk: Dict[str, Any]) -> Dict[str, str]:
        prompt = self._build_prompt(source=source, analysis=analysis, risk=risk)
        system_role = (
            "You are an executive cyber risk reporter. "
            "Return strict JSON only with keys: summary, recommended_action."
        )
        output = call_llm(prompt=prompt, system_role=system_role)

        parsed = self._parse_output(output)
        if parsed:
            return parsed

        return {
            "summary": f"Potential {analysis.get('threat_type', 'cyber')} activity detected from {source}.",
            "recommended_action": "Monitor updates, validate exposure, and escalate to SOC if indicators match internal telemetry.",
        }

    def _build_prompt(self, source: str, analysis: Dict[str, Any], risk: Dict[str, Any]) -> str:
        analysis_json = json.dumps(analysis)
        risk_json = json.dumps(risk)
        return (
            "Generate business-friendly threat report as JSON only.\\n"
            "Output format:\\n"
            "{\\n"
            '  "summary": "string",\\n'
            '  "recommended_action": "string"\\n'
            "}\\n"
            f"Source: {source}\\n"
            f"Analysis: {analysis_json}\\n"
            f"Risk: {risk_json}"
        )

    def _parse_output(self, output: str) -> Dict[str, str]:
        if not output:
            return {}

        try:
            data = json.loads(output)
            summary = data.get("summary")
            recommended_action = data.get("recommended_action")
            if isinstance(summary, str) and isinstance(recommended_action, str):
                return {
                    "summary": summary,
                    "recommended_action": recommended_action,
                }
        except json.JSONDecodeError:
            return {}
        return {}
