#!/usr/bin/env python3
"""Nightly GitHub profile updater for shatwiks/shatwiks.

Scans all non-empty public repositories under GITHUB_OWNER, detects newly added
or updated repos, reads their Markdown docs, recalculates Top Skills from real
code/manifests, and uses Gemini (with automatic GitHub Models fallback) to
produce concise 2-3 line recruiter-focused descriptions ranked by recruiter
impact. Updates ONLY the Top Skills and Featured Projects sections of README.md.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import requests

OWNER = os.environ.get("GITHUB_OWNER", "shatwiks").strip() or "shatwiks"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
FORCE_REFRESH = os.environ.get("FORCE_REFRESH", "false").strip().lower() == "true"

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
STATE_PATH = REPO_ROOT / "profile" / "projects-state.json"

EXCLUDE_PREFIXES = (
    ".agents/",
    ".codex/",
    ".impeccable/",
    ".taste-skill/",
    "graphify-out/",
    ".planning/",
    "node_modules/",
)
EXCLUDE_SUBSTRINGS = (
    "/node_modules/",
    "package-lock.json",
    "/dist/",
    "/build/",
    ".min.",
)

LANG_MAP = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".cpp": "C++20",
    ".hpp": "C++20",
    ".h": "C++20",
    ".sql": "SQL",
    ".css": "CSS",
    ".html": "HTML",
    ".lua": "Lua",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
}

BOT_COMMIT_RE = re.compile(
    r"(\[skip ci\]|update readme cards|update 3d contribution graph|refresh project metrics|auto-update profile)",
    re.IGNORECASE,
)

URL_RE = re.compile(r"https?://[^\s\)\"'>]+")


def gh_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{OWNER}-profile-updater",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def list_project_repos() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{OWNER}/repos"
            f"?per_page=100&type=owner&sort=pushed&page={page}"
        )
        resp = requests.get(url, headers=gh_headers(), timeout=30)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for r in batch:
            name = r["name"]
            if name.lower() == OWNER.lower():
                continue
            if r.get("fork") or r.get("archived"):
                continue
            repos.append(r)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_latest_human_commit_sha(repo_name: str, default_branch: str) -> str | None:
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/commits"
    resp = requests.get(
        url,
        headers=gh_headers(),
        params={"sha": default_branch, "per_page": 15},
        timeout=30,
    )
    if resp.status_code in (404, 409):  # 409 = empty repo
        return None
    resp.raise_for_status()
    commits = resp.json()
    if not commits:
        return None
    for c in commits:
        msg = (c.get("commit", {}).get("message") or "").splitlines()[0]
        author_login = ((c.get("author") or {}).get("login") or "").lower()
        if author_login.endswith("[bot]") or BOT_COMMIT_RE.search(msg):
            continue
        return c["sha"]
    return commits[0]["sha"]


def is_excluded(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/")
    if any(norm.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    if any(s in f"/{norm}" for s in EXCLUDE_SUBSTRINGS):
        return True
    return False


def shallow_clone(clone_url: str, dest: Path) -> bool:
    cmd = ["git", "clone", "--depth=1", "--quiet", clone_url, str(dest)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0


def git_tracked_files(repo_dir: Path) -> list[str]:
    res = subprocess.run(
        ["git", "-C", str(repo_dir), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in res.stdout.splitlines() if line.strip()]


def collect_markdown_context(repo_dir: Path, tracked: list[str]) -> tuple[str, list[str]]:
    """Collect highest-signal Markdown docs and verified external URLs."""
    md_files: list[str] = []
    for rel in tracked:
        norm = rel.replace("\\", "/")
        if not norm.lower().endswith(".md"):
            continue
        if any(
            norm.startswith(p)
            for p in (".agents/", ".codex/", ".impeccable/", ".taste-skill/", "graphify-out/", "node_modules/")
        ):
            continue
        md_files.append(norm)

    def priority(path: str) -> tuple[int, int, str]:
        lower = path.lower()
        if lower == "readme.md":
            return (0, len(path), path)
        if any(k in lower for k in ("benchmark", "verification", "full_report", "results", "state.md", "project.md")):
            return (1, len(path), path)
        if any(k in lower for k in ("deployment", "roadmap", "changelog", "prd", "arch")):
            return (2, len(path), path)
        return (3, len(path), path)

    md_files.sort(key=priority)

    chunks: list[str] = []
    urls: list[str] = []
    budget = 2400
    used = 0
    for rel in md_files[:6]:
        fp = repo_dir / rel
        if not fp.is_file():
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in URL_RE.findall(text):
            cleaned = match.rstrip(".,;:")
            if cleaned not in urls:
                urls.append(cleaned)
        if used >= budget:
            continue
        # Strip HTML/SVG noise and collapse blank lines for compact LLM context
        compact = re.sub(r"<[^>]+>", " ", text)
        compact = re.sub(r"\n{3,}", "\n\n", compact).strip()
        snippet = compact[: min(1400, budget - used)].strip()
        if snippet:
            chunks.append(f"### {rel}\n{snippet}")
            used += len(snippet)

    return "\n\n".join(chunks), urls


def measure_top_skills(repo_dirs: dict[str, Path]) -> dict[str, Any]:
    lang_lines: dict[str, int] = {}
    lang_repos: dict[str, int] = {}

    tool_patterns = {
        "React": r'"react"',
        "Next.js": r'"next"',
        "Vite": r'"vite"',
        "Tailwind CSS": r'"tailwindcss"',
        "Three.js": r'"three"',
        "Zustand": r'"zustand"',
        "FastAPI": r"fastapi",
        "SQLAlchemy": r"sqlalchemy",
        "Pydantic": r"pydantic",
        "Express": r'"express"',
        "Alembic": r"alembic",
        "Prisma": r'"prisma"|"@prisma/client"',
        "Zod": r'"zod"',
        "pytest": r"pytest",
        "Vitest": r'"vitest"',
        "Playwright": r"playwright",
        "pgvector": r"pgvector",
        "DuckDB": r"duckdb",
    }
    tool_counts: dict[str, int] = {k: 0 for k in tool_patterns}
    infra_counts: dict[str, int] = {
        "Docker": 0,
        "PostgreSQL": 0,
        "GitHub Actions CI": 0,
        "Redis": 0,
        "SQLite": 0,
        "Terraform": 0,
        "Kubernetes": 0,
    }

    for _, rdir in repo_dirs.items():
        tracked = [f for f in git_tracked_files(rdir) if not is_excluded(f)]
        seen_langs: set[str] = set()

        for rel in tracked:
            ext = Path(rel).suffix.lower()
            if ext in LANG_MAP:
                fp = rdir / rel
                if fp.is_file():
                    try:
                        with fp.open("r", encoding="utf-8", errors="ignore") as fh:
                            cnt = sum(1 for line in fh if line.strip())
                    except OSError:
                        cnt = 0
                    lang = LANG_MAP[ext]
                    lang_lines[lang] = lang_lines.get(lang, 0) + cnt
                    seen_langs.add(lang)

        for lang in seen_langs:
            lang_repos[lang] = lang_repos.get(lang, 0) + 1

        manifests = [
            rdir / f
            for f in tracked
            if re.search(r"(^|/)(package\.json|requirements[^/]*\.txt|pyproject\.toml)$", f)
        ]
        manifest_text = "\n".join(
            m.read_text(encoding="utf-8", errors="ignore") for m in manifests if m.is_file()
        )
        for tool, pat in tool_patterns.items():
            if re.search(pat, manifest_text, re.IGNORECASE):
                tool_counts[tool] += 1

        if any(re.search(r"Dockerfile|docker-compose", f) for f in tracked):
            infra_counts["Docker"] += 1
        if any(f.startswith(".github/workflows/") for f in tracked):
            infra_counts["GitHub Actions CI"] += 1
        if any(f.endswith(".tf") for f in tracked):
            infra_counts["Terraform"] += 1
        if any(re.search(r"(^|/)k8s/|kind|kubernetes", f, re.IGNORECASE) for f in tracked):
            infra_counts["Kubernetes"] += 1

        cfg_files = [
            rdir / f
            for f in tracked
            if re.search(
                r"(docker-compose[^/]*\.ya?ml|package\.json|requirements[^/]*\.txt|pyproject\.toml|\.env\.example|schema\.prisma)$",
                f,
            )
        ]
        cfg_text = "\n".join(
            c.read_text(encoding="utf-8", errors="ignore") for c in cfg_files if c.is_file()
        )
        if re.search(r"postgres", cfg_text, re.IGNORECASE):
            infra_counts["PostgreSQL"] += 1
        if re.search(r"redis", cfg_text, re.IGNORECASE):
            infra_counts["Redis"] += 1
        if re.search(r"sqlite", cfg_text, re.IGNORECASE):
            infra_counts["SQLite"] += 1

    return {
        "repo_count": len(repo_dirs),
        "lang_lines": lang_lines,
        "lang_repos": lang_repos,
        "tool_counts": tool_counts,
        "infra_counts": infra_counts,
    }


def render_top_skills(metrics: dict[str, Any]) -> str:
    lang_lines: dict[str, int] = metrics["lang_lines"]
    lang_repos: dict[str, int] = metrics["lang_repos"]
    total_lines = sum(lang_lines.values()) or 1
    top_langs = sorted(lang_lines.items(), key=lambda kv: kv[1], reverse=True)[:6]

    bars: list[str] = []
    for lang, lines in top_langs:
        pct = (lines / total_lines) * 100.0
        filled = max(1, round((pct / 100.0) * 40)) if lines > 0 else 0
        bar = "█" * filled + "░" * (40 - filled)
        k_val = f"{lines / 1000:.1f}k" if lines >= 1000 else f"{lines}"
        repo_n = lang_repos.get(lang, 1)
        repo_label = "1 repo" if repo_n == 1 else f"{repo_n} repos"
        bars.append(f"{lang:<11} {bar}  {pct:4.1f}%  · {k_val:>5} lines · {repo_label}")

    tc = metrics["tool_counts"]
    ic = metrics["infra_counts"]

    fe = [
        f"⚛️ React · **{tc['React']}**",
        f"🎨 Tailwind CSS · **{tc['Tailwind CSS']}**",
        f"▲ Next.js · **{tc['Next.js']}**",
        f"⚡ Vite · **{tc['Vite']}**",
        f"🧊 Three.js · **{tc['Three.js']}**",
        f"🐻 Zustand · **{tc['Zustand']}**",
    ]
    be = [
        f"⚡ FastAPI · **{tc['FastAPI']}**",
        f"🧱 SQLAlchemy + Pydantic · **{min(tc['SQLAlchemy'], tc['Pydantic'])}**",
        f"🚂 Express · **{tc['Express']}**",
        f"🛠️ Alembic · **{tc['Alembic']}**",
        f"🧪 pytest · **{tc['pytest']}** *(+ Vitest · {tc['Vitest']})*",
        f"🛡️ Zod · **{tc['Zod']}** *(+ Prisma · {tc['Prisma']})*",
    ]
    inf = [
        f"🐳 Docker · **{ic['Docker']}**",
        f"🐘 PostgreSQL · **{ic['PostgreSQL']}**",
        f"⚙️ GitHub Actions CI · **{ic['GitHub Actions CI']}** *(+ profile)*",
        f"🟥 Redis · **{ic['Redis']}**",
        f"🧭 pgvector · **{tc['pgvector']}** *(+ SQLite · {ic['SQLite']})*",
        f"☸️ Terraform · **{ic['Terraform']}** *(+ K8s · {ic['Kubernetes']})*",
    ]

    rows = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in zip(fe, be, inf))
    total_k = total_lines // 1000

    return (
        "## 📊 Top Skills (measured from my repos)\n\n"
        f"*Measured by non-blank lines of code and how many repos use each tool, across {metrics['repo_count']} public repositories ({total_k}k+ lines).*\n\n"
        "**Languages**\n\n"
        "```text\n"
        + "\n".join(bars)
        + "\n```\n\n"
        "**Most-used frameworks & infrastructure** *(number of repos)*\n\n"
        "| Frontend | Backend | Data & Infra |\n"
        "| :--- | :--- | :--- |\n"
        + rows
    )


def call_gemini(prompt: str) -> str:
    from google import genai
    from google.genai import types

    is_vertex_express = GEMINI_API_KEY.startswith("AQ.")
    client = genai.Client(vertexai=is_vertex_express, api_key=GEMINI_API_KEY)

    last_err: Exception | None = None
    for model_name in ("gemini-2.5-flash", "gemini-2.0-flash"):
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            if resp.text:
                return resp.text
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"[warn] Gemini {model_name} failed: {exc}", file=sys.stderr)
    raise RuntimeError(f"All Gemini models failed: {last_err}")


def call_github_models(prompt: str) -> str:
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN missing for GitHub Models fallback")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    last_err: Exception | None = None
    for model_name in ("openai/gpt-4.1-mini", "openai/gpt-4o-mini"):
        try:
            resp = requests.post(
                "https://models.github.ai/inference/chat/completions",
                headers=headers,
                json={
                    "model": model_name,
                    "temperature": 0.2,
                    "max_tokens": 3000,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a Staff Engineer writing crisp, strictly factual, "
                                "recruiter-ready GitHub README project descriptions. Return valid JSON only."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                },
                timeout=90,
            )
            body_preview = (resp.text or "")[:400].replace("\n", " ")
            if resp.status_code >= 400:
                raise RuntimeError(f"HTTP {resp.status_code}: {body_preview}")
            if not resp.text or not resp.text.strip():
                raise RuntimeError(
                    f"Empty response body (HTTP {resp.status_code}, "
                    f"content-type={resp.headers.get('content-type')})"
                )
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            if content:
                print(f"[info] GitHub Models succeeded with {model_name}.")
                return content
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"[warn] GitHub Models {model_name} failed: {exc}", file=sys.stderr)
    raise RuntimeError(f"All GitHub Models fallbacks failed: {last_err}")


def generate_ranked_projects(
    repo_contexts: dict[str, dict[str, Any]],
    prev_state: dict[str, Any],
) -> list[dict[str, Any]]:
    payload = []
    for name, info in sorted(repo_contexts.items()):
        payload.append(
            {
                "repo": name,
                "url": f"https://github.com/{OWNER}/{name}",
                "status": info["status"],
                "existing_entry": prev_state.get("entries", {}).get(name),
                "verified_urls_in_docs": info["urls"][:25],
                "markdown_docs": info["markdown"],
            }
        )

    prompt = (
        "You are updating the Featured Projects section of a CS engineering student's GitHub profile README.\n"
        "You are given ALL built public repositories and excerpts from their actual Markdown docs.\n\n"
        "Requirements:\n"
        "1. Include EVERY single repository provided in the input list (exact 'repo' names, no omissions, no extras).\n"
        "2. Rank ALL repositories from #1 (strongest) to last based on what SDE / Backend / Distributed Systems / Applied AI recruiters would love the most: systems depth, verified benchmarks/tests, security & reliability engineering, uniqueness, CI/CD, and live deployments.\n"
        "3. For repos with status == 'unchanged' that already have a good 'existing_entry', preserve their factual claims and style; for 'new' or 'changed' repos, write fresh details grounded strictly in their markdown_docs.\n"
        "4. Write EXACTLY 2 crisp recruiter-focused sentences/lines ('line1' = what hard problem it solves & core architecture; 'line2' = verified benchmarks, test counts, security/CI proof from the docs) plus a concise 'stack' array (5-9 tech tags).\n"
        "5. NEVER invent metrics, test counts, or URLs. Set 'live_demo_url' / 'api_docs_url' ONLY if that exact URL appears in that repo's verified_urls_in_docs (and points to a real deployed app like vercel.app / onrender.com, not localhost or github.com).\n\n"
        'Return ONLY a JSON object with shape:\n'
        '{"projects": [{"repo": "...", "title": "ProjectName — Short Descriptor", "live_demo_url": null, "api_docs_url": null, "line1": "...", "line2": "...", "stack": ["Python", "FastAPI"]}]}\n\n'
        "REPOSITORIES:\n"
        + json.dumps(payload, ensure_ascii=False)
    )

    raw_text: str | None = None
    if GEMINI_API_KEY:
        try:
            raw_text = call_gemini(prompt)
            print("[info] Ranked projects generated via Gemini API.")
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] Falling back to GitHub Models after Gemini error: {exc}", file=sys.stderr)

    if raw_text is None:
        raw_text = call_github_models(prompt)
        print("[info] Ranked projects generated via GitHub Models fallback.")

    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()

    parsed = json.loads(raw_text)
    projects = parsed.get("projects", [])

    # Validate completeness and sanitize URLs against doc ground truth
    expected = set(repo_contexts.keys())
    seen: set[str] = set()
    cleaned: list[dict[str, Any]] = []
    for item in projects:
        rname = item.get("repo")
        if rname not in expected or rname in seen:
            continue
        seen.add(rname)
        allowed_urls = set(repo_contexts[rname]["urls"])
        demo = item.get("live_demo_url")
        if demo not in allowed_urls or "localhost" in (demo or "") or "github.com" in (demo or ""):
            demo = None
        api_docs = item.get("api_docs_url")
        if api_docs not in allowed_urls or "localhost" in (api_docs or "") or "github.com" in (api_docs or ""):
            api_docs = None

        cleaned.append(
            {
                "repo": rname,
                "title": (item.get("title") or rname).strip(),
                "live_demo_url": demo,
                "api_docs_url": api_docs,
                "line1": (item.get("line1") or "").strip(),
                "line2": (item.get("line2") or "").strip(),
                "stack": [str(s).strip() for s in (item.get("stack") or []) if str(s).strip()][:9],
            }
        )

    if seen != expected:
        missing = sorted(expected - seen)
        raise RuntimeError(f"Model omitted repositories from ranking: {missing}")

    return cleaned


def render_featured_projects(projects: list[dict[str, Any]]) -> str:
    blocks = [
        "## 🚀 Featured Projects\n",
        f"*All {len(projects)} projects built across distributed systems, applied AI, cloud-native infrastructure, and full-stack engineering — ranked by systems depth and recruiter impact.*\n",
    ]
    for idx, p in enumerate(projects, start=1):
        repo_url = f"https://github.com/{OWNER}/{p['repo']}"
        heading = f"### {idx}. [{p['title']}]({repo_url})"
        if p.get("live_demo_url"):
            heading += f" • [Live Demo]({p['live_demo_url']})"
        if p.get("api_docs_url"):
            heading += f" • [API Docs]({p['api_docs_url']})"

        stack_str = " · ".join(f"`{s}`" for s in p["stack"])
        lines = [heading, p["line1"]]
        if p["line2"]:
            lines.append(p["line2"])
        if stack_str:
            lines.append(f"**Stack:** {stack_str}")
        blocks.append("\n".join(lines) + "\n")

    return "\n".join(blocks).rstrip()


def patch_readme(top_skills_md: str, projects_md: str) -> bool:
    original = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(## 📊 Top Skills \(measured from my repos\).*?)(?=\n---\n\n## 🏆 Hackathons & Achievements)",
        re.DOTALL,
    )
    replacement = f"{top_skills_md}\n\n---\n\n{projects_md}"
    updated, count = pattern.subn(lambda _: replacement, original, count=1)
    if count != 1:
        raise RuntimeError("Could not locate Top Skills / Featured Projects markers in README.md")
    if updated == original:
        return False
    README_PATH.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    prev_state: dict[str, Any] = {}
    if STATE_PATH.is_file():
        try:
            prev_state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prev_state = {}
    prev_shas: dict[str, str] = prev_state.get("shas", {})

    raw_repos = list_project_repos()
    active_repos: dict[str, dict[str, Any]] = {}
    for r in raw_repos:
        sha = get_latest_human_commit_sha(r["name"], r["default_branch"])
        if not sha:
            continue
        active_repos[r["name"]] = {
            "sha": sha,
            "clone_url": r["clone_url"],
            "default_branch": r["default_branch"],
        }

    added = sorted(set(active_repos) - set(prev_shas))
    removed = sorted(set(prev_shas) - set(active_repos))
    changed = sorted(
        name for name in set(active_repos) & set(prev_shas) if active_repos[name]["sha"] != prev_shas[name]
    )

    print(
        f"[info] Found {len(active_repos)} non-empty repos "
        f"(added={added}, changed={changed}, removed={removed}, force={FORCE_REFRESH})"
    )

    if not added and not removed and not changed and not FORCE_REFRESH:
        print("[info] No repository changes detected; skipping README update.")
        return 0

    tmp_dir = Path(tempfile.mkdtemp(prefix="profile_sync_"))
    try:
        repo_dirs: dict[str, Path] = {}
        repo_contexts: dict[str, dict[str, Any]] = {}

        for name, meta in sorted(active_repos.items()):
            dest = tmp_dir / name
            if not shallow_clone(meta["clone_url"], dest):
                print(f"[warn] Failed to clone {name}, skipping.", file=sys.stderr)
                continue
            repo_dirs[name] = dest
            tracked = git_tracked_files(dest)
            md_text, urls = collect_markdown_context(dest, tracked)
            status = "new" if name in added else ("changed" if name in changed else "unchanged")
            repo_contexts[name] = {
                "sha": meta["sha"],
                "status": status,
                "markdown": md_text,
                "urls": urls,
            }

        metrics = measure_top_skills(repo_dirs)
        top_skills_md = render_top_skills(metrics)
        ranked_projects = generate_ranked_projects(repo_contexts, prev_state)
        projects_md = render_featured_projects(ranked_projects)

        readme_changed = patch_readme(top_skills_md, projects_md)

        new_state = {
            "shas": {name: info["sha"] for name, info in repo_contexts.items()},
            "entries": {p["repo"]: p for p in ranked_projects},
        }
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(new_state, indent=2) + "\n", encoding="utf-8", newline="\n")

        print(f"[info] Done. README modified={readme_changed}, tracked repos={len(ranked_projects)}.")
        return 0
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
