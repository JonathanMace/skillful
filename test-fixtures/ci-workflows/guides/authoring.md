# Authoring GitHub Actions Workflows

Use this guide when creating a new GitHub Actions workflow, significantly
reworking an existing one, or adding CI/CD automation such as build, test,
release, deploy, or scheduled maintenance jobs. The goal is a workflow that is
correct, secure, understandable, and cheap to operate.

## Procedure

1. **Define the workflow outcome first**
   - Write down what the workflow must accomplish: test, package, release, deploy, scan, or automate maintenance.
   - Identify the event that should trigger it: `pull_request`, `push`, `workflow_dispatch`, `schedule`, `release`, or reusable `workflow_call`.
   - Decide what success means in observable terms: green checks, published package, deployed artifact, or generated output.

2. **Determine whether to create, edit, or reuse**
   - Prefer extending an existing workflow when the responsibility clearly belongs there.
   - Create a new workflow when the trigger, permissions, runtime, or ownership is distinct.
   - Consider reusable workflows for shared patterns across services or repositories.

3. **Design the job graph before writing YAML**
   - Split work into jobs with clear responsibilities.
   - Use `needs` to express dependencies explicitly.
   - Separate build, test, package, and deploy concerns where that improves observability and rerun behavior.
   - Decide whether artifacts, caches, or outputs need to cross job boundaries.

4. **Choose runners and execution model**
   - Select the minimum runner type that meets requirements.
   - Use a matrix only when the added coverage is worth the runtime cost.
   - For monorepos, scope jobs to changed areas when possible.
   - For deploy workflows, separate approval-governed environments from ordinary CI.

5. **Set permissions deliberately**
   - Start with least privilege.
   - Add only the permissions needed for checkout, commenting, packages, releases, deployments, or OIDC.
   - Prefer OIDC federation over long-lived cloud credentials when supported.
   - Be explicit about environment protections and secret usage.

6. **Author the workflow YAML**
   - Give the workflow and jobs clear names.
   - Use `actions/checkout` and setup actions explicitly.
   - Pin versions intentionally and keep action usage consistent.
   - Use `defaults.run.working-directory` or step-level `working-directory` in monorepos instead of repeating `cd`.
   - Keep shell commands readable and fail-fast.

7. **Handle data flow explicitly**
   - Use outputs for small values and artifacts for files.
   - Name artifacts predictably.
   - Keep environment variables scoped as tightly as practical.
   - Avoid hidden coupling between jobs through implicit repository state.

8. **Make failure modes clear**
   - Name steps so logs are readable.
   - Put expensive setup after fast validation when possible.
   - Use `timeout-minutes` for long-running or risk-prone jobs.
   - Add concurrency controls for workflows that should cancel stale runs or serialize deploys.

9. **Design for trusted and untrusted contexts**
   - Treat forked pull requests differently from trusted branches.
   - Avoid exposing secrets to untrusted code paths.
   - Be cautious with `pull_request_target`; use it only when the trust model is well understood.
   - Separate validation from privileged publish/deploy steps when necessary.

10. **Add local and operational validation**
   - Validate YAML structure and expression logic carefully.
   - Sanity-check commands locally if possible.
   - Consider whether branch protection, required checks, environments, or repository settings must be updated along with the workflow.

11. **Document intent in the workflow itself**
   - Use concise comments only where behavior is non-obvious.
   - Prefer clear naming and structure over heavy inline commentary.
   - If the workflow depends on repo settings, call that out in the change notes.

12. **Verify end-to-end behavior**
   - Confirm the workflow appears under the expected event.
   - Confirm the jobs run in the intended order.
   - Confirm success, failure, and cancellation states are understandable to future maintainers.

## Rules and Constraints

- Keep workflow responsibilities clear; do not pack unrelated automation into one YAML file just because it shares a trigger.
- Prefer least-privilege `permissions`; never grant broad write access by default.
- Prefer official or well-maintained actions, and pin versions intentionally.
- Do not rely on undocumented runner state; install or set up required tooling explicitly.
- Avoid duplicated logic across workflows when a reusable workflow or shared action would be clearer.
- Use secrets only when required, and assume pull requests from forks cannot access them.
- Avoid `continue-on-error` unless the step is intentionally non-blocking and the user experience is still clear.
- Use concurrency controls for deploys, previews, or branch-scoped workflows that should not overlap.
- Make job names stable and human-readable because they become required checks and operational signals.
- If introducing a new required check, ensure its name is durable and unlikely to churn.

## Authoring Checklist

### Trigger selection
- `pull_request` for validation before merge
- `push` for branch protection, default branch CI, or post-merge tasks
- `workflow_dispatch` for operator-triggered tasks
- `schedule` for maintenance, auditing, or sync jobs
- `workflow_call` for reusable workflows shared across repos or directories

### Job structure
- Fast lint/typecheck before slow integration tests when appropriate
- Build once, test many if artifacts make that worthwhile
- Deploy from a known artifact rather than rebuilding in deploy jobs
- Separate privilege boundaries between test/build and publish/deploy

### Security design
- Explicit `permissions`
- Environment-scoped secrets
- OIDC for cloud auth
- No secret exposure to untrusted pull request code
- Careful use of third-party actions

## Examples

### Example 1: Pull request validation workflow
Use when the user asks:
> Create a workflow that runs lint and tests on pull requests.

Recommended shape:
1. Trigger on `pull_request`
2. Add a fast setup job or separate lint and test jobs
3. Use explicit runtime setup
4. Cache dependencies if justified
5. Publish test reports or artifacts only if they help triage failures
6. Keep permissions read-only unless comments or statuses require more

### Example 2: Reusable deployment workflow
Use when the user asks:
> Factor our deploy logic into a reusable workflow called by multiple services.

Recommended shape:
1. Create a `workflow_call` workflow with explicit inputs and secrets
2. Validate all required inputs and defaults
3. Keep deploy permissions and environment configuration inside the reusable workflow
4. Return outputs only if callers truly need them
5. Document call sites and required repository/environment settings

### Example 3: Release workflow
Use when the user asks:
> Publish a package when a tag is pushed.

Recommended shape:
1. Trigger on tag push
2. Build once and store the artifact
3. Authenticate with least privilege for the package registry
4. Publish from the built artifact
5. Gate release creation or provenance steps behind explicit permissions and branch/tag conventions

## Minimal Example Skeleton
