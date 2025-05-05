<!---- AUTO-GENERATED: do not edit by hand -->

## .windsurf.json  \[ae85dd3c]
```json
{
  "mcp_servers": [
    { "name": "GitHub", "url": "https://api.github.com" },
    { "name": "LocalFS", "path": "./context" }
  ],
  "default_planner": "Planner",
  "branching_strategy": "ticket"
}

```

## requirements.txt  \[c0cc6b88]
```txt
mem0ai>=0.1.0

```

## README.md  \[133172f7]
```md
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

```

## agent_configs/coder_alpha.json  \[477e963e]
```json
{
  "name": "Coder-Alpha",
  "branch_prefix": "feat/${ISSUE_ID}",
  "llm": "o3",
  "role": "Implement one task at a time.  Steps: git_pull → edit ≤3 files → unit tests → git_add_commit → git_push",
  "post_push_hook": "open_pull_request"
}

```

## agent_configs/coder_beta.json  \[bf9f0799]
```json
{
  "name": "Coder-Beta",
  "branch_prefix": "feat/${ISSUE_ID}",
  "llm": "o3",
  "role": "Implement one task at a time.  Steps: git_pull → edit ≤3 files → unit tests → git_add_commit → git_push",
  "post_push_hook": "open_pull_request"
}

```

## agent_configs/coder_gamma.json  \[c730b189]
```json
{
  "name": "Coder-Gamma",
  "branch_prefix": "feat/${ISSUE_ID}",
  "llm": "o3",
  "role": "Implement one task at a time.  Steps: git_pull → edit ≤3 files → unit tests → git_add_commit → git_push",
  "post_push_hook": "open_pull_request"
}

```

## agent_configs/coder_template.json  \[28eb0c38]
```json
{
  "name": "${CODER_NAME}",
  "branch_prefix": "feat/${ISSUE_ID}",
  "llm": "o3",
  "role": "Implement one task at a time.  Steps: git_pull → edit ≤3 files → unit tests → git_add_commit → git_push",
  "post_push_hook": "open_pull_request"
}

```

## agent_configs/tester.json  \[60b0bf38]
```json
{
  "name": "Tester",
  "branch": "*",  
  "llm": "o3",
  "role": "On every pull-request run pytest and eslint.  If failures, comment with traceback; else approve.",
  "tools": ["bash", "pytest", "eslint"]
}

```

## agent_configs/planner.json  \[5ad33166]
```json
{
  "name": "Planner",
  "branch": "main",
  "llm": "o3",
  "role": "Break GitHub issues into atomic tasks, label them, and assign to free Coder agents.  Never write code.",
  "max_tokens": 12000
}

```

## agent_configs/merge_bot.json  \[883d66e7]
```json
{
  "name": "Merge-bot",
  "branch": "main",
  "llm": "o3",
  "role": "Merge any PR with ‘✔ tests passed’ label.  Delete branch post-merge.",
  "tools": ["git"]
}

```

## scripts/fswatch_snapshot.sh  \[11ad5178]
```sh
#!/usr/bin/env bash
# Live snapshot every time a file changes (macOS/Linux).
repo_root="$(git rev-parse --show-toplevel)"
fswatch -o "$repo_root" | while read; do
  python "$repo_root/scripts/repo2md.py" > "$repo_root/context/latest.md"
  git add context/latest.md
  git commit -m "auto snapshot (fswatch)" --no-verify || true
  git push || true
done

```

## scripts/repo2md.py  \[93ee45fa]
```py
#!/usr/bin/env python3
"""Walk the repo and emit a single markdown file showing changed source only."""
import pathlib, sys, hashlib, os
root = pathlib.Path(__file__).resolve().parents[1]
EXCLUDE = {".git", "context", ".github"}

# Initialize Mem0 memory layer if available
MEMORY = None
if os.getenv("MEM0_API_KEY"):
    try:
        from mem0 import MemoryClient
        # MemoryClient reads MEM0_API_KEY from env; optional namespace through set_default_metadata
        MEMORY = MemoryClient()
    except ImportError:
        MEMORY = None

print("<!---- AUTO-GENERATED: do not edit by hand -->")
for path in root.rglob("*.*"):
    if any(part in EXCLUDE for part in path.parts):
        continue
    if path.stat().st_size > 50_000:  # skip binaries & huge assets
        continue
    rel = path.relative_to(root)
    code = path.read_text(errors="ignore")
    sha  = hashlib.sha1(code.encode()).hexdigest()[:8]
    # Push to Mem0 if configured
    if MEMORY:
        try:
            # Store code with basic path/sha context if supported
            MEMORY.add(code, metadata={"path": str(rel), "sha": sha})
        except TypeError:
            # Fallback to add(content) if metadata param unsupported
            try:
                MEMORY.add(code)
            except Exception:
                pass
        except Exception:
            pass
    print(f"\n## {rel}  \[{sha}]\n```{rel.suffix.lstrip('.')}\n{code}\n```")

```
