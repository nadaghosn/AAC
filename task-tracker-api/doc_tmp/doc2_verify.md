# README.md — Items Needing Verification

Flagged while drafting the Module 4 `README.md` rewrite. None of these are guesses about behavior — each was checked directly against the repo — but each represents a fact, naming choice, or repo-layout assumption the README author (you) should confirm.

## 1. Repo root vs. module root

`git rev-parse --show-toplevel` from `task-tracker-api/` resolves to `/home/esu-linux/AAC` — the actual git repository root is one level up; `task-tracker-api/` is a subdirectory of a larger repo. The README's "Local setup" section assumes `task-tracker-api/` is the effective project root (consistent with how CLAUDE.md already frames things). **Confirm this is the intended framing** before treating the README's commands as runnable from the outer repo root.

## 2. CI workflow file location

`.github/workflows/ci.yml` lives outside `task-tracker-api/`, at the outer repository's root (`../.github/workflows/ci.yml` relative to this module). It sets `working-directory: task-tracker-api` for its steps. This was confirmed by reading the actual file — several commit messages mention "CI workflow" but only touch unrelated `.md` files (`c2.md`, `c3*.md`, `s2*.md`, `s3*.md`), which was initially misleading.

## 3. `pydantic-settings` unused dependency

`pydantic-settings==2.9.1` is pinned in `requirements.txt`, but a search for `BaseSettings`/`pydantic_settings` across `app/` and `tests/` found zero references. **Confirm whether this is a leftover from an earlier iteration or intended for near-term use.**

## 4. `.env.example` variables are inert

`PORT` is never read anywhere in `app/`. `APP_ENV` is assigned once (`app/main.py:30`, `os.getenv("APP_ENV", "development")`) but never referenced again in the file. `load_dotenv()` runs at startup, but neither variable currently changes runtime behavior. **Confirm whether these are scaffolding for future use or should be removed.**

## 5. `data/tasks.json`

This file exists in the repo (git-tracked, contents `[]`) but nothing in `app/` reads or writes it — `app/storage.py` confirms storage is in-memory only. **Confirm the purpose of this file** (leftover from an earlier persistence approach, per `docs/midcourse/mini-adr.md`'s mention of a JSON-file storage option that was ultimately not the final implementation?).

## 6. No `docs/decisions/` directory

The task asked the README to link to `docs/decisions` if a technical note exists. No such directory exists. The closest match is `docs/midcourse/mini-adr.md`, an ADR-style write-up of the storage/tags decision — but it lives under `docs/midcourse/`, not `docs/decisions/`, and isn't named or structured as a formal ADR file. **Confirm whether this is an acceptable substitute, or whether a `docs/decisions/` note should be created.**

## 7. PATCH vs. PUT on task comments

`patch_comment` (PATCH) and `put_comment` (PUT) on `/tasks/{task_id}/comments` currently behave identically — both call storage functions (`update_comment` / `replace_comment`) with the same body: fully overwrite `text`, preserve the original `created_at`. Already flagged during the docstring pass (`app/main.py`, `app/storage.py`) with `[VERIFY]` comments. **Confirm whether distinct partial-vs-full-replace semantics were intended**, since `CommentUpdate` only has one field (`text`), so there may be no meaningful distinction to implement.
