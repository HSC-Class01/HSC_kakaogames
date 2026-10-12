from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parent

def test_config():
    cfg = json.loads((ROOT / "settings.json").read_text(encoding="utf-8"))
    assert cfg["corp_code"] == "00126380"
    assert cfg["start_year"] == 2010
    assert cfg["fs_div"] in {"CFS", "OFS"}

def test_workflow_yaml():
    workflow = ROOT / ".github" / "workflows" / "monthly_update.yml"
    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "jobs" in data
    assert "update-and-deploy" in data["jobs"]
    assert data["jobs"]["update-and-deploy"]["steps"]

def test_dashboard_has_data_loader():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "data/financials.csv" in html
    assert "data/ratios.csv" in html
