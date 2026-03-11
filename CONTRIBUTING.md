# Contributing to Actuarial Skills for Claude

Thanks for your interest in contributing! This project aims to build useful, open-source Claude skills for the P&C actuarial community.

## Ways to Contribute

### Report Issues

If a triangle format doesn't parse correctly, a method produces unexpected results, or you find a bug, please open an issue with:

- A description of what you expected vs. what happened
- A sample input file (anonymized — no real policyholder or company data)
- The error message or incorrect output

### Suggest Enhancements

Open an issue tagged `enhancement` if you'd like to see:

- Additional reserving methods (e.g., Mack's model, bootstrapping, GLMs)
- Better diagnostics or visualizations
- Support for new input formats (e.g., Schedule P, NAIC Annual Statement)
- New skills entirely

### Submit a Pull Request

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test with sample triangle data
5. Submit a PR with a clear description of what you changed and why

### Skill Development Guidelines

If you're building a new skill:

- Follow the skill structure: `SKILL.md` + `scripts/` + `references/`
- Include clear trigger descriptions in the SKILL.md frontmatter
- Add appropriate caveats (these are tools, not actuarial opinions)
- Test with at least 2-3 different input formats
- Anonymize any sample data

## Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes to skill format or structure
- **MINOR** — new skill added or significant method added to an existing skill
- **PATCH** — bug fixes, documentation updates, minor improvements

When submitting a PR, update [CHANGELOG.md](CHANGELOG.md) under an `## [Unreleased]` section. Maintainers will assign the version number at release time.

## Developer Certificate of Origin (DCO)

By contributing to this project, you certify that you have the right to submit your work under the [MIT License](LICENSE). We use the [Developer Certificate of Origin](https://developercertificate.org/) — sign your commits by adding a `Signed-off-by` line:

```
git commit -s -m "Add new method to loss reserve analysis"
```

This adds a line like `Signed-off-by: Your Name <your@email.com>` to your commit message.

## Code of Conduct

Be kind, be constructive, and remember that actuaries are people too.

## Questions?

Open an issue or start a discussion on GitHub.
