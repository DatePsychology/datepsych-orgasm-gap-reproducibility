#!/usr/bin/env python3
"""Reproduce aggregate-statistics audits and 3 figures for a methodological review.

Input: hand-transcribed/reconstructed published summary statistics (CSV files).
NOT a reanalysis of participant-level data. Requires numpy, scipy and matplotlib.
Run from any directory: python reproduce_orgasm_review.py

This code writes PNGs, reconstruction_results.txt, and reconstruction_results.csv
next to the script and can overwrite files with those names in that folder.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, norm

ROOT = Path(__file__).resolve().parent
NAVY = "#172d40"
TEAL = "#68949c"
PALE = "#a5b7be"
LIGHT = "#c2d0d3"
BG = "#f8f5ef"
MUTED = "#6d7e88"
GRID = "#dbe2e6"


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def fnum(x: str) -> float:
    return float(x)


def setup_figure(width: float = 12, height: float = 6.6):
    fig = plt.figure(figsize=(width, height), facecolor=BG)
    return fig


def axis_style(ax, ymax: int = 100):
    ax.set_facecolor(BG)
    ax.set_ylim(0, ymax)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], color=MUTED, fontsize=14)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=12)


def save_figure(fig, filename: str):
    fig.savefig(ROOT / filename, dpi=180, facecolor=BG)
    plt.close(fig)


def fig_01_oral(rows):
    values = [float(rows[0]["ever_orgasm_yes"]) / (float(rows[0]["ever_orgasm_yes"]) + float(rows[0]["ever_orgasm_no"])) * 100,
              float(rows[1]["ever_orgasm_yes"]) / (float(rows[1]["ever_orgasm_yes"]) + float(rows[1]["ever_orgasm_no"])) * 100]
    fig = setup_figure()
    fig.text(0.04, 0.94, "Oral sex and orgasm: the corrected comparison", fontsize=23,
             color=NAVY, weight="bold", ha="left", va="top")
    fig.text(0.04, 0.85, "Observed orgasm rates within each oral-sex group; n = 70 women", fontsize=13,
             color=MUTED, ha="left")
    ax = fig.add_axes([0.10, 0.20, 0.84, 0.54])
    axis_style(ax)
    x = [0, 1]
    bars = ax.bar(x, values, color=[TEAL, PALE], width=0.53)
    ax.set_xlim(-0.55, 1.55)
    ax.set_xticks(x)
    ax.set_xticklabels(["Reported receiving oral sex", "Did not report receiving oral sex"], fontsize=12, color=MUTED)
    for i, bar in enumerate(bars):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3, f"{values[i]:.1f}%",
                ha="center", va="bottom", fontsize=19, color=NAVY, weight="bold")
        n_yes = int(rows[i]["ever_orgasm_yes"])
        n = n_yes + int(rows[i]["ever_orgasm_no"])
        ax.text(bar.get_x()+bar.get_width()/2, 4, f"{n_yes} of {n}",
                ha="center", fontsize=13, color=("white" if i == 0 else NAVY), weight="bold")
    fig.text(0.04, 0.055,
             "The article's 82.6% and 17.4% instead divide the 46 women who orgasmed by oral-sex status.",
             fontsize=11.2, color=MUTED)
    save_figure(fig, "figure_01_oral_sex_correct_denominators.png")


def fig_02_followup(rows, risk_ratio, odds_ratio):
    values = [int(r["five_or_more_encounters_yes"]) / (int(r["five_or_more_encounters_yes"]) + int(r["five_or_more_encounters_no"])) * 100
              for r in rows]
    fig = setup_figure()
    fig.text(0.04, 0.94, "Initial orgasm and five or more encounters", fontsize=23,
             color=NAVY, weight="bold", ha="left", va="top")
    fig.text(0.04, 0.85, "Observed share reporting at least five encounters with the same partner; n = 70 women", fontsize=12,
             color=MUTED, ha="left")
    ax = fig.add_axes([0.095, 0.22, 0.66, 0.49])
    axis_style(ax)
    bars = ax.bar([0, 1], values, width=0.56, color=[TEAL, PALE])
    ax.set_xlim(-0.5, 1.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Orgasm on first encounter", "No orgasm on first encounter"], fontsize=11, color=MUTED)
    for i, bar in enumerate(bars):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2,
                f"{values[i]:.1f}%", ha="center", va="bottom", fontsize=17, color=NAVY, weight="bold")
        yes = int(rows[i]["five_or_more_encounters_yes"])
        n = yes + int(rows[i]["five_or_more_encounters_no"])
        ax.text(bar.get_x()+bar.get_width()/2, 5, f"{yes} of {n}", ha="center", fontsize=12,
                color=("white" if i == 0 else NAVY), weight="bold")
    fig.text(0.84, 0.57, f"{risk_ratio:.2f}×", color=NAVY, fontsize=30, weight="bold", ha="center")
    fig.text(0.84, 0.52, "relative probability", color=MUTED, fontsize=11, ha="center")
    fig.text(0.84, 0.35, f"{odds_ratio:.2f}×", color=NAVY, fontsize=30, weight="bold", ha="center")
    fig.text(0.84, 0.30, "odds ratio", color=MUTED, fontsize=11, ha="center")
    fig.text(0.04, 0.05,
             "An odds ratio is not a probability ratio; these are observational associations.",
             fontsize=11.5, color=MUTED)
    save_figure(fig, "figure_02_odds_vs_probability.png")


def fig_03_dasilva(rows):
    values = [float(r["r_squared_percent"]) for r in rows]
    labels = [r["partner_trait"] for r in rows]
    fig = setup_figure()
    fig.text(0.04, 0.94, "Statistically detectable associations can still be small", fontsize=22,
             color=NAVY, weight="bold", ha="left", va="top")
    fig.text(0.04, 0.85,
             "Da Silva, Mafra & Valentova (2024/2025); 939 Brazilian women in committed relationships",
             fontsize=12, color=MUTED, ha="left")
    ax = fig.add_axes([0.33, 0.18, 0.59, 0.58])
    ax.set_facecolor(BG)
    positions = np.arange(len(labels))
    bars = ax.barh(positions, values, color=[TEAL, "#7fa6ac", "#92b0b5", "#a5bdc1", LIGHT], height=0.58)
    ax.set_yticks(positions, labels, fontsize=12, color=NAVY)
    ax.invert_yaxis()
    ax.set_xlim(0, 4.0)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(["0%", "1%", "2%", "3%", "4%"], fontsize=12, color=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0, pad=11)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for b, val in zip(bars, values):
        ax.text(val+0.075, b.get_y()+b.get_height()/2, f"{val:.1f}%",
                va="center", ha="left", fontsize=14, weight="bold", color=NAVY)
    fig.text(0.04, 0.06,
             "R²: variance in partner-trait ratings associated with orgasm-domain score; not a causal effect.",
             fontsize=11, color=MUTED)
    save_figure(fig, "figure_03_dasilva_explained_variance.png")


def fmt(x: float, n: int = 3) -> str:
    return f"{x:.{n}f}"


def main():
    oral = read_csv("oral_sex_counts.csv")
    follow = read_csv("encounter_followup_counts.csv")
    welch = read_csv("welch_reported_inputs.csv")
    r2 = read_csv("dasilva_reported_r2.csv")
    prosocial = read_csv("selected_prosocial_pvalues.csv")
    mediation = read_csv("mediation_reported_coefficients.csv")

    assert len(oral) == 2 and oral[0]["reported_receipt_of_oral_sex"] == "Yes"
    a = int(oral[0]["ever_orgasm_yes"])
    b = int(oral[0]["ever_orgasm_no"])
    c = int(oral[1]["ever_orgasm_yes"])
    d = int(oral[1]["ever_orgasm_no"])
    assert (a, b, c, d) == (38, 13, 8, 11), "Check transcript before interpreting"
    tab = np.array([[a, b], [c, d]])
    chi2, p_yates, _, _ = chi2_contingency(tab, correction=True)
    p_oral_yes = a / (a+b)
    p_oral_no = c / (c+d)
    rr_oral = p_oral_yes / p_oral_no
    rd_oral = p_oral_yes-p_oral_no
    assert sum(tab.flatten()) == 70 and a+c == 46
    assert abs(chi2 - 5.0934681653) < 1e-8
    assert abs(p_yates - 0.0240161165) < 1e-8

    e = int(follow[0]["five_or_more_encounters_yes"])
    f = int(follow[0]["five_or_more_encounters_no"])
    g = int(follow[1]["five_or_more_encounters_yes"])
    h = int(follow[1]["five_or_more_encounters_no"])
    assert (e, f, g, h) == (22, 11, 13, 24)
    risk1, risk0 = e/(e+f), g/(g+h)
    risk_ratio = risk1/risk0
    odds_ratio = (e*h)/(f*g)
    assert abs(risk_ratio-1.8974358974) < 1e-8
    assert abs(odds_ratio-3.6923076923) < 1e-8

    logs = []
    audit_rows = []
    def add(name: str, value: float, units: str = "", note: str = ""):
        logs.append(f"{name}: {value:.6f}{(' '+units) if units else ''}{(' | '+note) if note else ''}")
        audit_rows.append({"calculation": name, "value": f"{value:.10g}", "unit": units, "note": note})

    logs.append("AGGREGATE-STATISTICS RECONSTRUCTION — NOT A PARTICIPANT-LEVEL REPLICATION")
    logs.append("Inputs: published/rounded statistics transcribed or logically reconstructed as documented in CSV files")
    logs.append("")
    logs.append("ORAL SEX × EVER ORGASM (reconstructed n=70; rows receipt yes/no, columns orgasm yes/no)")
    logs.append(f"Contingency table: [[{a},{b}],[{c},{d}]]")
    add("oral_sex_orgasm_rate_yes", p_oral_yes*100, "percent")
    add("oral_sex_orgasm_rate_no", p_oral_no*100, "percent")
    add("oral_sex_relative_risk", rr_oral, "ratio")
    add("oral_sex_risk_difference", rd_oral*100, "percentage_points")
    add("reported_wrong_conditioning_yes_div_46", a/(a+c)*100, "percent", "NOT P(orgasm | oral sex)")
    add("reported_wrong_conditioning_no_div_46", c/(a+c)*100, "percent", "NOT P(orgasm | no oral sex)")
    add("oral_sex_chi2_Yates", chi2)
    add("oral_sex_chi2_Yates_p", p_yates, "p")
    logs.append("")
    logs.append("FIRST-ENCOUNTER ORGASM × >=5 ENCOUNTERS (reconstructed n=70)")
    logs.append(f"Contingency table: [[{e},{f}],[{g},{h}]]")
    add("five_encounters_probability_first_orgasm", risk1*100, "percent")
    add("five_encounters_probability_no_first_orgasm", risk0*100, "percent")
    add("five_encounters_risk_ratio", risk_ratio, "ratio")
    add("five_encounters_odds_ratio", odds_ratio, "ratio")
    logs.append("")
    logs.append("WELCH T RECONSTRUCTIONS — CONDITIONAL ON UNVERIFIED 51-vs-19 SUBGROUP SIZES")
    logs.append("Sign of reported t/d may depend on comparison order; magnitudes used below.")
    for row in welch:
        label = row["outcome"].lower().replace(" ", "_")
        n1, n2 = int(row["assumed_n_oral_yes"]), int(row["assumed_n_oral_no"])
        m1, s1 = float(row["mean_oral_yes"]), float(row["sd_oral_yes"])
        m2, s2 = float(row["mean_oral_no"]), float(row["sd_oral_no"])
        v1, v2 = (s1*s1)/n1, (s2*s2)/n2
        t_value = (m1-m2)/math.sqrt(v1+v2)
        df = (v1+v2)**2 / (v1*v1/(n1-1) + v2*v2/(n2-1))
        pooled_sd = math.sqrt(((n1-1)*s1*s1+(n2-1)*s2*s2)/(n1+n2-2))
        cohen_d = (m1-m2)/pooled_sd
        add(label+"_recalculated_abs_Welch_t", abs(t_value), "abs_t", "rounded reported means/SDs; assumed n=51/19")
        add(label+"_recalculated_Welch_df", df, "df", "assumed n=51/19")
        add(label+"_recalculated_abs_pooled_Cohens_d", abs(cohen_d), "abs_d", "assumed n=51/19")
        add(label+"_article_reported_abs_t", abs(float(row["reported_t"])), "abs_t")
        add(label+"_article_reported_Welch_df", float(row["reported_df"]), "df")
        add(label+"_article_reported_abs_d", abs(float(row["reported_cohens_d"])), "abs_d")
    logs.append("")
    logs.append("MEDIATION PRINTED-COEFFICIENT CHECKS — DO NOT INFER LAVAAN MODEL SPECIFICATION")
    for rec in mediation:
        coef, se, reported = float(rec["coefficient"]),float(rec["se"]),float(rec["reported_z"])
        z_arith = coef/se
        logs.append(f"{rec['outcome']}: {rec['article_label']}: beta={coef}, SE={se}, reported z={reported}, beta/SE={z_arith:.3f}; "+
                    ("OPPOSITE SIGNS" if z_arith*reported<0 else "sign consistent"))
    add("female_minus_male_ever_orgasm_prevalence", (0.6571-0.9205), "probability_difference", "rounded percentages 65.71% and 92.05%")
    logs.append("A common sex-to-orgasm path may legitimately repeat; repeated outcome-specific paths still need clarification.")
    logs.append("")
    logs.append("BONFERRONI ILLUSTRATION — FOUR SELECTED TESTS ONLY; NOT PRE-REGISTERED FAMILY")
    for rec in prosocial:
        p=float(rec["reported_p"])
        label=rec["comparison"].lower().replace(" ", "_")
        add("bonferroni_"+label, min(p*len(prosocial),1.0), "adjusted_p", "illustrative 4-test set")
    logs.append("")
    logs.append("CONSTANT PER-ENCOUNTER ORGASM PROBABILITY — HYPOTHETICAL EXPOSURE EXAMPLE")
    add("probability_ever_orgasm_5_encounters_if_p40_each_independent", (1-(1-0.4)**5)*100, "percent", "hypothetical, not sample data")
    logs.append("")
    logs.append("DA SILVA ET AL. REPORTED R^2 (not independent recalculations)")
    for rec in r2:
        add("dasilva_r2_"+rec["partner_trait"].lower().replace(" ", "_"), float(rec["r_squared_percent"]), "percent")

    fig_01_oral(oral)
    fig_02_followup(follow, risk_ratio, odds_ratio)
    fig_03_dasilva(r2)

    (ROOT/"reconstruction_results.txt").write_text("\n".join(logs)+"\n", encoding="utf-8")
    with (ROOT/"reconstruction_results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer=csv.DictWriter(fh, fieldnames=["calculation", "value", "unit", "note"])
        writer.writeheader(); writer.writerows(audit_rows)
    print("\n".join(logs))
    print("\nWrote 3 figures, reconstruction_results.txt, reconstruction_results.csv")


if __name__ == "__main__":
    main()
