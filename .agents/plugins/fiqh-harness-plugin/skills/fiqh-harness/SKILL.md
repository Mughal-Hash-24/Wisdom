---
name: fiqh-harness
description: "Evaluates, tests, and grades the Fiqh Madhab Pipeline and its subagents. Use this skill whenever the user asks to 'evaluate fiqh', 'test madhab-pipeline', 'grade fiqh rulings', 'run fiqh benchmark', or 'harness fiqh'. Supports baseline comparison and qualitative grading."
---

# Fiqh Harness Orchestrator

This skill orchestrates the evaluation of the Fiqh Madhab Pipeline, verifying both structural compliance and qualitative theological rigor.

## Execution Mode: Hybrid (Sequential + Subagent)

---

## Benchmark Test Suite

The harness tests the pipeline using three distinct categories of questions to evaluate coverage:

| ID | Category | Question | Slug | Concept |
|:---|:---|:---|:---|:---|
| **TC-1** | **Classical** | "What is the ruling on buying or selling gold with silver in delay (Riba al-Nasi'ah)?" | `gold-silver-nasiha` | `riba-usury` |
| **TC-2** | **Contemporary** | "What is the ruling on trading cryptocurrencies and digital tokens?" | `cryptocurrency-trading` | `cryptocurrency` |
| **TC-3** | **Mixed/Derived** | "What is the ruling on using AI-generated avatars of human beings in commercial advertisements?" | `ai-avatars-commercial` | `digital-representation` |

---

## Orchestrator Workflow

### Phase 0: Context Verification & Input Selection
1. Check if the Fiqh Harness workspace directory `/home/ibtasaam/Kybernetes/.fiqh_harness_workspace` exists. If not, create it.
2. Check for existing iterations to determine the current iteration number `iteration-N`.
3. Ask the user which test case they want to run (**TC-1**, **TC-2**, **TC-3**, or **All**). If they ask to run a custom question, parse it into `question`, `slug`, and `concept` values.

### Phase 1: Execution Setup
1. Record the start epoch timestamp `start_time` in seconds.
2. Initialize the iteration output directories:
   * Programmatic outputs: `.fiqh_harness_workspace/iteration-N/with_skill/outputs/`
   * Grading and timing configs: `.fiqh_harness_workspace/iteration-N/with_skill/`

### Phase 2: Pipeline Execution
1. Trigger the target `madhab-pipeline` skill for the chosen question.
2. Wait for the pipeline to finalize its output in `30_Knowledge_Base/Fiqh/{slug}/`.
3. Copy the five generated files from `30_Knowledge_Base/Fiqh/{slug}/` to `.fiqh_harness_workspace/iteration-N/with_skill/outputs/` for testing isolation and historic archiving.

### Phase 3: Programmatic Verification
1. Propose and run the programmatic validation script:
   ```bash
   python3 /home/ibtasaam/Kybernetes/.agents/plugins/fiqh-harness-plugin/skills/fiqh-harness/scripts/run_fiqh_eval.py \
     --dir /home/ibtasaam/Kybernetes/.fiqh_harness_workspace/iteration-N/with_skill/outputs/ \
     --slug {slug} \
     --concept {concept} \
     --start-time {start_time} \
     --out-dir /home/ibtasaam/Kybernetes/.fiqh_harness_workspace/iteration-N/with_skill/
   ```
2. Read the generated `.fiqh_harness_workspace/iteration-N/with_skill/grading_programmatic.json` file using `view_file`.

### Phase 4: Qualitative Grading
1. Invoke the `@fiqh-grader` subagent to evaluate the generated output:
   * **TypeName**: `fiqh-grader`
   * **Role**: `Fiqh Grader`
   * **Prompt**:
     ```
     Please grade the Fiqh files in `.fiqh_harness_workspace/iteration-N/with_skill/outputs/`.
     - Cross-reference rulings with the grading principles in `/home/ibtasaam/Kybernetes/.agents/plugins/fiqh-harness-plugin/skills/fiqh-harness/rules/fiqh-grading-principles.md`.
     - Perform a web search to verify cited books and Hadiths.
     - Evaluate Hanafi, Maliki, Shafi'i, Hanbali files, and the Synthesis.
     - Write a detailed qualitative assessment report to `.fiqh_harness_workspace/iteration-N/with_skill/grading_qualitative.json`. Include a 1-10 score and structured critique for each school and the synthesis.
     ```
2. Wait for `@fiqh-grader` to complete and read `.fiqh_harness_workspace/iteration-N/with_skill/grading_qualitative.json`.

### Phase 5: Compile Report & Synthesis
1. Merge the programmatic and qualitative grading results into a unified `/home/ibtasaam/Kybernetes/.fiqh_harness_workspace/iteration-N/with_skill/grading.json` file.
2. Create a final evaluation report artifact `fiqh_harness_report.md` in the user's workspace, summarizing:
   * Overall Pass Rate & Programmatic score.
   * School-by-school qualitative scores (out of 10).
   * Detailed breakdown of citation issues, structural flaws, or logical deviations.
   * Total execution time from `timing.json`.
   * Clear recommendations for refining the pipeline or specific school prompts.

---

## Error Handling
* **Grader Failure**: If the `@fiqh-grader` subagent fails or times out, fall back to programmatic grading scores only, note the grader failure in the final report, and proceed.
* **Missing Files**: If the pipeline fails to create the files, the python script will report a 0% pass rate. Log the exact error and prompt the user to check the subagent logs for the failing school.

---

## Test Scenarios

### Successful Run
1. User requests `harness fiqh` for **TC-2**.
2. Pipeline runs and writes output to `30_Knowledge_Base/Fiqh/cryptocurrency-trading/`.
3. Programmatic validation passes structural check (all 5 files present, tags correct, links active).
4. `fiqh-grader` runs and scores the legal reasoning 8/10, confirming citations for *Radd al-Muhtar* and *Al-Umm*.
5. Overall report is displayed with score 92%.

### Failure Run
1. User runs `harness fiqh` for **TC-1**.
2. Hanbali agent fails to produce content, so `Hanbali - gold-silver-nasiha.md` is missing or empty.
3. Programmatic check reports failure for Hanbali file existence and structure.
4. Report highlights the failure, flags the overall score as degraded (e.g. 60%), and advises re-dispatching the Hanbali subagent.
