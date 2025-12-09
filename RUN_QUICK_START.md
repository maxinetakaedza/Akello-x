# Quick Start — 1-day prototype runbook

Goal: Run the rule-based decision prototype locally and exercise the main rules with a few test attempts.

Prerequisites
- Python 3.9+ (Mac / Linux / WSL / Windows)
- git (optional if using the GitHub web UI)
- curl (optional; a test script is provided)

If you haven't already, add the prototype files into your repo or download this folder.

## 1) Create a virtual environment and install dependencies
Open a terminal in the project root and run:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## 2) Run the API server
Start the FastAPI app with Uvicorn:

```bash
uvicorn app:app --reload
```

By default it will start at:
http://127.0.0.1:8000

## 3) Run the test script (in a new terminal)
With the virtualenv activated, make the script executable (macOS/Linux) and run it:

```bash
chmod +x test_attempts.sh
bash test_attempts.sh
```

The script sends a few sequences of attempts (wrong streak -> decrease difficulty, correct streak -> increase difficulty, repeated fails -> micro-lesson) and prints server responses.

## 4) Inspect responses
Each `/attempt` response contains a `next_action` object describing what the rule engine decided. Useful fields:

- `next_action.action` — e.g. `"increase_difficulty"`, `"decrease_difficulty"`, `"show_micro_lesson"`, `"next_questions"`
- `xp_gained`
- `level_up`
- `weekly_mission`

## Quick manual test (curl)
If you prefer to POST a single attempt manually:

```bash
curl -sS -X POST "http://127.0.0.1:8000/attempt" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id":"student1",
    "question_id":"q1",
    "topic":"algebra/linear-equations",
    "difficulty":"easy",
    "correct":false,
    "time_spent_seconds":45
  }'
```

## Troubleshooting
- ModuleNotFoundError: ensure virtualenv is activated and `pip install -r requirements.txt` succeeded.
- Address already in use: change the port or stop other `uvicorn` processes.
- If the test script fails, run the curl command above and paste the server error here — I’ll help debug.

## What to look for in responses (expected rule triggers)
- After two wrong attempts on the same topic: `next_action.action == "decrease_difficulty"`
- After three correct attempts on the same topic: `next_action.action == "increase_difficulty"`
- After multiple recent failures (>=60% fail rate, >=3 attempts) on a topic and `difficulty == "easy"`: `next_action.action == "show_micro_lesson"`

## If you want help updating this file on GitHub
1. Open the repo page in your browser: `https://github.com/maxinetakaedza/Akello-x`
2. Switch to the branch you want to edit (use the branch dropdown; create `prototype/rule-engine` if you don't have one).
3. Open `RUN_QUICK_START.md` in the file list.
4. Click the pencil icon (Edit this file).
5. Replace the contents with this corrected content, scroll down, add a commit message like "Fix README / quick start formatting", and click "Commit changes" (commit to your branch).
6. Open a Pull Request if you want to merge to `main`.

If you'd like, I can paste this into the GitHub web editor for you (prepare a PR) — tell me the branch name you want to use (default: `prototype/rule-engine`) and I'll create the PR content for you.
