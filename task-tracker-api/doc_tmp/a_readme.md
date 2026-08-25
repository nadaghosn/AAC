# README.md — Coverage Check

Checked the current `README.md` for: branch name, local run command, Docker run command, test command, evidence files, and a short AI assistance summary.

| Item | Present? | Evidence |
|---|---|---|
| **Branch name** | ❌ No | No mention of `final-project` (or any branch) anywhere in the file |
| **Local run command** | ✅ Yes | Line 36: `uvicorn app.main:app --reload --port 8000` (under "Run the app locally") |
| **Docker run command** | ✅ Yes | Lines 96-97: `docker build -t task-tracker:dev .` / `docker run -d --name task-tracker-dev -p 8000:8000 task-tracker:dev` (under "Run with Docker") |
| **Test command** | ✅ Yes | Line 82: `pytest -v` (under "Run tests") |
| **Evidence files** | ❌ No | No reference anywhere to the `d1*.md`/`d2*.md`/`doc2*.md`/`doc3*.md`/`c3_green_red.md`/`b1_dangerous.md` verification/evidence docs sitting at the module root |
| **Short AI assistance summary** | ❌ No | No section or line disclosing AI assistance/authorship anywhere in the file |

## Summary

3 of 6 items covered. Branch name, evidence files, and an AI assistance summary are missing.
