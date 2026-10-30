# Excel Charts Skill — turn Excel / CSV into report-ready charts and dashboards with AI

An **agent skill** for Claude Code and other AI assistants that **turns a spreadsheet (Excel, CSV or a pasted table) into chart images and one-page dashboards** ready for slides, reports and phones. No install, no internet: the AI writes one HTML file, you open it in a browser and download PNGs.

[中文说明](README.zh-CN.md) · by **NeoSun**

![Dashboard example](examples/dashboard-16x9.png)

## Features

- **11 chart types**: bar chart, column chart, line chart, donut chart, stacked column chart, waterfall chart, KPI cards, dumbbell chart, waffle chart, bullet chart, calendar heatmap.
- **Dashboards**: a row of KPI cards plus 2–6 charts on one page, as a 16:9 slide or a long phone image.
- **Two sizes for every chart**: 3:4 for phones and social posts, 16:9 for PowerPoint, Keynote and Google Slides.
- **3 color themes**: Oat Latte, Mist Blue, Midnight Navy (dark), switched with one click.
- **Built for people new to data**: the AI first asks 3 questions (who it's for, which numbers matter, compared with what), cleans messy spreadsheets (several sheets, merged cells, dates stored as text, "$3,200" as text) and tells you what it changed.
- **No made-up numbers**: every value comes from your data, and the AI explains how it summarized.
- **English and Chinese** chart text (`lang: "en"` / `"zh"`).

![All 11 chart types](examples/all-charts.png)

## Install

**Claude Code**: copy the `skills/excel-charts` folder into `~/.claude/skills/` (all projects) or `.claude/skills/` in your project.

```bash
git clone https://github.com/NeoSunxz/excel-charts-skill.git
cp -r excel-charts-skill/skills/excel-charts ~/.claude/skills/
```

**Other AI assistants** (any tool that reads Agent Skills, or none at all): attach `skills/excel-charts/SKILL.md` and say "follow these instructions".

## Use

1. Give the AI your spreadsheet and say "chart this" or "build me a dashboard".
2. It creates an HTML file. Open it in Chrome or Edge.
3. Click the download buttons under each chart to save PNGs.

To see it first, open [`examples/demo.html`](examples/demo.html) in a browser. It uses made-up coffee shop data.

## Limits

- Static images: no clicking or filtering; regenerate when the data changes.
- Each chart has a row limit (for example 15 bars, 4 lines), so large data is summarized first.
- Text uses the fonts on your computer, so letter shapes differ slightly between machines.
- The page runs only in your browser and never uploads your data.

## License

[MIT](LICENSE) © NeoSun
