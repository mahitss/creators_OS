# Vapor OS — Contributing Guidelines

Thank you for contributing to Vapor OS! All pull requests must adhere to our Sprint 1 engineering standards.

---

## Contribution Workflow

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Commit Convention**:
   We enforce [Conventional Commits](https://www.conventionalcommits.org/):
   * `feat: ...` — New feature implementation
   * `fix: ...` — Bug fix
   * `docs: ...` — Documentation updates
   * `chore: ...` — Tooling/build updates

3. **Pre-Push Quality Checks**:
   Before opening a PR, ensure all local validation checks pass:
   ```bash
   pnpm lint
   pnpm typecheck
   pnpm test
   ```

4. **Pull Request Review**:
   * All CI/CD GitHub Actions checks must pass.
   * PRs must be under 300 lines of code diff wherever possible.
