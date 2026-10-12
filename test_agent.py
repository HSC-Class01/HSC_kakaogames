"""Lightweight repository smoke tests; uses only the Python standard library."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class AgentSmokeTests(unittest.TestCase):
    def test_collector_and_dashboard_exist(self):
        self.assertTrue((ROOT / "scripts" / "update.py").is_file())
        self.assertTrue((ROOT / "docs" / "index.html").is_file())
        self.assertTrue((ROOT / "requirements.txt").is_file())

    def test_collector_targets_kakao_games(self):
        source = (ROOT / "scripts" / "update.py").read_text(encoding="utf-8")
        self.assertIn("'293490'", source)
        self.assertIn("data/processed", source)
        self.assertIn("financials.json", source)

    def test_dashboard_uses_processed_json(self):
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("./data/processed/financials.json", html)
        self.assertIn("Annual", html)
        self.assertIn("Half-year", html)
        self.assertIn("Quarterly", html)
        self.assertIn("국내 Peer Firms", html)

    def test_monthly_workflow_has_schedule_and_pages_deploy(self):
        workflow = (ROOT / ".github" / "workflows" / "monthly_update.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "15 0 1 * *"', workflow)
        self.assertIn("python scripts/update.py", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("secrets.DART_API_KEY", workflow)


if __name__ == "__main__":
    unittest.main()
