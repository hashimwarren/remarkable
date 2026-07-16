# Premise Divergence and Transformation

Treat premise quality as Remarkable's highest-leverage result. Search broadly before presenting a narrow, simple choice.

## Run the five-scout premise council

When the runtime supports subagents, spawn five independent, read-only premise scouts in parallel. Do not ask the user to request delegation again. Keep all premise selection and file writes in the main thread. Tell every scout not to spawn descendants.

Give every scout the same bounded packet:

- the reader and relevant audience context;
- the reader's current belief;
- the desired movement;
- why the idea matters now;
- available evidence and explicit truth boundaries;
- any relevant project positioning; and
- instructions to read `premise.md` and this reference before generating candidates.

Do not pass another scout's candidates into its context. Independent search is the point.

Assign the ten appeals exactly once across five deliberately tense pairs:

1. **Future and stakes:** Encourage their dreams + Agitate their fears.
2. **Risk and reassurance:** Warn against the destruction of their dreams + Allay their fears.
3. **Causal responsibility:** Justify their failures + Imply they are their own worst enemy.
4. **Recognition and reversal:** Confirm their suspicions + Shock them with unusual praise for their enemies.
5. **Opposition and replacement:** Thwart their conventional wisdom + Help them throw rocks at their enemies.

Each scout must use both assigned appeals as separate search territories, test at least three fitting fascination advantages or pairs across its exploration, and generate at least three candidate governing ideas. It returns only its strongest two candidates. Do not force one winner per assigned appeal when both strongest candidates honestly emerge from the same territory.

Require this compact return shape for each candidate:

- **Premise:** the single governing claim;
- **Belief shift:** what the reader must stop, start, or change believing;
- **Causal logic:** the explanation that makes the premise govern a whole article;
- **Appeal:** the primary assigned appeal;
- **Fascination:** the advantage or archetype and underlying pair;
- **Truth boundary:** the strongest responsible version of the claim and what would overstate it; and
- **Support fit:** what supplied or obtainable evidence could support it.

Wait for all five scouts when possible. Pool all returned candidates and ignore the scouts' relative confidence when selecting finalists. The main agent is the editor-in-chief.

### Degrade gracefully

If the runtime cannot spawn subagents, has fewer than five available worker slots, or a scout fails, continue in the main thread. Privately simulate the same five appeal territories, generate 12–20 candidates, and apply the same selection process below. Briefly disclose that the premise search ran in one context. Never claim that scouts ran when they did not.

For `Go wider`, use a fresh council when capacity permits. Give it the rejected candidates' fingerprints as negative territory, not as examples to imitate. For `[letter], but bolder`, use up to three scouts when capacity permits, all preserving the selected claim, appeal, fascination posture, and truth boundary while testing different intensification moves. The main agent selects the strongest responsible revision.

## Generate for divergence

Keep the reader, desired movement, and why-now context fixed. Privately generate 12–20 candidate governing ideas that vary the causal explanation, mistaken assumption, consequence, and action—not merely the wording.

Identify the obvious/default cluster and discard it. Fingerprint surviving candidates by:

- core claim;
- causal explanation;
- reader's mistaken assumption;
- primary consequence;
- desired action;
- appeal; and
- fascination posture.

Before presenting finalists, compare A vs. B, A vs. C, and B vs. C. Replace a candidate when substantially the same article body or evidence could support both members of a pair, or when believing either would lead to the same reader decision. Select for both quality and distance: truth, specificity, surprise, consequence, supportability, generative power, and difference from the other finalists.

Choose the appeal and fascination posture after establishing genuinely different governing ideas. A different emotional wrapper does not make the same claim a different premise.

## Select the three finalists

The main agent evaluates the entire candidate pool. Score candidates privately for truth, specificity, surprise, consequence, supportability, generative power across a full article, and distance from the other finalists. Reject a candidate that is interesting only because of its headline, emotional temperature, or fascination label.

Do not select one candidate from each scout as a fairness exercise. Select the strongest portfolio of three. Prefer different core claims and causal models over superficial coverage of more appeals.

Then run the pairwise test for A vs. B, A vs. C, and B vs. C. Replace either member of a pair when substantially the same body, evidence, or reader decision could support both. The final three should lead to meaningfully different articles even if all headlines are removed.

## Offer refinement controls

After A, B, and C, allow the user to:

- choose one;
- say `Go wider` to reject the explored territory and receive three new premise clusters;
- say `[letter], but bolder` to intensify that premise; or
- combine two options, after which Remarkable synthesizes one premise and confirms it.

For `Go wider`, do not paraphrase rejected candidates. Avoid their core claims, causal explanations, and consequences in the next round.

## Make a premise bolder

Preserve the governing claim, selected appeal, fascination posture, and truth boundary by default. Intensify contrast, stakes, consequence, specificity, or the required reader decision through the selected fascination trigger. If a meaningful increase requires changing the claim or posture, explain that and offer alternatives rather than silently switching.

Use the fascination trigger as the control:

- **Innovation:** make the new possibility or category break more consequential; avoid unsupported revolution language.
- **Passion:** bring emotional or relational stakes closer; avoid melodrama.
- **Power:** make the claim and decision more decisive; avoid aggression and false certainty.
- **Prestige:** raise the standard and clarify what excellence demands; avoid status theater.
- **Trust:** express calmer, more earned conviction; avoid bland reassurance.
- **Mystique:** reveal a deeper hidden mechanism or tension; avoid vagueness and clickbait.
- **Alert:** make the relevant risk, detail, or failure mode concrete; avoid fearmongering.

Use the appeal to decide where the additional persuasive pressure lands:

- **Encourage dreams:** make the desired future more specific and meaningful.
- **Warn against destroying dreams:** clarify the credible obstacle and consequence.
- **Justify failures:** sharpen the misdiagnosed cause without removing agency.
- **Their own worst enemy:** expose the consequential behavior or assumption without shaming.
- **Allay fears:** make reassurance more credible, concrete, and actionable.
- **Agitate fears:** make a supported danger vivid without inflating it.
- **Confirm suspicions:** say plainly what the reader senses and substantiate it.
- **Thwart conventional wisdom:** challenge a deeper assumption and supply a stronger replacement.
- **Throw rocks at enemies:** name the obstructing force without scapegoating.
- **Praise enemies:** reveal a more surprising but defensible lesson from the apparent opponent.

The appeal determines where persuasive pressure lands. Fascination determines how that pressure becomes difficult to ignore. The premise is the governing claim produced by both.
