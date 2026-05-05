import unittest
from unittest.mock import patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.analyzer_agent import AnalyzerAgent
from agents.risk_agent import RiskAgent


class TestScoringRegression(unittest.TestCase):
    @patch("agents.analyzer_agent.call_llm", return_value="")
    def test_analysis_confidence_not_constant_for_different_inputs(self, _: object) -> None:
        agent = AnalyzerAgent()

        low_signal = agent.analyze(
            text="Weekly security newsletter with minor platform updates.",
            transparency_note="test",
        )
        high_signal = agent.analyze(
            text=(
                "Ransomware campaign used CVE-2026-12345 exploit and lateral movement "
                "for data exfiltration against AcmeCorp."
            ),
            transparency_note="test",
        )

        self.assertNotEqual(low_signal["confidence_score"], high_signal["confidence_score"])
        self.assertNotEqual(low_signal["threat_type"], high_signal["threat_type"])
        self.assertGreater(high_signal["confidence_score"], low_signal["confidence_score"])

    @patch("agents.analyzer_agent.call_llm", return_value="")
    def test_risk_confidence_not_pinned_at_054(self, _: object) -> None:
        analyzer = AnalyzerAgent()
        risk = RiskAgent()

        a = analyzer.analyze(
            text="Routine maintenance bulletin for internal systems.",
            transparency_note="test",
        )
        b = analyzer.analyze(
            text=(
                "APT intrusion with command and control infrastructure, CVE-2026-98765, "
                "credential dumping and data exfiltration observed."
            ),
            transparency_note="test",
        )

        r1 = risk.assess(a)
        r2 = risk.assess(b)

        self.assertNotEqual(r1["confidence_score"], 0.54)
        self.assertNotEqual(r2["confidence_score"], 0.54)
        self.assertNotEqual(r1["confidence_score"], r2["confidence_score"])
        self.assertGreater(r2["confidence_score"], r1["confidence_score"])


if __name__ == "__main__":
    unittest.main()
