# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`ai-data-report-skill` is a **Claude Code plugin / agent skill**, not an application. It ships instructions plus one self-contained HTML renderer; there is no build step, no package manifest, no test suite and no dependencies. What users run is `skills/data-report/SKILL.md` read by an AI agent, which then produces a standalone HTML file from `skills/data-report/template.html`.

```
skills/data-report/SKILL.md        # the skill: instructions, DOC schema, chart selection rules
skills/data-report/template.html   # the renderer: CSS + Canvas 2D drawing code + page shell
examples/                          # generated demo pages (GitHub Pages) + PNG screenshots
.claude-plugin/{plugin,marketplace}.json  # plugin metadata; marketplace name "neosun-skills"
README.md / README.zh-CN.md        # user-facing docs, kept in sync with each other
```

Installed by users via `/plugin marketplace add NeoSunxz/ai-data-report-skill` + `/plugin install data-report@neosun-skills`, or `npx skills add NeoSunxz/ai-data-report-skill`. The examples under `examples/` are published at https://neosunxz.github.io/ai-data-report-skill/ — anything committed there is public.

## The `DOC` contract is the whole architecture

The agent never writes chart code. It fills in a single JavaScript object `DOC` and substitutes it for the one marker line in the template:

```
var DOC = {};      // line 117 — exactly one occurrence, and the only line an agent edits
```

`template.html` contains two separable pieces:

- **`/* ===== CHARTS_JS START ===== */` … `/* ===== CHARTS_JS END ===== */`** (lines ~119–2079) — a dependency-free Canvas 2D drawing library that exports `window.Charts`. It is meant to be copied verbatim into third-party HTML decks (SKILL.md §6), so it must stay self-contained, ES2017-only, and must not reference the page shell or `DOC`. Chart functions are registered in the `API` object near the end of the block: `bar, column, line, donut, stacked, waterfall, kpi, dumbbell, waffle, bullet, calendar, calendarMonths, imageCards, tileMap, scatter, radar, table, dashboard`, plus `palette`, `dashboardHeight`, `num`, `THEMES`, `parseDate`, `dateKey`. Every registered chart is wrapped to reset the hover hit-test array (`canvas.__hits`) per draw — preserve that wrapper when adding a kind.
- **The rest of the file** — page CSS, the `DOC`-driven page shell (`gallery()` for `charts`, `report()`, `slides()`), theme switching, hover tooltips, and print CSS. This part **must not be modified** by the skill at runtime; only `DOC` changes.

Three output modes: `charts` (gallery of downloadable PNG sizes), `report` (long page printing to A4), `slides` (1920×1080 stage, arrow keys / F / click, prints one slide per page). Canvas ids are a public API used for headless export: `chart-<n>-16x9`, `chart-<n>-3x4`, `chart-<n>-chart`, `chart-<n>-long` in charts mode; `chart-<n>` in report/slides.

## Conventions that matter when editing

- **Do not "clean up" or reformat `template.html`.** It is intentionally dense, minified-ish, with Chinese comments. Stylistic edits create enormous diffs and risk changing rendering.
- **Keep the three examples in sync.** `examples/demo.html`, `examples/report.html`, `examples/slides.html` are each the current template with only two changes: the `<title>` and the `DOC` value. Each still carries its own copy of `CHARTS_JS`. After any change inside the CHARTS_JS block, the block must be byte-identical in `template.html` and all three examples; after shell/CSS changes, the examples must be regenerated. Verify with:
  ```bash
  for f in examples/*.html; do diff <(sed -n '/CHARTS_JS START/,/CHARTS_JS END/p' skills/data-report/template.html) <(sed -n '/CHARTS_JS START/,/CHARTS_JS END/p' "$f") >/dev/null && echo "$f ok" || echo "$f STALE"; done
  ```
- **Regenerating an example**: start from the template and replace only the `<title>` and the `var DOC = {};` line (the agent path in SKILL.md §5 shows the Python one-liner). Don't hand-build a page.
- **Bilingual surface.** Chart strings live in the `T` tables (`zh`/`en`) inside the CHARTS_JS block; page UI strings live in `UI` in the shell. `DOC.lang` selects one and also drives font stacks. A new user-visible string needs both `zh` and `en`.
- **Themes** are `THEMES.latte` (default), `THEMES.mist`, `THEMES.navy` (dark), plus a custom-colors object path in `customTheme()` that derives `cats` by comparing supplied colors. `THEMES.forest` is a backward-compat alias for `navy` — keep it.
- **Scaling**: the drawing code is authored against a 1080×1440 base; `setup(ctx)` derives `s` from the actual canvas size, and `u(n)` applies it. Use `u()` for every dimension and `font()` for every font, or charts break at 16:9.
- **Files are UTF-8 with CRLF line endings** (git `core.autocrlf=true` on Windows). Don't introduce LF-only rewrites or a BOM — embedded `data:` images and the template copy rely on byte-level integrity.
- SKILL.md is prose addressed to an AI agent. Changes there change behaviour as much as code changes do: chart-selection rules (§2), the "never invent numbers" rules (§1), and the pre-delivery checklist (§7) are the guardrails that make output trustworthy. Don't weaken them for brevity.
- README and README.zh-CN are parallel documents; update both. The feature list must match what the chart code actually supports (it enumerates the 17 chart types).

## Verifying changes

There is no test command. Verify in a real browser:

```bash
pip install playwright && playwright install chromium   # only if not already installed
```

Load a page via `file://`, wait ~1s for canvas drawing, and check every chart/slide for cut-off or crowded text; export PNGs with `canvas.toDataURL('image/png')` (SKILL.md §5 has the exact Playwright snippet). PDFs may only be produced through a browser (`emulate_media(media="print")` + `pg.pdf(...)`); tools that don't execute JavaScript (WeasyPrint, wkhtmltopdf, pandoc, LibreOffice) yield blank charts and are explicitly disallowed by the skill.

## Git

Default branch `main`, remote `git@github.com:NeoSunxz/ai-data-report-skill.git`, GitHub Pages serves `examples/` from `main`. No CI. Commit messages are short, imperative, sentence case (see `git log`).
