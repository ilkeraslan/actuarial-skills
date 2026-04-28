---
name: loss-reserve-analysis
description: "Perform a loss reserve analysis on P&C insurance loss development triangles in a European / Swiss regulatory context. Use this skill whenever the user uploads loss triangles (paid or incurred), Solvency II QRT S.19.01 data, FINMA reserve templates, or asks about reserve adequacy, IBNR estimation, best estimate of claims provisions, loss development analysis, or ultimate loss projections. Also trigger when the user mentions chain ladder, Bornhuetter-Ferguson, Cape Cod, Mack method, loss development factors, tail factors, claims provisions, or actuarial reserving methods. This skill reads triangles from Excel or CSV, runs multiple standard actuarial methods, diagnoses unusual patterns, and produces a formatted Excel report with exhibits. Even if the user just says 'check my reserves', 'run development on this triangle', 'estimate the best estimate', or 'analyze my loss reserves', use this skill."
---

# Loss Reserve Analysis (European / Swiss Edition)

## Purpose

Analyze P&C insurance loss development triangles using standard actuarial reserving methods, flag anomalies, and produce a professional loss reserve analysis report in Excel. This skill is adapted for European practice — Solvency II Article 77 and Article 82 (Best Estimate and data quality), Swiss Solvency Test (SST), and FINMA reserve reporting contexts.

Methods reference Friedland's *Estimating Unpaid Claims Using Basic Techniques* and Wüthrich & Merz, *Stochastic Claims Reserving Methods in Insurance* (Wiley, 2008). Where US ASOPs are cited, they are educational only — Swiss-licensed work follows SAV professional guidance and FINMA Circular 2008/44 (Solvency II equivalent: EIOPA Guidelines on Valuation of Technical Provisions).

## When to Use

- User uploads a loss triangle (Excel or CSV) and wants reserve analysis
- User asks about IBNR, claims provisions, best estimate, or ultimate loss estimates
- User mentions chain ladder, Bornhuetter-Ferguson, Cape Cod, or Mack
- User has Solvency II QRT S.19.01 data, FINMA reserve templates, or treaty reinsurance triangles (gross/ceded/net)

## Workflow

### Step 1: Identify and Parse the Triangle

1. Check `/mnt/user-data/uploads/` for uploaded files.
2. Read the file using the `scripts/parse_triangle.py` helper.
3. If the data format is ambiguous, ask the user:
   - Is this **paid** losses, **incurred** losses, or both? Are these **gross**, **ceded**, or **net** of reinsurance?
   - What is the **evaluation date** (Stichtag)?
   - Are the development periods in **months**, **quarters**, or **years**?
   - Is there an **earned premium** column or sheet for BF/Cape Cod methods? Note whether premiums are on-level or as-collected.
   - Is the data discounted or undiscounted? (For Solvency II Best Estimate, undiscounted nominal cash flows are typically required first; discounting is applied separately using the EIOPA risk-free rate term structure.)

Per Solvency II Article 82 and EIOPA Guidelines on Valuation of Technical Provisions (Sections on data quality), assess whether data is appropriate, complete, and accurate. Ask the user about known data issues such as changes in claim coding, coverage triggers, reopened claims, large-loss treatment, or reinsurance restructuring that may affect triangle integrity. See Friedland Ch. 1–4 and Wüthrich & Merz Ch. 1 for background on the claims process and triangle data.

**Supported formats:**
- Standard triangle layout: rows = accident years/quarters, columns = development periods
- Columnar layout: columns for accident period, development period, and loss amount
- Solvency II QRT S.19.01 format (rolling triangles in Solvency II structure)
- Transaction-level claim data (auto-aggregated to a triangle)

### Step 2: Run the Analysis

Execute the main analysis script:

```bash
python scripts/reserve_analysis.py \
  --input <path_to_triangle_file> \
  --sheet <sheet_name_if_excel> \
  --type <paid|incurred|both> \
  --basis <gross|ceded|net> \
  --dev-periods <months|quarters|years> \
  --premium <path_or_value_if_available> \
  --output /home/claude/reserve_report.xlsx
```

The script runs these methods:

1. **Chain Ladder (Volume-Weighted)** — Standard development method using volume-weighted average factors. Friedland Ch. 7; Wüthrich & Merz Ch. 3 (Mack's distribution-free chain ladder framework).
2. **Chain Ladder (Simple Average)** — Arithmetic mean of age-to-age factors for comparison.
3. **Mack (1993) Method** — Distribution-free chain ladder with analytical mean square error of prediction (MSEP). Provides reserve standard error per accident year and in total. Required for any output that supports SST or Solvency II Best Estimate uncertainty assessment. Reference: Mack, T. (1993), *ASTIN Bulletin* 23(2); Wüthrich & Merz Ch. 3.
4. **Bornhuetter-Ferguson** — Blends an a priori expected loss ratio with the chain ladder pattern. Friedland Ch. 9; Bornhuetter & Ferguson, PCAS 1972; Wüthrich & Merz Ch. 2.
5. **Cape Cod (Stanard-Bühlmann)** — Derives the expected loss ratio from the data itself. Friedland Ch. 10; Stanard, PCAS 1985. Bühlmann's contribution refers to the credibility-theoretic interpretation.
6. **Expected Loss Ratio (ELR)** — Pure a priori method, used when development data has very limited credibility (early accident periods or new lines).

### Step 3: Review Diagnostics

The script produces diagnostic exhibits. Review these and flag findings to the user:

- **Calendar year (diagonal) test**: Checks whether development along diagonals is consistent. Large swings may indicate reserve strengthening/weakening, claim handling changes, or operational shifts.
- **Mack's three assumption tests**: Independence of accident years, variance proportionality, and absence of calendar-year effects. If any are violated, the chain ladder MSEP is unreliable and bootstrapping or a GLM approach should be considered. (Wüthrich & Merz Ch. 3.)
- **High/low factor analysis**: Flags individual age-to-age factors that are outliers (>2 standard deviations from the column mean). With only 4–6 observations per development column on most triangles, treat 2σ flags as "review this", not "exclude this".
- **Tail factor sensitivity**: Shows how ultimates and IBNR change under ±10% and ±25% tail factor variations. For long-tail Casualty, also report sensitivity at ±50% — exponential-decay tails materially under-estimate long-tail liabilities.
- **Incurred-vs-paid gap** (if both triangles provided): Large divergence at later maturities may signal case reserve adequacy issues — relevant to the **Berquist-Sherman** correction (planned extension).
- **Standardized residuals**: Plot of standardized chain-ladder residuals against accident period, development period, and calendar period. Patterns indicate model inadequacy.

These diagnostics support the EIOPA "appropriateness of methods" requirement (Guidelines on Valuation of Technical Provisions, Guideline 56 onward) and the SST framework's requirement that the actuary justify method selection.

### Step 4: Interpret Results and Present

After running the analysis:

1. Copy the output Excel to `/mnt/user-data/outputs/`.
2. Present the file to the user.
3. Provide a **narrative summary** that includes:
   - The range of indicated ultimates across methods, with the Mack standard error attached to the chain ladder estimate.
   - Whether carried reserves appear adequate, deficient, or redundant relative to the chain ladder indication.
   - Which accident years show the most development volatility.
   - Any red flags from the diagnostics (in particular: violations of Mack's assumptions, large calendar-year effects, paid-vs-incurred divergence).
   - Caveats about data limitations and the quick-check nature of the analysis.
   - For Solvency II / SST contexts: explicitly note whether the output is on a **nominal undiscounted** basis (default) and that discounting and risk margin / market value margin are *not* included.

**Important tone guidance**: This is a quick check, not a Best Estimate calculation in the regulatory sense. Always caveat:
- The analysis relies on standard methods and does not incorporate claim-level information, large-loss treatment, ENID (Events Not In Data) loadings, or expert judgment.
- Tail factor selection is mechanical and should be reviewed by a credentialed actuary.
- Results should be cross-referenced with operational knowledge — claims handling changes, coverage shifts, legal environment, reinsurance program changes.
- **This does not constitute a Best Estimate of Claims Provisions under Solvency II Article 77, an SST-compliant reserve calculation, or a Responsible Actuary opinion under FINMA Circular 2008/44.** A credentialed actuary (SAV / DAV / IFoA / equivalent) should review results, apply professional judgment to factor selections, and consider regulatory requirements before relying on these estimates.

### Step 5: Interactive Follow-Up

After presenting results, offer the user options to:
- Adjust tail factors manually or apply Sherman's inverse power curve as an alternative to exponential decay.
- Exclude specific accident periods or development periods from the factor selection.
- Change the weighting scheme (volume-weighted, simple average, latest *N* years, exclusion of high/low).
- Run sensitivity scenarios on the a priori loss ratio (BF/Cape Cod).
- Compare against a benchmark loss ratio or a market loss ratio.
- Apply EIOPA risk-free rate term structure to discount cash flows (separate step; requires a payment pattern derived from paid triangle plus assumed remaining payment profile).

When adjusting selections, note that EIOPA Guidelines on Valuation of Technical Provisions emphasize that changes in environment (legal, social, operational) may invalidate historical patterns. Document any judgmental adjustments transparently.

## Key Actuarial Concepts (Reference)

Read `references/methods.md` for detailed formulas and implementation notes on each method during development or debugging. The references file should be expanded to cover Mack's MSEP formula in full and the Wüthrich & Merz notation conventions used by Continental European actuaries.

## Error Handling

- If the triangle has fewer than 3 accident periods, warn that credibility is very limited. In such cases, BF or pure ELR with an externally-derived expected loss ratio is more defensible than chain ladder.
- If any age-to-age factors are < 1.0 (negative development), flag explicitly. Negative development can be legitimate (subrogation, salvage, reopened claims with favorable settlement) but warrants explanation. Do not silently floor at 1.0.
- If the triangle is not square (jagged), handle gracefully by computing factors only where data exists.
- If earned premium is not provided, skip BF and Cape Cod methods and note this in the output.
- If the user provides ceded triangles, run the analysis on a gross basis as well and report the ceded reserve as the difference; flag any anomalies in the cession pattern.

## Notes on Adaptation from the Original Skill

This skill is adapted from [`kalta-ai/actuarial-skills`](https://github.com/kalta-ai/actuarial-skills). Key differences from the original (US-focused) version:

- ASOP references reframed as educational; Swiss / EIOPA / Solvency II framing added as the primary regulatory context.
- Wüthrich & Merz added as a primary reference alongside Friedland.
- Mack (1993) method added to provide an analytical reserve standard error — required for any uncertainty reporting under SST or Solvency II.
- Quarterly accident periods supported (relevant for Swiss and EU monthly/quarterly close cycles).
- Gross / ceded / net basis explicitly tracked, given the importance of treaty reinsurance in European P&C portfolios.
- Sherman inverse power tail option flagged as alternative to exponential decay.
- Output explicitly framed as nominal undiscounted, with discounting and risk margin called out as separate steps.
