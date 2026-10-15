"""Kiểm cấu trúc, link, nguồn, nội dung model và output notebook sau chuyển thư mục.

Chạy từ Nile_Sale: python -X utf8 scripts/validate_project_structure.py
Không chạy pipeline, không ghi dữ liệu hoặc model.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapped(name):
    name = name.replace("\\", "/")
    if name in {".agent-work/PLAN.md", ".agent-work/PLAN.v0.2.approved.md"}:
        return name.replace(".agent-work/", "Plan/", 1)
    name = name.replace(".agent-work/", "Log/", 1).replace("powerbi/", "pbi/", 1)
    if name.startswith("Log/structure_") or name in {"Log/input_inventory.json", "Log/SKILL_APPLICATION_REVIEW.md"}:
        name = name.replace("Log/", "Log/evidence/setup/", 1)
    return name


def main():
    for name in ("data", "docs", "Log", "notebooks", "pbi", "Plan", "reports", "scripts"):
        assert (ROOT / name).is_dir(), name
    for name in ("AGENTS.md", "CLAUDE.md", "README.md", ".gitignore", "Plan/PLAN.md", "Log/RESULT.md", "Log/session.json"):
        assert (ROOT / name).is_file() and (ROOT / name).stat().st_size > 0, name
    assert not (ROOT / ".agent-work").exists()
    assert not (ROOT / "powerbi").exists()
    state = json.loads((ROOT / "Log/session.json").read_text(encoding="utf-8-sig"))
    assert state["skillVersion"] in {"1.1", "1.2"} and isinstance(state["gate4Approved"], bool)
    if state.get("phase4bDispatched"):
        assert state["gate4Approved"] is True, "4B dispatched before Gate 4 approval"
    for move in state.get("logOrganization", {}).get("moves", []):
        target = ROOT / mapped(move["oldPath"])
        assert mapped(move["oldPath"]) == move["newPath"], move["oldPath"]
        assert target.is_file() and digest(target) == move["sha256"], move["newPath"]
    migration = json.loads((ROOT / "Log/evidence/setup/structure_migration.json").read_text(encoding="utf-8-sig"))
    for name, expected in migration["beforeHashes"].items():
        target = ROOT / mapped(name)
        if name == ".agent-work/PLAN.md":
            target = ROOT / "Plan/PLAN.v0.6.before-format.md"
        assert target.is_file(), f"Lost file: {name}"
        if name.startswith(("data/", "powerbi/")) or name.endswith("_evidence.json"):
            if "/.pbi/" not in name.replace("\\", "/"):
                assert digest(target) == expected, f"Protected bytes changed: {name}"
    for name, expected in migration["notebookOutputHashes"].items():
        nb = json.loads((ROOT / name).read_text(encoding="utf-8"))
        outputs = json.dumps([c.get("outputs", []) for c in nb["cells"]], sort_keys=True, ensure_ascii=False).encode()
        assert hashlib.sha256(outputs).hexdigest() == expected, name
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                assert ".agent-work" not in source, name
                compile(source, name, "exec")
    docs = [ROOT / name for name in ("README.md", "CLAUDE.md", "Plan/PLAN.md", "Log/RESULT.md")]
    docs += list((ROOT / "docs").glob("*.md"))
    for doc in docs:
        for raw in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8-sig")):
            link = raw.strip("<>").split("#", 1)[0]
            if link and not re.match(r"^[a-zA-Z][\w+.-]*:", link):
                assert (doc.parent / unquote(link)).exists(), f"Broken link: {doc}: {link}"
    pbip = json.loads((ROOT / "pbi/NileSales.pbip").read_text(encoding="utf-8-sig"))
    report = ROOT / "pbi" / pbip["artifacts"][0]["report"]["path"]
    definition = json.loads((report / "definition.pbir").read_text(encoding="utf-8-sig"))
    assert (report / definition["datasetReference"]["byPath"]["path"]).is_dir()
    print("ĐẠT: cấu trúc/link/nguồn/model/output notebook; quyền phase theo Log/session.json.")


if __name__ == "__main__":
    main()
