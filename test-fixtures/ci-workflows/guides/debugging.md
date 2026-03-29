# Debugging GitHub Actions Failures

Use this guide when a workflow run, job, or check is failing, flaky, or producing
unexpected results. The goal is to identify the exact failing step, determine
whether the problem is workflow logic, environment, permissions, secrets, or
repository code, and then apply the narrowest reliable fix.

## Procedure

1. **Start with the failing run, not assumptions**
   - Identify the workflow name, run ID, branch, event type, and failing job.
   - Gather the exact error text, failing step name, and exit code.
   - Distinguish between a consistent failure and an intermittent one.

2. **Inspect workflow structure before reading long logs**
   - Open the workflow YAML and locate the failing job and step.
   - Note `on`, `permissions`, `env`, `defaults`, `needs`, matrix settings, and reusable workflow calls.
   - Check whether the failure is in repo code or in workflow orchestration.

3. **Read the smallest useful amount of log data first**
   - Read the failed step and nearby context before pulling the entire log.
   - Capture the first actionable error, not every downstream symptom.
   - Watch for hidden root causes: missing files, wrong working directory, missing tools, auth failures, and artifact path mismatches.

4. **Classify the failure**
   - **Workflow authoring problem**: invalid YAML, unsupported syntax, bad expressions, bad conditionals, missing outputs.
   - **Environment problem**: runner image differences, unavailable tools, wrong shell, platform-specific path issues.
   - **Dependency problem**: lockfile drift, cache poisoning, upstream package outage, registry auth failure.
   - **Permission or secret problem**: insufficient `permissions`, unavailable secret on forks, OIDC misconfiguration.
   - **Repository code problem**: tests or builds genuinely failing.
   - **Flake or timing problem**: race conditions, network instability, service readiness, parallel contention.

5. **Check recent change boundaries**
   - Look at the commit range or PR diff that introduced the failure.
   - Compare the last green run to the first red run.
   - If the workflow recently changed, inspect workflow YAML first; otherwise inspect application changes first.

6. **Reproduce locally when practical**
   - Run the same build, test, or lint command locally with the same shell and working directory.
   - Match runtime versions from the workflow: language version, package manager, OS, architecture.
   - If local reproduction is impossible, document why and continue with remote evidence.

7. **Validate GitHub Actions-specific assumptions**
   - Confirm action versions and whether they are pinned appropriately.
   - Check matrix expansion values and `if:` expressions.
   - Verify `needs` dependencies and required outputs exist.
   - Confirm artifact upload/download names and paths match exactly.
   - Verify reusable workflow inputs, secrets, and outputs line up with the caller.

8. **Check permissions and trust boundaries**
   - Ensure `GITHUB_TOKEN` permissions are sufficient but minimal.
   - Remember that secrets may not be available for forked pull requests.
   - For cloud deploys, verify OIDC audience, subject, role assumption, and environment protection rules.
   - For package publishing, verify registry scopes, tokens, and provenance requirements.

9. **Look for environment drift**
   - Compare failing runner image to previous successful runs.
   - Check tool setup actions and pinned versions.
   - Watch for implicit tools that used to exist on the runner but are no longer guaranteed.
   - Prefer explicit setup steps over relying on preinstalled software.

10. **Fix the root cause, not the symptom**
   - Update workflow logic only if the workflow is wrong.
   - Update repository code only if the code is wrong.
   - Avoid masking failures with `continue-on-error`, blanket retries, or overly broad conditionals unless that behavior is intentional and justified.

11. **Re-run the narrowest useful validation**
   - Validate the affected command locally if possible.
   - Re-run the relevant workflow or job after the change.
   - If the issue is flaky, gather evidence across multiple runs before declaring success.

12. **Document the failure mode in the change**
   - Explain what failed, why it failed, and why the chosen fix addresses the root cause.
   - Note any follow-up hardening work if the immediate fix is intentionally minimal.

## Rules and Constraints

- Prefer the exact failing step over reading entire logs blindly.
- Do not assume the newest error line is the root cause.
- Do not weaken security to get green CI; fix permissions correctly.
- Do not replace a failing check with a skipped check unless the requirement truly changed.
- Do not leave mutable major tags unexplained for critical actions; pin deliberately.
- Treat flaky failures as bugs to be explained, not noise to ignore.
- If secrets or tokens are involved, never print or persist sensitive values.
- Keep fixes surgical: change the workflow, script, or code component actually responsible.
- If the run failed on a forked PR, explicitly consider secret availability and token restrictions.
- If the failure is caused by repository code, still verify the workflow did not amplify or hide it.

## Common Failure Patterns

### Dependency install failures
- Lockfile does not match manifest
- Private registry auth missing
- Cache restored incompatible dependencies
- Upstream package deleted or rate-limited

### Test failures
- Test relies on local state not present in CI
- Wrong environment variables or test database config
- Parallel execution exposes hidden race condition
- Service container not ready before tests start

### Build failures
- Missing generated files
- Different Node, Python, Java, or .NET version than local
- Platform-specific path or shell behavior
- Wrong working directory in monorepo job

### Deployment failures
- Missing environment approval
- OIDC or cloud role trust mismatch
- Insufficient `permissions`
- Artifact name mismatch between build and deploy jobs

## Examples

### Example 1: Missing permissions
User request:
> Debug why the release workflow can create tags locally but fails in Actions.

Approach:
1. Inspect the failing job and release step logs.
2. Open the workflow and check job-level `permissions`.
3. Confirm the step uses `GITHUB_TOKEN` to create a release or push a tag.
4. Add only the required permission such as `contents: write`.
5. Re-run the workflow and confirm the release step succeeds.

### Example 2: Matrix-specific failure
User request:
> The Python 3.12 job fails but 3.11 passes.

Approach:
1. Compare the matrix entries and setup steps.
2. Reproduce with the failing version locally if possible.
3. Check dependency compatibility and tool setup pinning.
4. Fix version-specific code or dependency constraints.
5. Re-run only the affected matrix job if available.

### Example 3: Artifact handoff broken
User request:
> Deploy job says artifact not found after the build job passes.

Approach:
1. Inspect upload and download artifact step names and paths.
2. Confirm artifact name matches exactly across jobs.
3. Verify `needs: build` exists and any conditional logic does not skip upload.
4. Fix naming or conditional mismatch.
5. Re-run and verify the deploy job retrieves the artifact.

## Done Criteria

A debugging task is done when all of the following are true:

- The exact failing step and root cause are identified.
- The fix addresses the root cause rather than suppressing the symptom.
- The affected command, job, or workflow has been re-validated.
- Security posture is preserved or improved, especially around tokens, secrets, and permissions.
- Any workflow assumptions changed by the fix are reflected in comments, commit notes, or related documentation when appropriate.
- If the issue was flaky, there is enough rerun evidence to justify confidence in the fix.
