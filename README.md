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

### In-depth usage guide

#### 1. Quick-start for a **new** repo (template method)
1. On GitHub click **Use this template** → select `Agent-starter-kit`.
2. Name your new repository and create it.
3. Go to **Settings → Secrets → Actions**.
   • Add `MEM0_API_KEY` (required)  
   • Add any other API keys (e.g. OPENAI)
4. Open a GitHub Issue → within ~60 seconds Planner comments and the agent loop begins.

#### 2. Add to an **existing** repo
```bash
# inside the repo root
cp -R path/to/Agent-starter-kit/.github .
cp -R path/to/Agent-starter-kit/agent_configs .
cp -R path/to/Agent-starter-kit/scripts .
mkdir -p context && echo "<!-- bootstrap -->" > context/latest.md

git add .github agent_configs scripts context
git commit -m "Enable multi-agent scaffold"
git push
```
Then add `MEM0_API_KEY` secret as above.

#### 3. Daily interaction model
| Human action            | Bot reaction                                      |
| ----------------------- | -------------------------------------------------- |
| Create/clarify Issue    | Planner decomposes into tasks                      |
| —                       | Prioritizer labels bottlenecks                     |
| —                       | Coder-α/β/γ pick tasks, create branches & code     |
| Review PR comment       | Coders amend until tests pass                      |
| Merge PR                | Merge-bot deletes branch & frees up coders         |
| Push / merge            | repo→markdown snapshot, memories sent to Mem0      |

#### 4. What you’ll see
1. **GitHub Issues:** Planner comments with check-box tasks assigned to Coders.  
2. **Branches/PRs:** feature branches named `feat/ISSUE-ID-…` appear automatically.  
3. **Actions:** `repo-to-markdown` workflow runs on every push.  
4. **Mem0 Dashboard:** new memories tagged with repo/branch metadata.

#### 5. Troubleshooting
• No Action runs → `.github/workflows` missing or Actions disabled.  
• 400 errors from Mem0 → payload too large; safe to ignore.  
• Planner silent → orchestrator not watching `main` or missing API key.  
• Need more compute → scale out by copying `coder_template.json` to `coder_delta.json` and editing the name.

#### 6. Glossary
*Planner* – reads Issues and breaks them into tasks.  
*Prioritizer* – surfaces the highest-impact task.  
*Coder* – writes code for one task at a time.  
*Tester* – runs unit tests / lint in CI.  
*Merge-bot* – merges green PRs.  
*Mem0* – long-term memory store used by all agents.
