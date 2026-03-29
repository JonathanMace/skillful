---
name: ci-workflows
description: >-
  Diagnose failing GitHub Actions pipelines, author new workflows, and optimize
  slow CI/CD runs.  Use when asked to debug CI failures, fix broken builds,
  write or edit GitHub Actions workflows, or speed up pipelines.
license: MIT
---

# CI Workflows

This skill covers GitHub Actions-based CI/CD work. Keep this dispatcher thin:
read the guide that matches the task before acting.

- **Debugging a failing workflow or job** — read and follow `guides/debugging.md`
- **Authoring or changing a workflow** — read and follow `guides/authoring.md`
- **Optimizing a slow pipeline** — read and follow `guides/optimization.md`

If the task spans multiple areas, read the relevant guides in this order:

1. `guides/debugging.md` to establish the current failure mode or bottleneck
2. `guides/authoring.md` to implement or restructure the workflow safely
3. `guides/optimization.md` to reduce runtime without weakening correctness

Routing rules:

- If the user mentions **failed Actions runs, broken checks, red CI, logs, or flaky jobs**,
  start with `guides/debugging.md`.
- If the user mentions **new workflows, triggers, matrices, deployments, releases,
  reusable workflows, or permissions**, start with `guides/authoring.md`.
- If the user mentions **slow pipelines, long build times, cache misses, queue time,
  redundant jobs, or cost/performance**, start with `guides/optimization.md`.

When a task touches multiple concerns, follow all applicable guides and preserve
workflow correctness, least-privilege permissions, and clear validation steps.
