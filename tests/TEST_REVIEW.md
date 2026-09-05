# Test value rubric and audit

Baseline: commit `4527eac` (43 tests). Reviewed 2026-09-05.

## Rubric

A necessary test detects a meaningful regression using evidence that the tested system actually produces. Score each dimension from 0 to 2 before deciding what to keep.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Consequence (C) | Cosmetic or no identifiable failure | Recoverable confusion or wasted work | Lost work, false success, broken execution, or an important contract violation |
| Evidence (E) | Matches prose or replays behavior written in the test itself | Indirect proxy with limited claims | Exercises shipped behavior or validates a machine-consumed artifact |
| Durability (D) | Breaks on harmless wording or implementation changes | Mixes stable and brittle assertions | Checks outcomes or stable interfaces |
| Unique coverage (U) | Redundant with stronger tests | Partially overlapping coverage | Distinct failure mode |
| Proportionality (P) | Maintenance cost exceeds protection | Some excess setup or incidental assertions | Small, deterministic, and worth maintaining |

Keep scores of 8–10 only when C >= 1 and E = 2. Narrow a test when it contains useful coverage obscured by brittle or unrelated assertions; score the original and explain what survives. Remove tests without a meaningful oracle even if the named requirement is important. A lower count is not a goal by itself.

Markdown is part of this product, but different assertions provide different evidence. A missing linked file is a real packaging defect; the presence of a sentence about approval does not prove approval is respected. A deterministic test of a declared machine-readable invocation flag is appropriate. Rhetorical quality, user choice, and instruction adherence require representative agent-session evaluations, not substring checks.

Fake external executables are appropriate when the shipped wrapper invokes them and its outputs, exit status, and file effects are asserted. A state machine implemented only inside a test cannot establish end-to-end workflow correctness.

## Per-test decisions

The audit below records each baseline test, its original C/E/D/U/P scores, and the failure it protects or fails to demonstrate.

### Script behavior: 17 retained

Scores are shown in C/E/D/U/P order. Narrowing preserves the useful behavioral test while removing incidental assertions or correcting its stated scope.

| Baseline test | C/E/D/U/P | Total | Decision and rationale |
| --- | --- | --- | --- |
| `ContextDiscoveryTests.test_prioritizes_context_and_excludes_generated_and_secret_files` | 2/2/1/2/2 | 9 | Narrow: preserve ranked discovery and explicit path inclusion/exclusion. Replace the incidental skipped-file count with direct exclusion of `.env`. |
| `ContextDiscoveryTests.test_succeeds_without_style_or_impeccable_files` | 1/2/2/2/2 | 9 | Keep: a minimal project works without optional style dependencies; this differs from the richer discovery fixture. |
| `DraftReservationTests.test_never_overwrites_an_existing_draft` | 2/2/2/2/2 | 10 | Keep: real reservation must preserve existing writing and create a distinct draft. |
| `OutlineReservationTests.test_reserves_and_reuses_predictable_outline_path` | 2/2/2/2/2 | 10 | Keep: the helper must return a discoverable outline and preserve its content when reused. |
| `OutlineReservationTests.test_rejects_articles_outside_the_project` | 2/2/1/2/2 | 9 | Narrow: retain rejection of the outside target; remove dependence on exact stderr wording. Check file effects at the rejected destination. |
| `OutlineReservationTests.test_rejects_existing_outline_symlink` | 2/2/1/2/2 | 9 | Narrow: retain rejection and preservation of the external target; remove dependence on a particular diagnostic phrase. |
| `SloplessTests.test_missing_slopless_and_npx_blocks_before_drafting` | 2/2/2/2/1 | 9 | Narrow: verify that preflight reports blocked when no executable is available. Remove the unnecessary draft fixture and the name's unsupported claim that the agent itself blocks drafting. |
| `SloplessTests.test_preflight_acquires_pinned_slopless_through_npx` | 2/2/2/2/2 | 10 | Keep: capture actual subprocess arguments and verify pinned package selection and readiness. The package version is an intentional compatibility contract. |
| `SloplessTests.test_exact_installed_version_is_used_without_npx` | 2/2/2/2/2 | 10 | Keep: a compatible local binary must work without the fallback command, preserving local/offline execution. |
| `SloplessTests.test_captures_findings_and_confirms_a_clean_rerun` | 2/2/2/2/2 | 10 | Keep: exercise status translation, findings extraction, rule reporting, persistence, and separate rerun artifacts through the shipped wrapper. |
| `SloplessTests.test_pinned_npx_replaces_a_mismatched_installed_slopless` | 2/2/2/2/2 | 10 | Keep: prevent silent use of a different ruleset by verifying inspection of the installed binary and actual pinned fallback invocation. |
| `SloplessTests.test_pinned_npx_replaces_prerelease_installed_versions` | 2/2/2/2/2 | 10 | Keep: prevent version parsing from treating a prerelease as the pinned release. An ordinary version mismatch would not catch suffix truncation. |
| `RoughdraftTests.test_missing_roughdraft_keeps_the_draft_available` | 2/2/1/2/2 | 9 | Narrow: preserve nonfatal missing-tool status, the returned draft path, and original draft bytes; exact installation-command wording is incidental. |
| `RoughdraftTests.test_uses_documented_non_watching_mode_when_supported` | 2/2/2/2/2 | 10 | Keep: verify explicit non-watching invocation, supported JSON mode, and successful return. Assert the external command's actual logged argument list instead of echoed response flags and a weak log substring. |
| `RoughdraftTests.test_waits_for_done_reviewing_by_default` | 2/2/2/2/2 | 10 | Keep, rename for accuracy: verify default watched invocation and completion-event interpretation. An immediately returning stub does not establish actual elapsed waiting. |
| `RoughdraftTests.test_does_not_complete_a_timed_out_review` | 2/2/2/2/2 | 10 | Keep: a timeout must override a completion event and must not report false success, including the CLI's nonzero timeout exit. |
| `RoughdraftTests.test_does_not_treat_an_abandoned_review_as_complete` | 2/2/2/2/2 | 10 | Keep: preserve the distinct cancellation state and supported single-event envelope. Remove the redundant inequality after asserting the exact abandoned status. |

The retained helper tests establish command selection, result interpretation, file preservation, and reported statuses. They do not establish Slopless rule quality, real browser behavior, or agent compliance with drafting and review gates.

### Instruction assertions: 24 removed, 2 narrowed

| Baseline test | C/E/D/U/P | Total | Decision and rationale |
| --- | --- | --- | --- |
| `PremiseCouncilInstructionTests.test_premise_council_has_five_scouts_and_a_single_agent_fallback` | 2/0/0/1/0 | 3 | Remove: hardcodes a release and sentences; never observes spawning, waves, fallback, or selection. |
| `PremiseCouncilInstructionTests.test_premise_council_uses_model_activating_mirror_pairs` | 1/0/0/1/1 | 3 | Remove: counts appeal labels between exact prose delimiters; cannot establish distinct premises or exploration coverage. |
| `PremiseCouncilInstructionTests.test_old_appeal_labels_are_not_active_instructions` | 1/0/0/1/1 | 3 | Remove: a terminology blacklist can reject harmless historical explanation without detecting functional failure. |
| `PremiseCouncilInstructionTests.test_awareness_transition_precedes_scouting_and_stays_private` | 2/0/0/1/0 | 3 | Remove: sentence positions cannot establish execution order, privacy, or recovery. |
| `PremiseCouncilInstructionTests.test_fascinate_layer_is_absent_from_active_instructions` | 1/0/0/1/1 | 3 | Remove: banned words can appear in harmless context; no behavior is exercised. |
| `PremiseCouncilInstructionTests.test_awareness_transition_is_carried_through_intermediate_handoffs` | 2/0/0/0/0 | 2 | Remove: repeated phrases do not demonstrate that state survives handoffs; overlaps other awareness assertions. |
| `ArticleRouteInstructionTests.test_two_advocated_routes_gate_outline_and_proof` | 2/0/0/1/0 | 3 | Remove: template labels and lifecycle wording do not exercise route selection or approval gates. |
| `ArticleRouteInstructionTests.test_visual_generation_waits_for_stable_proof` | 2/0/0/1/1 | 4 | Remove: three phrase assertions never observe when visual work starts. |
| `InstructionContractTests.test_router_is_low_resolution_and_all_pointers_resolve` | 2/2/1/2/1 | 8 | Narrow: retain actual local-link resolution, including links within references. Drop arbitrary line, word, and link-count budgets and the fixed stage roster. |
| `InstructionContractTests.test_focused_outline_and_draft_load_authoritative_contracts` | 2/0/0/1/1 | 4 | Remove: forces links onto exact command lines; cannot demonstrate that an agent loads or follows them. |
| `InstructionContractTests.test_every_stage_owner_uses_the_shared_contract_shape` | 1/0/0/1/1 | 3 | Remove: heading order is an editorial convention, not a machine-consumed schema. |
| `InstructionContractTests.test_detailed_contracts_live_outside_the_router` | 1/0/0/0/0 | 1 | Remove: locks particular sentences to particular documents and repeats architectural prose checks. |
| `InstructionContractTests.test_lifecycle_order_and_completion_gates_are_explicit` | 2/0/0/1/0 | 3 | Remove: numbered labels and completion-phrase counts cannot establish workflow order or gating. |
| `InstructionContractTests.test_durable_artifact_ownership_is_single_and_bounded` | 2/0/0/1/0 | 3 | Remove: descriptions of artifact ownership do not show which files the workflow creates. |
| `InstructionContractTests.test_headline_runs_only_at_outline_and_critique` | 1/0/0/1/0 | 2 | Remove: exact phrases and category names do not observe headline passes. |
| `InstructionContractTests.test_outline_is_the_shared_rhetorical_contract` | 2/0/0/1/0 | 3 | Remove: cannot detect rhetorical drift; actual broken links are covered by the retained packaging check. |
| `InstructionContractTests.test_direction_changes_require_explicit_renegotiation` | 2/0/0/1/0 | 3 | Remove: presence of approval choices cannot demonstrate approval before revision. |
| `InstructionContractTests.test_slopless_adjudicates_rhetoric_sensitive_findings` | 2/0/0/1/0 | 3 | Remove: checks prose and self-labeled samples without running an adjudicator. Executable version selection already has behavioral coverage. |
| `InstructionContractTests.test_proof_and_lens_share_one_outline_state` | 2/0/0/1/0 | 3 | Remove: phrase inventory cannot demonstrate claim validation, shared state, visual approval, or evidence fidelity. |
| `InstructionContractTests.test_fresh_start_orientation_is_brief_and_scoped` | 1/0/0/1/1 | 3 | Remove: four phrases do not establish when orientation appears or its actual length. |
| `InstructionContractTests.test_roughdraft_contract_is_watched_and_recoverable` | 2/0/0/0/0 | 2 | Remove: wrapper behavior has stronger script coverage; remaining agent-approval claims need session evaluations. |
| `InstructionContractTests.test_fragile_transitions_have_observable_contracts` | 2/0/0/0/0 | 2 | Remove: repeats substring checks without observing a transition. |
| `InstructionContractTests.test_guided_1_2_trace_replays_observable_state_and_writes` | 2/0/0/0/0 | 2 | Remove: the test invents state, writes its own artifacts, and records tool names without invoking them. It is not end-to-end coverage. |
| `InstructionContractTests.test_slopless_contract_preserves_transparency_and_failure_gate` | 2/0/0/0/1 | 3 | Remove: reporting phrases cannot establish reporting behavior or blocking; executable preflight failure remains covered. |
| `InstructionContractTests.test_premise_divergence_and_existing_product_contracts_survive` | 2/0/0/0/0 | 2 | Remove: repeats a broad, mixed inventory of editorial phrases. |
| `InstructionContractTests.test_retired_map_and_invocation_contracts` | 2/2/1/2/1 | 8 | Narrow: protect the actual explicit-invocation metadata declaration; remove legacy-map wording and prose assertions. |

The two retained checks are `PackagingTests.test_packaged_instruction_links_resolve` (2/2/2/2/2 = 10) and `PackagingTests.test_agent_metadata_declares_explicit_invocation` (2/2/1/2/2 = 9). The latter deliberately lints the canonical YAML block declaration with the standard library. It rejects missing, commented-out, duplicate, or nested flag declarations, but does not validate general YAML syntax or prove runtime invocation behavior. Equivalent YAML serialization may require updating that small check; a new YAML dependency is not justified solely for this flag.

### Unused fixtures

| Fixture | Decision |
| --- | --- |
| `tests/fixtures/guided_workflow_1_2.json` | Remove with its only consumer, the synthetic replay. The test manufactures the expected state instead of observing a shipped workflow. |
| `tests/fixtures/rhetorical_hygiene_cases.json` | Remove with its only consumer, the category/string check. Samples alone lack an executing adjudicator and approved-outline context; they never establish preserve/revise decisions. |

## Outcome and verification

Two independent subagents audited all 43 baseline tests: one reviewed the 17 helper tests against their implementations, and one reviewed the 26 instruction tests and both fixtures. Their findings informed the per-test decisions above.

The suite now contains 19 tests: all 17 helper tests, with incidental assertions and overstated names narrowed, plus two focused packaging checks. Twenty-four tests and two unused fixtures were removed. Product instructions and production scripts are unchanged.

Run the retained suite with `python3 -m unittest discover -s tests -v`. It uses only the Python standard library and local executable stubs; it does not require live Slopless, Roughdraft, network access, or a browser.

Validation: all 43 baseline tests passed before editing; all 19 retained tests pass afterward. Skill validation and `git diff --check` pass. The reviewers also tested disposable copies: the retained tests catch draft overwrite, acceptance of the wrong Slopless version, false completion after a review timeout, a broken link in a reference file, and an invocation flag that is true, commented out, or misplaced under a nested key. Harmless prose and heading edits still pass the packaging checks. The temporary mutation copies were removed; production files were not altered.

These tests do not replace representative agent-session evaluations of approval, instruction adherence, premise diversity, rhetorical quality, or actual editor interaction. Those requirements remain in the skill documents. No new evaluation framework is introduced in this cleanup.
