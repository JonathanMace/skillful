# Behavioral Tests

Behavioral tests verify that skills produce correct results when invoked by Copilot. Unlike structural compliance tests (which check format), behavioral tests check whether skills actually work.

## How Behavioral Tests Work

1. Each test file contains **prompts** and **expected outcomes**.
2. To run a test, give the test file's prompt section to a subagent (or paste it into a Copilot CLI session).
3. Compare the subagent's output against the expected outcome.
4. Score the result using the criteria defined in the test file.

### Running a Single Test

```
Read tests/behavioral/description-discovery.md and execute the test prompts described in it.
Report results using the scoring criteria defined in the file.
```

### Running All Behavioral Tests

```
Read each test file in tests/behavioral/ and execute all test prompts.
Report results per-test and provide a summary.
```

## Scoring

Each test prompt is scored individually:

| Rating | Meaning |
|--------|---------|
| **PASS** | Output matches expected outcome within tolerance |
| **NEEDS WORK** | Partially correct — right direction but missing key elements |
| **FAIL** | Wrong outcome, wrong skill invoked, or critical elements missing |

## Test Files

| File | Tests | Skill(s) Covered |
|------|-------|-----------------|
| `description-discovery.md` | Auto-invocation accuracy | All skills (description quality) |
| `instruction-placement.md` | Correct file placement | `writing-custom-instructions` |
| `skill-authoring.md` | Skill creation quality | `writing-skills` |
| `git-workflow.md` | Git lifecycle correctness | `git-checkpoint` |

## Adding a Behavioral Test

1. Create a new `.md` file in this directory.
2. Include these sections:
   - **Purpose** — what the test validates and which skill(s) it covers
   - **Test Prompts** — the exact prompts to use, with context
   - **Expected Outcome** — what correct behavior looks like for each prompt
   - **Scoring Criteria** — specific PASS/NEEDS WORK/FAIL definitions
3. Make the file self-contained — a subagent should be able to run it without prior context.
4. Add the test to the table above and to `tests/README.md`.

## Notes

- Behavioral tests are inherently non-deterministic. Small variations in output are expected.
- Focus scoring on whether the **intent and structure** are correct, not exact wording.
- When possible, have a reviewer subagent score results to reduce manual effort.
- Results can optionally be appended to `tests/LAST-RUN.md` for comparison across runs.
