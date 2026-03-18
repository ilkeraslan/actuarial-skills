# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2026-03-17

### Added
- Tail factor derivation transparency in SKILL.md — instructs Claude to build a LINEST-based derivation block on the ATA sheet so the tail factor is fully traceable (selected factors → LN(excess) → LINEST slope/intercept → projected factors → PRODUCT)
- Sample earned premium file (`examples/sample_premium.csv`) — enables BF and Cape Cod methods on sample data
- Premium generation in `generate_sample_data.py` (`--premium-output` argument, `generate_premium()` function)

### Changed
- Scaled claim severity in `generate_sample_data.py` (log_mean 2.9 → 3.21) so generated paid triangles are consistent with `sample_triangle.csv` when tested against the same premium
- Regenerated `sample_loss_transactions.csv` with updated parameters
- SKILL.md Step 4: moved tail factor from "static values" list to "formula" list with detailed derivation instructions
- SKILL.md Step 1: added sample data inventory (triangle, transactions, premium)

## [0.2.1] - 2026-03-17

### Changed
- Added "Rebuild Workbook with Formula Transparency" step to SKILL.md (new Step 4)
- SKILL.md now instructs Claude to rebuild the script-generated workbook so every derived cell uses a live Excel formula with a cached calculated value
- Specifies exactly which cells must be formulas vs. static values (triangle data, premium, and diagnostics stay static; all ATA factors, averages, CDFs, ultimates, IBNR, and cross-sheet references become formulas)
- Python analysis script (`reserve_analysis.py`) unchanged — continues to produce reliable static-value workbooks as the computation engine

### Note
- Formula transparency is handled at the skill instruction layer, not in the Python script, because Claude can natively produce formula-based workbooks with correct cached values when instructed via SKILL.md
- Diagnostics remain as static values — complex statistical operations not suited to Excel formulas

## [0.2.0] - 2026-03-15

### Added
- Transaction-level data support in `parse_triangle.py` — raw claim-level CSV files (with `claim_id`, `accident_date`, `evaluation_date`, loss columns) are now auto-detected and aggregated into development triangles
- Sample raw loss transaction dataset (`loss-reserve-analysis/examples/sample_loss_transactions.csv`) with ~490 claims across 5 accident years
- Generator script (`loss-reserve-analysis/examples/generate_sample_data.py`) for reproducible synthetic data
- `.gitignore` for common OS and Python artifacts
- CODEOWNERS file for automated PR review assignment

### Changed
- Moved sample data from root `examples/` into `loss-reserve-analysis/examples/` for skill-level co-location
- Repository is now public with branch protection on `main`

## [0.1.0] - 2026-03-09

### Added
- Loss Reserve Analysis skill — Chain Ladder, Bornhuetter-Ferguson, Cape Cod methods with diagnostics and formatted Excel output
- Repository structure with `scripts/`, `references/`, `examples/`, and `releases/` directories
- README with project mission, quick start guide, and roadmap
- CONTRIBUTING guide with skill development guidelines
- PR and issue templates for contributors
