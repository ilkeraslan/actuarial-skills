# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
