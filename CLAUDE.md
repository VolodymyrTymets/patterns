# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Design-pattern examples, each implemented twice (TypeScript and Python) around the same
notification domain (`Sender`, `Notification`, `EmailSender`, `SmsSender`, ...). There is no
application, no build step and no test suite: each example is a standalone script that prints
to stdout when run.

## Commands

Install: `npm install` and `uv sync`.

| Purpose             | Command                                              |
| ------------------- | ---------------------------------------------------- |
| Typecheck TS        | `npm run typecheck`                                  |
| Lint TS             | `npm run lint`                                       |
| Format check TS     | `npm run format:check` (fix: `npm run format`)       |
| All TS checks       | `npm run check`                                      |
| Lint Python         | `uv run ruff check .` (fix: `--fix`)                 |
| Format check Python | `uv run ruff format --check .` (fix: drop `--check`) |
| Run TS example      | `npx tsx creation/factory/index.ts`                  |
| Run Python example  | `uv run creation/factory/main.py`                    |

Run each check on its own and report its real exit code. Prettier only covers `*.{ts,js,json}`,
so the box-drawing tables in the pattern READMEs are never reformatted.

## Structure

One folder per pattern, grouped by category: `<category>/<pattern>/{README.md,index.ts,main.py}`.
The README holds an "actors" table mapping the pattern's roles to the names used in the example;
keep it in sync with the code and with both language versions. Both versions of a pattern should
mirror each other (same class names and responsibilities).

Layout differs between branches: on `main`/`lint` patterns are under `creation/`, while the
`abstract-factory` and `builder` branches put them under `src/creation/`. `tsconfig.json`
includes both, so keep both globs when touching it.

## Gotchas

- Every `index.ts` is a global script (no imports/exports) and declares names like `ISender`
  that repeat across patterns. `tsconfig.json` sets `moduleDetection: "force"` so these do not
  collide; do not remove it, and do not add `export {}` to work around it.
- `index.ts` files call `main()` at import time, so they cannot be imported by a test without
  running the example.
- Prettier style is 4 spaces, single quotes, semicolons (matches existing code). Ruff selects
  `E,F,I,UP,B` with line length 100, target Python 3.13.
- Stale untracked `src/creation/abstract-factory/.mypy_cache/` may exist locally; it is ignored by
  `.gitignore` and not used (no mypy in this repo).
