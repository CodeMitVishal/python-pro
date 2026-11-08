# Git & team workflow (asked in almost every interview)

Day one at any job: clone, branch, commit, open a pull request, get a review, merge. Here's the workflow and the questions about it.

[← Interview prep](README.md)

---

## The everyday flow

```bash
git switch main && git pull                 # start from the latest main
git switch -c feat/order-export             # one branch per task
# ... edit, test ...
git add -p                                  # stage hunk by hunk, review your own diff
git commit -m "Add CSV export for orders"
git push -u origin feat/order-export        # then open a Pull Request
```

While the PR is open, keep your branch up to date:

```bash
git fetch origin
git rebase origin/main                      # replay your commits on top of the new main
git push --force-with-lease                 # safe force push of YOUR branch only
```

## Good pull requests

- **Small**: one topic, ideally under about 400 lines of diff.
- A **clear title and description**: what, why, how you tested it, screenshots for UI changes.
- **Green CI**: lint, types and tests pass before you ask for a review.
- Respond to every review comment; resolve the conversation when it's done.

---

## Interview questions

### 1. `git merge` vs `git rebase`?

**Say:** **Merge** joins two histories with a merge commit. It keeps the true history and is safe on shared branches. **Rebase** replays your commits on top of another branch, giving a linear history. Use it on **your own** feature branch before merging. Never rebase commits that other people have already pulled.

### 2. How do you resolve a merge conflict?

**Say:** Run `git status` to see the conflicted files, open each one, and choose or combine the changes between the `<<<<<<<` and `>>>>>>>` markers. Run the tests, `git add` the files, then `git rebase --continue` (or commit the merge). Talk to the other author if the intent is unclear.

### 3. `git reset` vs `git revert`?

**Say:** `revert` creates a **new** commit that undoes an old one, so it's safe on shared branches. `reset` moves the branch pointer back and rewrites history: `--soft` keeps the changes staged, `--hard` throws them away. Only reset local, unpushed work.

### 4. What is `git stash`?

**Say:** It temporarily shelves uncommitted changes (`git stash`, then later `git stash pop`), so you can switch branches for an urgent fix.

### 5. What branching strategy have you used?

**Say:** **Trunk-based / GitHub flow**: short-lived feature branches from `main`, PRs with review and CI, merge often, and deploy from `main`. Release branches or tags are used for versioned releases. Long-lived branches cause painful merges.

### 6. How do you find which commit introduced a bug?

**Say:** `git bisect`. Mark a good and a bad commit, and Git binary-searches the history while you test each step (or automate it with `git bisect run pytest ...`). `git log -p` and `git blame` help too.

### 7. What makes a good commit message?

**Say:** A short imperative summary ("Add CSV export for orders"), and optionally a body explaining **why**. One logical change per commit.

### 8. What should never be committed?

**Say:** Secrets (`.env`, keys), virtual environments, `__pycache__`, build output and large data files. Use `.gitignore`. If a secret leaks, **rotate it**: deleting the commit isn't enough.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
