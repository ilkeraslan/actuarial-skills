# Actuarial Skills for Claude

**Open-source Claude skills for property & casualty actuaries.**

AI is reshaping how actuaries work — but the profession benefits most when practical tools are shared openly. This project provides ready-to-use Claude skills that encode standard actuarial methods, so any actuary can leverage them immediately. Think of it as a starting point: use these skills as they are, adapt them to your workflows, or contribute new ones. The goal is to build a shared foundation that helps the insurance industry move forward together.

---

## What Are Skills?

Skills are packaged workflows that extend Claude's capabilities for domain-specific tasks. When you install an actuarial skill into a Claude Project, Claude automatically recognizes when to use it — upload a loss triangle and ask "check my reserves," and Claude runs a full analysis using standard actuarial methods without you writing a single line of code.

Skills work in [Claude.ai](https://claude.ai) Projects and [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Available Skills

### Loss Reserve Analysis

Upload a loss development triangle (Excel or CSV) and get a multi-method reserve analysis with formatted exhibits — in seconds.

**Methods included:**
- Chain Ladder — volume-weighted and simple average age-to-age factors
- Bornhuetter-Ferguson — blends a priori ELR with development patterns
- Cape Cod (Stanard-Bühlmann) — derives ELR directly from the data
- Tail factor estimation via exponential decay extrapolation

Methods reference standard actuarial literature including Friedland's *Estimating Unpaid Claims Using Basic Techniques* and relevant ASOPs (No. 43, 23, 25, 36) for educational context.

**Output:** A 6-exhibit Excel workbook containing:

| Exhibit | Contents |
|---------|----------|
| 1 — Triangle | Your input data, formatted |
| 2 — ATA Factors | Individual and selected age-to-age factors (volume-weighted, simple, medial) |
| 3 — CL Ultimates | Chain ladder projected ultimates, CDFs, IBNR by accident period |
| 4 — BF & Cape Cod | Bornhuetter-Ferguson and Cape Cod results (when premium is provided) |
| 5 — Diagnostics | Calendar year test, outlier factor detection, tail factor sensitivity |
| 6 — Summary | Side-by-side method comparison with range analysis |

**Diagnostics automatically flag:**
- Outlier development factors (>2σ from the column mean)
- Calendar year diagonal inconsistencies
- Negative development (factors < 1.0)
- Sensitivity of total IBNR to ±10% and ±25% tail factor changes

### More Skills Coming Soon

We're building additional skills for common actuarial workflows. See the [Roadmap](#roadmap) below.

## Quick Start

### Option 1: Install the `.skill` File (Recommended)

1. Download `loss-reserve-analysis.skill` from the [Releases](../../releases) page
2. Open a Claude.ai Project → Project Settings → Skills
3. Upload the `.skill` file
4. Upload any loss triangle and ask Claude to analyze it

### Option 2: Add Manually to a Project

1. Clone this repo
2. In your Claude.ai Project, add the contents of `loss-reserve-analysis/` to your Project Knowledge
3. Claude will automatically reference the skill when you upload triangles

## Example Usage

Upload a file like this to your Claude Project conversation:

| Accident Year | 12 | 24 | 36 | 48 | 60 |
|---------------|------|------|------|------|------|
| 2019 | 1,610 | 2,450 | 2,810 | 2,990 | 3,070 |
| 2020 | 1,390 | 2,080 | 2,390 | 2,540 | — |
| 2021 | 1,550 | 2,340 | 2,680 | — | — |
| 2022 | 1,820 | 2,750 | — | — | — |
| 2023 | 2,100 | — | — | — | — |

Then ask:

> "Run a loss reserve analysis on this triangle. It's incurred losses in thousands, development in months."

Or, if you also have premium data:

> "Check reserves on the attached triangle. Earned premiums are in the second sheet. Use BF and Cape Cod too."

Claude parses the triangle, runs all applicable methods, and returns a formatted Excel report with the exhibits described above plus a narrative summary of findings.

## Supported Input Formats

The skill handles common triangle layouts automatically:

- **Standard triangle** — rows are accident periods, columns are development periods (most common)
- **Columnar / long format** — three columns: accident period, development period, loss amount
- **Excel or CSV** — `.xlsx`, `.xls`, `.xlsm`, `.csv`
- **Multiple sheets** — specify which sheet contains the triangle; premium data can be on a separate sheet

Development periods can be in months or years. Accident periods can be annual or quarterly.

## Important Caveats

This is a **quick check**, not a full reserve study. Specifically:

- Methods are standard textbook implementations — they don't incorporate claim-level information, operational context, or judgment that a credentialed actuary would apply
- Tail factor selection is mechanical (exponential decay). Production reserve analyses require actuarial judgment on tail selection
- Results should be cross-referenced with knowledge of changes in claims handling, coverage, legal environment, or reinsurance
- **This does not constitute an actuarial opinion under ASOP No. 43 or a Statement of Actuarial Opinion per ASOP No. 36**
- ASOPs are referenced throughout for educational context — see the separate ASOP Compliance Advisor skill (roadmap) for compliance-focused guidance

Use this as a starting point, a sanity check, or a way to quickly explore your data — not as a substitute for a signed actuarial analysis.

## Roadmap

We plan to add skills for other common P&C actuarial workflows. Ideas we're considering (feedback welcome via [Issues](../../issues)):

- **Loss Development Triangle Analyzer** — deeper diagnostics, residual analysis, and method comparison visualizations
- **Actuarial Exhibit Formatter** — convert rough calculations into properly formatted, numbered exhibits
- **Rate Filing Completeness Checker** — cross-reference filing exhibits against state-specific requirements
- **Credibility Calculator** — classical and Bühlmann credibility with complement selection guidance
- **ASOP Compliance Advisor** — comprehensive compliance checking (complements the educational ASOP references in the Loss Reserve Analysis skill)

If you have ideas for skills that would save you time, open an issue or reach out.

## Contributing

We welcome contributions from actuaries and developers. Some ways to help:

- **Report bugs** — if a triangle format doesn't parse correctly, open an issue with a sample (anonymized) file
- **Suggest methods** — want to see Mack's model, bootstrapping, or GLM-based reserving? Let us know
- **Improve diagnostics** — the more red flags we can automatically surface, the more useful the quick check becomes
- **Add skills** — if you've built a workflow that other actuaries would benefit from, submit a PR

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Credits

Originally created by Kohei Kudo and [Kalta](https://kalta.ai).
