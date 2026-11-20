# Patterns

This repository contains patterns examples in Typescript, Python languages.

## Layout

Each pattern lives in its own folder, grouped by category (for example `creation/factory`):

```
<category>/<pattern>/
├── README.md   # pattern actors and how they map to the example
├── index.ts    # TypeScript implementation
└── main.py     # Python implementation
```

## Prerequisites

- Node.js and npm (developed with Node 24, npm 11)
- [uv](https://docs.astral.sh/uv/) and Python 3.13

## Install

```sh
npm install   # TypeScript tooling: tsc, ESLint, Prettier, tsx
uv sync       # Python tooling: ruff
```

## Run an example

```sh
npx tsx creation/factory/index.ts
uv run creation/factory/main.py
```

## Checks

| Scope      | What         | Check                          | Fix                         |
| ---------- | ------------ | ------------------------------ | --------------------------- |
| TypeScript | types        | `npm run typecheck`            | -                           |
| TypeScript | lint         | `npm run lint`                 | -                           |
| TypeScript | format       | `npm run format:check`         | `npm run format`            |
| TypeScript | all of above | `npm run check`                | -                           |
| Python     | lint         | `uv run ruff check .`          | `uv run ruff check --fix .` |
| Python     | format       | `uv run ruff format --check .` | `uv run ruff format .`      |

Run all of them before you commit:

```sh
npm run check && uv run ruff check . && uv run ruff format --check .
```

The same checks run in CI (`.github/workflows/ci.yml`) on every pull request and on pushes to `main`.

Configuration: `tsconfig.json` (strict, `moduleDetection: force` because every `index.ts` is a
standalone script that declares its own `ISender`, `Notification`, ...), `eslint.config.js`,
`.prettierrc.json`, and `[tool.ruff]` in `pyproject.toml`.
