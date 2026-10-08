# CLAUDE.md

Claude Code reads this file automatically at the start of every session.
The two lines below pull in the project memory and the standing instructions.

@MEMORY.md
@SKILLS.md

## Start of every session
1. Read MEMORY.md (what has happened, what is pending) and SKILLS.md (how to work).
2. Run `git fetch` and check the open PRs, so memory matches reality.
3. Tell the user in 2-3 simple lines where things stand and what the next pending task is.
4. Continue with the pending tasks unless the user asks for something else.

## End of every session (or after any big step)
Update MEMORY.md: status, decisions, pending tasks, and one line in the session log. Commit it with the work.
