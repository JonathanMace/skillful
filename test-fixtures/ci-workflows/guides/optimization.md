# Optimizing Slow GitHub Actions Pipelines

Use this guide when CI/CD runs are too slow, too expensive, too noisy, or too
variable. The goal is to reduce wall-clock time and compute waste without
reducing signal quality, weakening security, or making workflows harder to
operate.

## Procedure

1. **Measure before changing**
   - Identify which workflows, jobs, and steps dominate runtime.
   - Separate queue time from execution time.
   - Compare median duration, not only worst-case outliers.
   - Determine whether the complaint is about developer feedback time, deploy latency, or runner cost.

2. **Find the true bottleneck class**
   - **Checkout/setup overhead**: repeated tool installation, large repositories, repeated dependency downloads.
   - **Dependency work**: slow package installation, cache misses, lockfile churn.
   - **Build/test work**: unnecessary full rebuilds, redundant test suites, poor parallelism.
   - **Workflow structure**: serialized jobs that could run independently, duplicate work across workflows.
   - **Artifact/log overhead**: large uploads, verbose reports, unnecessary retention.
   - **Environment contention**: concurrency groups, external service rate limits, deployment locks.

3. **Optimize for the user-visible critical path first**
   - Speed up the checks developers wait on before merge.
   - Defer non-blocking or expensive reporting to later jobs when appropriate.
   - Separate fast validation from heavy integration or release logic.
   - Cancel stale runs for the same branch or PR.

4. **Eliminate redundant work**
   - Do not rebuild or reinstall if the exact result can be reused safely.
   - Build once and share artifacts when downstream jobs need the same output.
   - Avoid running identical setup in many jobs unless parallel speedup outweighs the duplication.
   - Consolidate overlapping workflows if they duplicate the same validation on the same events.

5. **Fix dependency caching intentionally**
   - Cache only what is safe and worth restoring.
   - Use keys that match the real invalidation boundary, usually lockfiles plus environment dimensions.
   - Do not hide correctness problems behind over-broad caches.
   - Verify restore-hit behavior and whether cache save time outweighs cache benefit.

6. **Reduce matrix cost**
   - Keep only matrix dimensions that provide distinct value.
   - Run the full matrix on protected branches and a narrower matrix on routine PRs if that fits the risk profile.
   - Remove combinations that are redundant or unsupported.
   - Consider splitting smoke coverage from exhaustive compatibility coverage.

7. **Parallelize where it helps**
   - Break independent jobs into parallel units.
   - Avoid artificial serialization through unnecessary `needs`.
   - Shard large test suites only if shard balancing and reporting remain understandable.
   - Parallelism is good only if setup duplication does not erase the win.

8. **Scope work to relevant changes**
   - In monorepos, run service-specific jobs only when related files change.
   - Avoid triggering deploy or package jobs on documentation-only changes unless required.
   - Be careful that path filters do not accidentally skip required branch protection checks.

9. **Minimize artifact and logging overhead**
   - Upload only artifacts that are actually consumed or useful for triage.
   - Use reasonable retention periods.
   - Avoid huge caches or artifacts whose transfer time dominates execution.
   - Keep logs actionable; excessive verbosity slows analysis and may increase storage overhead.

10. **Tune runner and tool setup choices**
   - Use the smallest runner that meets performance and memory needs.
   - Pin runtime versions to avoid unexpected setup drift.
   - If self-hosted runners are used, ensure the operational cost and consistency tradeoff is worth it.
   - Avoid relying on preinstalled tools whose availability may change.

11. **Preserve correctness and security while optimizing**
   - Do not drop important checks solely for speed without explicit agreement.
   - Do not broaden permissions to simplify caching or artifact flow.
   - Do not trade deterministic builds for slightly faster but flaky pipelines.
   - Prefer predictable pipelines over highly clever pipelines.

12. **Re-measure and compare**
   - Compare before/after duration for the same workflow and event type.
   - Check whether the change improved median time, critical path time, or cost.
   - Confirm logs, artifacts, and required checks remain understandable.
   - Keep the optimization only if the gain is real and the workflow remains maintainable.

## Rules and Constraints

- Measure first; avoid speculative “optimizations.”
- Optimize the critical path developers feel, not just total compute minutes.
- Preserve required coverage unless the requested scope explicitly changes.
- Do not let caches become hidden state that masks missing dependencies or bad builds.
- Prefer simple, explainable workflow structure over fragile micro-optimizations.
- Treat queue time and runtime as different problems; YAML changes may not fix queue congestion.
- Be cautious with path filters and conditional skips because they can affect required checks.
- Keep workflow names and job names stable when possible, especially if branch protection depends on them.
- Validate that an optimization actually helps in the target repo; generic advice is not enough.

## High-Value Optimization Levers

### Fast feedback improvements
- Cancel superseded runs with `concurrency`
- Move lint/typecheck ahead of slow integration suites
- Narrow PR matrices where risk allows
- Skip unchanged monorepo areas safely
- Reuse build artifacts across downstream jobs

### Dependency improvements
- Use native setup-action caching where available
- Ensure lockfiles are committed and stable
- Avoid cache keys that change on every run
- Revisit package manager commands for CI-safe fast paths

### Structural improvements
- Split independent jobs
- Remove unnecessary `needs`
- Reuse workflows for repeated patterns
- Separate validation workflows from release/deploy workflows

### Waste reduction
- Shorten artifact retention
- Stop uploading unused artifacts
- Reduce duplicate runs on both `push` and `pull_request` when branch strategy makes one redundant
- Avoid running scheduled heavy jobs more often than needed

## Examples

### Example 1: Slow pull request feedback
User request:
> Our PR checks take 25 minutes. Speed them up without dropping coverage.

Approach:
1. Measure which jobs dominate the first failing-or-passing signal.
2. Add `concurrency` to cancel stale PR runs.
3. Move fast static checks earlier.
4. Reuse a built artifact rather than rebuilding in multiple jobs.
5. Keep deep integration coverage, but run it in parallel or later in the graph.
6. Compare before/after PR feedback time.

### Example 2: Cache exists but pipeline is still slow
User request:
> We cache dependencies already, but install is still slow.

Approach:
1. Check whether cache restore hits actually occur.
2. Inspect cache key invalidation boundaries.
3. Verify whether install commands still rebuild or verify large trees after restore.
4. Measure cache save/upload overhead.
5. Keep the cache only if the net runtime improves.

### Example 3: Oversized matrix
User request:
> Our matrix runs across too many versions and OSes.

Approach:
1. Identify which combinations are required for correctness or support policy.
2. Keep high-value coverage on PRs.
3. Move exhaustive compatibility coverage to main, nightly, or release workflows if appropriate.
4. Ensure branch protection still reflects the intended required checks.
5. Document the new coverage strategy.

## Useful Workflow Patterns

### Cancel stale branch runs
