# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-06-30

### Added
- Standard Sphinx Makefile and make.bat for local documentation building.
- Missing module and class docstrings to reach 100% docstring coverage.
- Jupyter Notebook tutorial for interactive usage.
- Missing codecov badges in documentation.

### Changed
- Improved test coverage to 100%.
- Bumped mypy to >=1.15.0 and set python_version to 3.12 to fix numpy stub parsing errors in CI.
- Updated documentation links and URLs to use the `elkins-lab` organization.
- Simplified package installation instructions by removing raw GitHub URLs.
- Standardized and simplified Google Colab setup blocks across all notebooks.
- Restructured tutorials and fixed linting issues.
- Updated ci workflow to force javascript actions to use Node.js 24 (fixing deprecation warnings).
- Refactored to use unified physical constants from `synth-core`.

### Fixed
- Import sorting to satisfy ruff.
- Silenced punycode deprecation and missing cache directory warnings.
- Suppressed noisy MDAnalysis warnings in the test suite.

## [0.1.2] - 2026-06-07

### Changed
- Maintenance release: General updates, dependency pins, and CI/CD workflow improvements.
