---
name: loss-reserve-analysis
description: "Perform a loss reserve analysis on P&C insurance loss development triangles. Use this skill whenever the user uploads loss triangles (paid or incurred), Schedule P data, or asks about reserve adequacy, reserve sufficiency, IBNR estimation, loss development analysis, loss reserve review, or ultimate loss projections. Also trigger when the user mentions chain ladder, Bornhuetter-Ferguson, Cape Cod, loss development factors, tail factors, or actuarial reserving methods. This skill reads triangles from Excel or CSV, runs multiple standard actuarial methods, diagnoses unusual patterns, and produces a formatted Excel report with exhibits. Even if the user just says 'check my reserves', 'run development on this triangle', or 'analyze my loss reserves', use this skill."
---

# Loss Reserve Analysis

## Purpose

Analyze P&C insurance loss development triangles using standard actuarial reserving methods, flag anomalies, and produce a professional loss reserve analysis report in Excel. This skill applies standard methods described in Friedland's *Estimating Unpaid Claims Using Basic Techniques* and references relevant Actuarial Standards of Practice (ASOPs) for educational context.

## When to Use

- User uploads a loss triangle (Excel or CSV) and wants reserve analysis
- User asks about IBNR, reserve adequacy, or ultimate loss estimates
- User mentions chain ladder, BF, or loss development
- User has Schedule P or similar statutory data

## Workflow

### Step 1: Identify and Parse the Triangle

1. Check `/mnt/user-data/uploads/` for uploaded files
2. Read the file using the `scripts/parse_triangle.py` helper
3. If the data format is ambiguous, ask the user:
   - Is this **paid** losses, **incurred** losses, or both?
   - What is the **evaluation date**?
   - Are the development periods in **months** or **years**?
   - Is there an **earned premium** column or sheet for BF/Cape Cod methods?

Per ASOP No. 23 (Data Quality), Section 3.2 (Selection of Data), consider whether the data is appropriate for the intended analysis. Ask the user about known data issues such as changes in claim coding, coverage triggers, or reopened claims that may affect triangle integrity. See Friedland Ch. 1–4 for background on the claims process, data types, and meeting with management to understand context.

**Supported formats:**
- Standard triangle layout: rows = accident years/quarters, columns = development periods
- Columnar layout: columns for accident period, development period, and loss amount
- Transaction-level data: claim-level records with accident_date, evaluation_date, and loss amounts — automatically aggregated into a triangle
- Schedule P format (will need manual identification of the relevant section)

### Step 2: Run the Analysis

Execute the main analysis script:

```bash
python scripts/reserve_analysis.py \
  --input <path_to_triangle_file> \
  --sheet <sheet_name_if_excel> \
  --type <paid|incurred|both> \
  --dev-periods <months|years> \
  --premium <path_or_value_if_available> \
  --output /home/claude/reserve_report.xlsx
```

The script runs these methods:

1. **Chain Ladder (Volume-Weighted)** — Standard link ratio method using volume-weighted average factors (Friedland Ch. 7; foundational development method per ASOP No. 43 Section 3.6.1)
2. **Chain Ladder (Simple Average)** — Arithmetic average of age-to-age factors for comparison
3. **Bornhuetter-Ferguson** — If earned premium is provided; blends expected loss ratio with chain ladder (Friedland Ch. 9; Bornhuetter & Ferguson, PCAS 1972; incorporates credibility concepts per ASOP No. 25)
4. **Cape Cod** — If earned premium is provided; derives expected loss ratio from the data itself (Friedland Ch. 10; Stanard, PCAS 1985)
5. **Expected Loss Ratio** — If earned premium and an a priori loss ratio are provided (Friedland Ch. 8; useful when development data has limited credibility per ASOP No. 43 Section 3.6.1)

### Step 3: Review Diagnostics

The script also produces diagnostic exhibits. Review these and call out to the user:

- **Calendar year development test**: Checks if development along diagonals is consistent. Large swings may indicate reserve strengthening/weakening or operational changes.
- **High/low factor analysis**: Flags individual age-to-age factors that are outliers (>2 standard deviations from the mean for that development period).
- **Tail factor sensitivity**: Shows how ultimates change under ±10% and ±25% tail factor variations.
- **Incurred-vs-paid gap** (if both triangles provided): Large divergence in later maturities may signal case reserve adequacy issues.
- **Residual plots**: Standardized residuals from the chain ladder model to check for systematic patterns.

These diagnostics align with ASOP No. 43 Section 3.7.1 (Reasonableness), which calls for the actuary to assess whether results are reasonable. The calendar year test and outlier analysis help identify data irregularities referenced in ASOP No. 23 Section 3.3 (Review of Data). See also Friedland Ch. 6 for discussion of the development triangle as a diagnostic tool and Werner & Modlin Ch. 6 for loss development context in ratemaking.

### Step 4: Interpret Results and Present

After running the analysis:

1. Copy the output Excel to `/mnt/user-data/outputs/`
2. Present the file to the user
3. Provide a **narrative summary** that includes:
   - The range of indicated ultimates across methods
   - Whether carried reserves appear adequate, deficient, or redundant relative to the chain ladder indication
   - Which accident years show the most development volatility
   - Any red flags from the diagnostics
   - Caveats about data limitations and the quick-check nature of the analysis
   - Reference the concept from ASOP No. 43 Section 3.7 (Unpaid Claim Estimate) and 3.7.1 (Reasonableness) — note that a point estimate is a selection, and the actuary should assess whether results are reasonable

**Important tone guidance**: This is a quick check, not a full reserve study. Always caveat that:
- The analysis relies on standard methods and does not incorporate claim-level information
- Tail factor selection is mechanical and should be reviewed by a credentialed actuary
- Results should be cross-referenced with operational knowledge (e.g., changes in claims handling, coverage, or legal environment)
- This does not constitute an actuarial opinion under ASOP No. 43 or a Statement of Actuarial Opinion per ASOP No. 36. A credentialed actuary should review results, apply professional judgment on factor selections, and consider the requirements of ASOP No. 43 Section 3 before relying on these estimates for decision-making

### Step 5: Interactive Follow-Up

After presenting results, offer the user options to:
- Adjust tail factors manually
- Exclude specific accident years or development periods
- Change the weighting scheme for age-to-age factors
- Run sensitivity scenarios on the a priori loss ratio (for BF/Cape Cod)
- Compare against a benchmark loss ratio

When adjusting selections, note that ASOP No. 43 Section 3.6.7 (Changing Conditions) and 3.6.6 (External Conditions) may affect development patterns and tail behavior. ASOP No. 25 provides guidance on credibility weighting when blending methods. Tail factor considerations are discussed in Friedland Ch. 7 as part of the development technique.

## Key Actuarial Concepts (Reference)

Read `references/methods.md` for detailed formulas and implementation notes on each method if needed during development or debugging.

## Error Handling

- If the triangle has fewer than 3 accident periods, warn that credibility is very limited. ASOP No. 25 Section 3.4 (Professional Judgment) notes that credibility assessment is not always a precise mathematical process; triangles with very few data points may warrant heavier reliance on the ELR or BF methods with an externally-derived expected loss ratio
- If any development factors are < 1.0 (negative development), flag explicitly — it may be legitimate but warrants explanation
- If the triangle is not square (jagged), handle gracefully by only computing factors where data exists
- If earned premium is not provided, skip BF and Cape Cod methods and note this in the output
