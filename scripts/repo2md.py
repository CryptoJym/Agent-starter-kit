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
