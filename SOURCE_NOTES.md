# Source notes and audit trail

## Scope

This package accompanies an approximately 9,000-word methodological and evolutionary review. It deliberately separates three types of evidence:

- **Reported:** rounded summary statistics printed in Alexander and Caitlin's article or in da Silva et al.
- **Reconstructed:** 2-by-2 cell counts and elementary calculations consistent with those published values; not derived from participant-level records.
- **Hypothetical:** a cumulative-event example under a constant, independent per-encounter probability; not observed data.

No source paper's full text or source PDF is included in the repository. Data rows are limited to a small number of published numbers required to reproduce figures and arithmetic. Those numbers should be cited to their original sources, not treated as our own primary observations.

## Reconstruction decisions

### Oral sex and orgasm

Published statements permit a 70-woman 2-by-2 count table with 46 women reporting ever experiencing orgasm. The quoted 17.39% and 82.61% translate into 8 and 38 people among these 46. Combining this with n=70 and matching the reported Yates chi-square gives the 2-by-2 table used here. There may be other tables with similarly rounded summary statistics, but the reconstruction reproduces the article's reported test. Cell counts and p-value are *conditionally* reconstructable; we do not know raw questionnaire handling or participant-level missingness.

### Continued encounters

66.67% and 35.14% correspond to 22/33 and 13/37 within the original n=70 female sample. The reported odds ratio of about 3.6 is approximately 3.69 in that reconstruction. Interpret as *association*, not causation or an estimate of how strongly orgasm “causes” continuation.

### Welch-test comparisons

Published oral-sex means/SDs are taken from the original article. The *n* values for the two outcome tests are not printed transparently in the manuscript. Using 51 and 19 from the oral-sex-by-orgasm table is therefore a **what-if audit**, not evidence that the author's tests used these exact subgroup sizes. It demonstrates that the reported group summaries and tests are not reconcilable from the disclosed information under the obvious group-size assumption. A definitive diagnosis requires original analytic sample sizes and code. Magnitudes of t and Cohen's d are compared because switching group order reverses signs.

### Mediation

The article repeats the same figures for satisfaction and regret. A common sex-to-orgasm coefficient may legitimately be identical in both, and a negative beta with positive z may reflect a sign omitted in prose rather than a different underlying estimate. The script flags exactly what was printed and avoids reconstructing unknown lavaan specifications or asserting impossible models. The sex difference in percentages is on a probability scale; whether this equals a specific lavaan parameter is unknown.

### Prosociality associations and multiplicity

The published prosociality effect sizes (two approximate Cohen d values and two reported r values) are transcribed but cannot be recalculated or independently verified from the published summaries alone. The four published p values are used only for a clearly labeled illustrative Bonferroni calculation. A correction across all tests would require defining the hypothesis family first.

### Third-party study

The da Silva et al. values summarize small R² values in SEM relationships between orgasm-domain scores and ratings of partner traits. This is a cross-sectional study of committed relationships, not a replication of the Date Psychology survey. Its values serve as contextual evidence and were *not* used to calculate Date Psychology results.

## What's not reproduced

This package does **not** reproduce the original article's prosociality-or-orgasm effect sizes, its original mixed models, raw factor construction, test statistics requiring individual responses, mediation models, partner-selection inference, or evolutionary claims. Those analyses cannot be independently reproduced from the summary numbers alone. It also does not attempt to independently recalculate da Silva's SEM results, which would require the data and model syntax.

## References

- Alexander & Caitlin (2024). https://datepsychology.com/the-orgasm-gap-prosocial-males-and-evolution/
- Da Silva, Mafra & Valentova (2024/2025). https://doi.org/10.1007/s10508-024-03011-3
- Companion methodological critique: publication URL can be added to this README after the Substack post is live.
