Write-up: MATACS-TH-2026-02

1. AI vs. rules
AI is used for two things:
1. Reading messy proposal text and extracting facts into a fixed JSON format, with an exact supporting quote for each fact.
2. Writing a one-sentence plain-English reason for each position, using only validated data.

Plain code or rules handle everything else:PDF text extraction, prompt-injection scanning, validation, mandatory pass/fail checks, all scoring maths, ranking, tie-breaking and logging.

Why this line:AI is good at understanding varied human writing. It is weak at being exactly repeatable, and it can be manipulated by text inside a document. Pass/fail decisions and arithmetic must be exact and auditable, so they stay in code. The AI never decides who wins. It only reports what the document says.
2. Consistency and explainability
- Extraction runs at temperature 0 with a pinned model version, a fixed JSON schema and a versioned prompt.
- Every extracted value needs an exact quote. Code checks the quote exists in the proposal text. If not, the value is rejected and sent to a human.
- Scores come from fixed formulas on the extracted facts, so the same facts always give the same score. Ties are broken in a fixed order: higher experience score, then lower price.
- If the same proposals were ranked twice, the result would be the same. Extraction results are saved against the file hash and reused, so re-ranking does not call the AI again. A fresh re-extraction could differ slightly, so any change in extracted values is flagged.
- Reviewers see a table per proposal: criterion, extracted value, evidence quote, points and weight. Nothing is a black box.

3. Human in the loop
- Review and confirm:the reviewer confirms or corrects extracted facts when validation fails or a value is missing (for example, a missing timeline).
- Flags held for a person:possible injection text, missing mandatory information, and unclear wording such as an ambiguous licence or date range. These are never auto-ranked or auto-rejected.
- Override:the reviewer can change a status or score but must enter a reason.
- Final decision:the award is always made by a human.
- Audit log per run:user, timestamp, file hashes, criteria version, model and prompt versions, raw AI output, validated values, flags, scores, every override with its reason, and the final decision.

4. Changing criteria
- Each scoring run stores a snapshot of the criteria version used. Editing criteria creates a new version. It never silently changes old results.
- Old rankings are labelled "scored under version N" and marked outdated, and the reviewer can re-score.
- Because extracted facts are saved and scoring is code, re-scoring is cheap and needs no new AI call. The AI is only called again if a new criterion needs a fact that was never extracted.
- Weights are validated to total 100% before saving.
- Existing human overrides are shown again for confirmation after a re-score, not silently kept or dropped.

5. Risks and safeguards
| Risk | Safeguard |
| Wrong extraction | Evidence quote required and verified in code; reviewer sees evidence; low confidence goes to a human |
| Made-up facts | Prompt allows "not stated" (null); missing values score 0 and are flagged, never guessed |
| Manipulation (sample C contains instruction-like text) | Proposal text is treated as data only; a pattern scan plus the AI report suspicious text; the AI never sets scores; the proposal is flagged for a human |
| Fake or unclear licence (sample B) | Mandatory rule requires the bidder to hold the licence; "subcontractor, to be confirmed" fails |
| Bias | Scoring uses only admin criteria and fixed formulas; company names are not used in scoring |
| Unfair relative scoring | Price and timeline are relative to the eligible set; the baseline is shown in the explanation |
| Cost | One AI extraction per proposal, cached by file hash, scoring in code, no AI calls on re-rank |
| Privacy | Only the proposal text needed is sent to the model; logs are access-controlled |

Assumptions
- A missing timeline scores 0 and is flagged, not guessed.
- "Last 5 years" is hard to confirm when a bidder says "since 2020", so it is flagged for the reviewer.
- A flagged proposal still shows its score for reference but gets no rank until a human decides.
- Scoring parameters (12 installs, 25 years, 12 years) are admin-editable settings.
