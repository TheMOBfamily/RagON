Read and execute the EXACT next pending task from `{INIT_FILE_PATH}`.

**CRITICAL**: After completing task, you MUST follow ftask/13-task-lifecycle-mark-done.md:
1. Fill Execution Log (timestamps, actions)
2. Update YAML status → completed
3. RENAME: XX-task.md → done-XX-task.md
4. Git commit
5. Update init-autoclaude.json

Execute ONE task at a time. DO NOT proceed until all 5 completion steps done!

If all tasks completed → doublecheck using mindset `.fong/instructions/mindsets/mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md`.
