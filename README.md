# Does Female Orgasm Select for Prosocial Men? — Reproducibility Materials

This repository contains **source-labeled aggregate inputs, Python code, independently reconstructed statistics, and three figures** for a methodological review of Alexander and Caitlin's Date Psychology article [“The Orgasm Gap, Prosocial Males, and Evolution” (August 8, 2024)](https://datepsychology.com/the-orgasm-gap-prosocial-males-and-evolution/).

**Scope and essential limitation:** These are **reconstructions from rounded published results**, not an independent replication of Date Psychology's original analysis. No participant-level observations, original survey responses, or original analysis scripts are included or were used here. Where published group sizes are uncertain, calculations are explicitly conditional on stated assumptions. The separate evolutionary argument is a literature-based assessment, **not** a result computed by this package.

## Contents

| File | Purpose |
| --- | --- |
| `reproduce_orgasm_review.py` | One-command script that recalculates the aggregate statistics and regenerates all three charts. |
| `oral_sex_counts.csv` | Reconstructed 2 × 2 subgroup counts for receiving oral sex and ever reporting orgasm (section 5.1). |
| `encounter_followup_counts.csv` | Reconstructed first-encounter orgasm × five-or-more-encounters counts (section 5.3). |
| `welch_reported_inputs.csv` | Published group means/SDs/tests plus **assumed**, not verified, oral-sex subgroup sizes (section 5.2). |
| `mediation_reported_coefficients.csv` | Printed coefficients, standard errors, and z-statistics from the two mediation descriptions (section 5.5). |
| `selected_prosocial_pvalues.csv` | Four selected published p-values and effect sizes used for a limited multiplicity illustration (section 4); effect sizes are transcriptions only. |
| `dasilva_reported_r2.csv` | Five reported explained-variance figures from da Silva, Mafra & Valentova (2024 online; journal issue 2025), used in Figure 3. |
| `reconstruction_results.txt` | Example script output with computed statistics and interpretation cautions. |
| `reconstruction_results.csv` | Machine-readable computed numerical results. |
| `figure_01_oral_sex_correct_denominators.png` | Figure 1: correctly conditioned oral-sex comparison (74.5% vs 42.1%). |
| `figure_02_odds_vs_probability.png` | Figure 2: first-encounter orgasm and subsequent encounters; risk vs odds (1.90 vs 3.69). |
| `figure_03_dasilva_explained_variance.png` | Figure 3: small explained-variance values (1.0%–3.4%) from the larger Brazilian study. |
| `test_reconstruction.py` | Sanity checks for the central reconstructed counts and arithmetic. |
| `SOURCE_NOTES.md` | Provenance, decision rules, and further limitations. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Standard local Python exclusions. |

## Reproduce the calculations and figures

1. Install **Python 3.11 or newer**. From the directory containing these files, run:

   ```bash
   python -m pip install -r requirements.txt
   python reproduce_orgasm_review.py
   ```

2. To run the included verification checks:

   ```bash
   python -m unittest test_reconstruction.py -v
   ```

3. The script writes three PNGs, `reconstruction_results.txt`, and `reconstruction_results.csv` **next to the script**; files of the same name will be overwritten. Run in a working copy if preserving the checked-in originals matters. The charts are recreated from the same published values as the companion review's illustrations; fonts and raster dimensions can vary slightly by installed plotting version.

The code uses fixed inputs and no random numbers. The key reported values agree with the published numbers to rounding precision. All scripts use relative paths derived from their own location, so no local machine path needs editing.

## Methods and interpretation

**1. Corrected oral-sex denominators.** The original article states that, among **46 women reporting an orgasm**, 38 had received oral sex and 8 had not; it also reports **70 women** and a Yates-corrected chi-square of about **5.09**. The reconstructed table `[[38, 13], [8, 11]]` is consistent with these statements. The **correct** comparison is `38/51 = 74.5%` vs `8/19 = 42.1%`, not `38/46 = 82.6%` vs `8/46 = 17.4%`. The script uses `scipy.stats.chi2_contingency(..., correction=True)`, yielding χ²≈5.093 and p≈.0240. Association is **not** causation.

**2. Odds and probabilities.** The original report's **66.67%** and **35.14%** are consistent with `22/33` and `13/37` (70 women). The probability ratio is **1.897**; the odds ratio is **3.692**. These are not interchangeable and do not show that initial orgasm caused further encounters.

**3. Welch tests.** Applying ordinary two-sample Welch formulas to the published means and SDs and the **unverified assumption** that both outcome analyses used the full `n=51` and `n=19` oral-sex groups gives |t|≈**3.657**, df≈**29.09** for satisfaction, and |t|≈**4.492**, df≈**36.26** for regret. The article prints |t|≈2.16/2.19, df≈25.58/26.26. Different outcome-specific sample sizes, missing data, or other discrepancies could explain part of this; the published information does **not** establish an exact computational error. The reported `d=0.67` is also compared with pooled-SD values **conditional on the same sample-size assumption**.

**4. Mediation reporting.** The script records the printed parameters and compares each coefficient's sign with the sign of its printed z-statistic. The apparent −0.263 “indirect effect” closely resembles the **difference** between reported female and male ever-orgasm rates (0.6571−0.9205≈−0.2634). This is **a clue, not a reconstruction of the original lavaan model**. Some coefficients could legitimately recur across models because the sex-to-orgasm path may be shared. Repeated outcome-specific results remain unexplained.

**5. Multiplicity illustration.** A Bonferroni calculation across **four selected p-values only** is supplied as an example. These were **not** necessarily a preregistered family; no claim is made that this is an exhaustive or definitive correction for the study's broader testing program.

**6. Hypothetical cumulative-exposure example.** `1 − 0.6^5 ≈ 92.224%` is what the probability of *ever* experiencing at least one event becomes over five independent occasions if each occasion has a constant 40% probability. This is **hypothetical**, not a model fit to the Date Psychology data.

**7. Independent literature (Figure 3).** The plotted 1.0%–3.4% explained-variance values are **transcribed** from da Silva et al. These are neither Date Psychology survey statistics nor a new model fit. The outcome is variation in women's ratings of partner traits associated with orgasm-domain scores—not explained variation in individual-orgasm probability.

## Figure and manuscript crosswalk

- **Figure 1; review §5.1:** `figure_01_oral_sex_correct_denominators.png` ← `oral_sex_counts.csv`.
- **Figure 2; review §5.3:** `figure_02_odds_vs_probability.png` ← `encounter_followup_counts.csv`.
- **Figure 3; review independent-literature discussion:** `figure_03_dasilva_explained_variance.png` ← `dasilva_reported_r2.csv`.
- **Review §5.2:** Welch calculations and discrepancies in `reconstruction_results.txt` ← `welch_reported_inputs.csv`.
- **Review §5.5:** Printed mediation checks in `reconstruction_results.txt` ← `mediation_reported_coefficients.csv`.
- **Review multiplicity discussion:** Illustrative adjusted p-values in `reconstruction_results.txt` ← `selected_prosocial_pvalues.csv`.

## Principal sources

- Alexander & Caitlin (2024). [*The Orgasm Gap, Prosocial Males, and Evolution*](https://datepsychology.com/the-orgasm-gap-prosocial-males-and-evolution/). Date Psychology. Source for the original study's reported aggregate inputs.
- Da Silva, C. S. A., Mafra, A. L., & Valentova, J. V. (published online 2024). [*Evolutionary Role of the Female Orgasm: Insights into Mate Choice and Beyond*](https://doi.org/10.1007/s10508-024-03011-3). *Archives of Sexual Behavior*. Source for the Figure 3 input values.

Full bibliographic discussion of evolutionary mechanisms is in the companion critique. No copyrighted journal PDFs, raw third-party webpage archives, or original participant records are redistributed.

## Transparency and limitations

All numerical inputs were manually reconstructed or transcribed from the cited publications; no original authors' microdata were available in this package. These calculations test **internal consistency of published numbers**, not validity of respondents' recollections, measurement instruments, causal identification, or evolutionary hypotheses. If original data and code become publicly accessible, direct reanalysis should supersede any assumptions required here.
