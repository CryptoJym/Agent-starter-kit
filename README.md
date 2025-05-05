# 🚀 Project Bootstrap for Multi-Agent Development

Welcome!  This repo is wired for:
1. **Branch-per-ticket** workflow (Planner ⇒ Coder branches ⇒ Merge-bot).
2. Automatic "repo → markdown context" snapshots for AI agents.
3. Local or cloud CI with identical steps.

### One-time setup
```bash
brew install fswatch act            # <-- optional speed boosters
pip install -r requirements.txt     # only if you add deps later
```

### Daily flow

| Step             | Human                                | Agent                            |
| ---------------- | ------------------------------------ | -------------------------------- |
| Pull latest main | `git pull`                           | –                                |
| New work item    | create GitHub Issue                  | Planner writes description       |
| Create branch    | click **Branches → New** in Windsurf | `git checkout -b feat/ISSUE-123` |
| Code & commit    | –                                    | Coder agent                      |
| Push branch      | click Push                           | same                             |
| PR + tests       | –                                    | Tester & Merge-bot               |

Need help?  Ping ChatGPT with the file path and line number.
