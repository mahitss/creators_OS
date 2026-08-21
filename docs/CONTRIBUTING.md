# KINETIQ — Engineering Contribution Guide

## 1. Development Principles

1. **Production-Grade Engineering**: Write code intended to run enterprise workloads. No hacks, no shortcuts, no fake synthetic mocks.
2. **Zero Breaking Changes**: Do not break existing API contracts, database schemas, or working features.
3. **Type Safety**: Maintain strict TypeScript in `apps/web` and `packages/*`, and Python type hints across `apps/api`.
4. **Matte Black Visual Discipline**: Strict adherence to the Kinetiq design tokens (`#050505` canvas, monochrome text, `#62E6B2` operational green, zero emoji characters).

---

## 2. Local Setup & Workflow

```bash
# 1. Install dependencies
pnpm install

# 2. Start development servers
pnpm run dev

# 3. Run test suites
pnpm --filter vapor-web test
python -m pytest apps/api/tests
```

---

## 3. Pull Request Checklist

- [ ] All new backend endpoints require authentication and tenant isolation.
- [ ] Database queries are scoped by `workspace_id` and have appropriate indices.
- [ ] Frontend changes respect the matte-black design tokens and zero-emoji rule.
- [ ] All tests in Vitest and Pytest pass cleanly.
