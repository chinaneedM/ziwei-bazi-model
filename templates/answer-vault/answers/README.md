# Answer object layout

Store one immutable JSON object per authorized run under `answers/<group-or-case>/<run_id>.json`. The workflow accepts only paths beneath `answers/` and rejects traversal. Never commit tokens, prediction worktrees, source ZIPs, example RARs, or SHADOW_REBUILD material here.
