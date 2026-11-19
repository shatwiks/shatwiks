# Change Report (`CHANGEREPORT.md`)

## 2026-11-20 02:06 IST — Refresh Top Skills & Featured Projects (`github-profile-update`)

### Objective
Execute the full `github-profile-update` workflow for `shatwiks/shatwiks`: scan all 11 public repositories under `shatwiks`, sync all 10 non-empty project repositories into the conversation scratch directory, measure real language and manifest usage, read project Markdown documentation and verification reports, and update only `## 📊 Top Skills` and `## 🚀 Featured Projects` in `README.md` while keeping the rest of `README.md` unchanged.

### Files Created / Modified
- **[README.md](README.md)** *(modified)* — Updated only `## 📊 Top Skills (measured from my repos)` (recalculated across all 10 project repositories totaling 161,004 non-blank project lines excluding vendored `.github/skills/` and `frontend/public/assets/` runtime kits) and `## 🚀 Featured Projects` (ranked all 10 built projects by engineering depth and recruiter impact with verified benchmarks, test counts, live demo/API links, and concise 2–3 line summaries). All other sections (`About Me`, `Tech Stack`, `Hackathons & Achievements`, `GitHub Stats`, `3D Contribution Graph`, `Contribution Snake`, `Engineering Principles`, `Currently Focused On`, footer) were left untouched.
- **[CHANGEREPORT.md](CHANGEREPORT.md)** *(created)* — Recorded this change summary in accordance with the standing change-report workflow.

### Verification Commands & Results
- **Repository Discovery & Sync:** Fetched `https://api.github.com/users/shatwiks/repos?per_page=100&sort=pushed` (11 public repos returned; `gh` CLI not installed) and cloned all 11 repos cleanly with `git -c core.longpaths=true`.
- **Top Skills Measurement:** Measured 161,004 non-blank project code lines across the 10 project repos (`Python` 79,227 / 49.2%, `TypeScript` 68,298 / 42.4%, `JavaScript` 6,365 / 4.0%, `CSS` 4,529 / 2.8%, `C++20` 1,322 / 0.8%, `SQL` 1,187 / 0.7%) and verified framework/infrastructure counts from manifests and CI/IaC files.
- **Git Diff & Push Verification:** Verified `git diff` touches only `Top Skills` and `Featured Projects` in `README.md`, then executed `git pull --rebase origin main` and `git push origin main` with `GIT_TERMINAL_PROMPT=0` and `GCM_INTERACTIVE=never`.
