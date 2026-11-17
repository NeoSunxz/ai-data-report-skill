---
name: data-report
license: MIT
description: Turns data into charts, a one-page dashboard, a printable report or HTML slides, choosing the charts that answer what the user wants to know. 17 chart types: bar, column, line, donut, stacked column, waterfall, KPI cards, dumbbell, waffle, bullet, calendar heatmap, month calendar, image cards, tile map (US states, Chinese provinces), scatter, radar, table. Use when the user has data (Excel, CSV, a pasted table, database or BI query results, or numbers typed in the chat) and asks to chart it, build a dashboard, write a data report, a business review, a weekly or monthly report, turn data into slides, analyze it, or which chart to use; prefer it whenever the result needs charts and goes to other people as a page, PDF, dashboard or deck; also when another presentation skill or template needs charts. Not for editing formulas or cells inside a spreadsheet file, or for producing native .xlsx, .pptx or .docx files.
---

# data-report: from what you want to know to charts, dashboards, reports and slides

How it works: find out what the user wants to know → suggest a report plan (section 2) → read and clean the data → pick charts → choose the output (charts, dashboard, report or slides) → fill in one `DOC` object → drop it into the web page template at the end of this file → the user opens one HTML file in a browser.

The user may know nothing about data. Use plain words throughout. Don't say "dimension", "measure", "aggregate" or "field"; say "by store", "added up", "this column".

All drawing code is in `template.html`, next to this file. Nothing is downloaded or installed. **Copy the template and change only the `var DOC = {};` line.** Don't touch anything else.

## 0. Find out what they want

**Make as many charts as were asked for.** "Make a chart", "chart this", "which chart should I use" means **one** chart that answers the question asked: no questions, no report plan. When it's delivered, offer one specific extra chart in a sentence ("Want a second chart with each store's actual sales?"). Make several charts only when the user asks for several, or wants a dashboard, report or slides; report plans (section 2) are for those.

If the request is specific ("make a bar chart of sales by store", "turn this into 6 slides"), skip the questions and do it.

**If the user named the format, the format is decided.** "Report" or "review report" means `report`, "dashboard" means a dashboard, "deck" or "slides" means `slides`, "chart" means images (section 3). Don't ask about the format again and don't switch to another one; if another format would also help, mention it once when you deliver ("I can also make a one-page dashboard image for the team chat").

If the user only says "build me a dashboard", "make a report" or "analyze this spreadsheet", look at the data first, then ask these questions **in one message** (skip question 1 when the format is already named). For each, offer options guessed from the data so the user can just pick or adjust. If your tool has a multiple-choice question feature (in Claude Code: AskUserQuestion), use it: one question per item, the best guess as the first option, up to 4 questions at once.

1. **Who is it for, and how will they see it?** (only when the format wasn't named) For example: a slide deck for a meeting / a report to send around / a dashboard image for a chat / charts to paste into my own slides. This picks the output (section 3).
2. **Which numbers matter most?** Pick 2–4 from the data, for example "sales, cups sold, average ticket".
3. **Compared with what?** For example: last year / the target / last month / nothing. If the data has nothing to compare with, say so. Don't make it up.
4. **Only if they want slides:** are they already using a slide template or another presentation skill (such as frontend-slides)? If yes, follow section 6.

If the user says "up to you" or "I don't know", use the default **business review**: KPI cards (key numbers vs. the comparison period) + a trend (by month) + a ranking (by store, product or person) + a breakdown (shares). Tell the user which question each part answers and that any part they don't need can be removed.

## 1. Read and clean the data. Never invent numbers

1. Read the data, wherever it comes from: an Excel or CSV file, a pasted table, the results of a database or BI query (for example a DAX or SQL query run through an MCP server), or numbers the user typed in the conversation. Note the columns, the units, and any total rows or blank rows. When numbers come only from the conversation, repeat them back in a small table before drawing.
2. Every number in a chart must come from the user's data or be calculated from it. **Don't fill gaps, don't estimate, don't round to nicer numbers.**
   - **Calculate with code, never in your head.** Sums, averages, shares, year-over-year changes, the daily rows for a calendar: compute them with a short script (Python, or JavaScript if that is what you can run) that reads the user's data.
   - **Let the script build `DOC`; don't type numbers by hand.** The script assembles `DOC` from its results and writes it into the page (code in section 5). Numbers inside titles and points come from the script's variables too (an f-string, for example): hand-copied numbers end up on the wrong month or with the wrong digits.
   - Put the script's numbers into `DOC` at full precision; don't round them first. The page rounds for display. Rounding first makes related numbers disagree: an average rounded to 35.9 and 34.1 shows +5.3% while the total it came from shows +5.2%.
   - **Keep one script** (for example `report_data.py`, next to the page) so every number can be traced. Fix errors in that script instead of writing patch files like `fix.py`, and delete scratch files before delivering.
   - **Windows encoding:** read CSV files with `encoding="utf-8-sig"` and fall back to `"gbk"`; write results to a JSON file instead of printing non-ASCII text to the console (or set `PYTHONIOENCODING=utf-8` first).
   - If you can't run code, say so, keep the summaries small, and show how each total was worked out in the section 7 table.
   - **Name metrics by how they're calculated.** Sales ÷ cups (or units) is "average price per cup/unit", not "average ticket" or "average order value", which need an order count; a repeat rate needs customer or member data; margin needs costs. If the data doesn't have it, don't use the term.
3. When you need to summarize (sum by month, sum by store, work out shares), first tell the user in one sentence how, for example "I added up each store's daily sales for 2025".
4. Don't draw total or subtotal rows as a category.

Spreadsheets made by people new to data often have the problems below. Fix them yourself, **without changing the original file**, then tell the user what you did in one plain sentence:

| Problem | What to do | What to tell the user (example) |
|---|---|---|
| Several sheets in one file | List what each sheet is and ask which to use; if it's clearly one table split by month, combine them | "January to December were on 12 sheets; I combined them into one" |
| Merged cells | Fill the merged value into every row | "Store names were in merged cells; I filled the name into every row" |
| Several header rows, with a title or notes on top | Find the real header row and skip what's above it | "I started reading at row 3; the first two rows are a title" |
| Dates stored as text or in mixed formats | Convert to YYYY-MM-DD; list any you can't read and ask. Watch for day/month order (3/5/2025 can be March 5 or May 3): check the other rows, and ask if still unclear | "3 dates were written as 'March 5th'; I used 2025-03-05" |
| Units or symbols inside numbers ("12k", "$3,200", "15%") | Convert to plain numbers and put the unit in the subtitle | "I removed the '$' from sales; the unit is shown on the chart" |
| The same thing spelled differently ("Main St", "Main Street") | Merge if you're sure they're the same, otherwise ask | "I treated 'Main St' and 'Main Street' as the same store" |
| Blank rows, stray spaces, duplicate rows | Skip blank rows; for identical rows, ask whether they're a double entry | "2 rows are exactly the same. Count them once?" |
| Missing data (a month with no numbers) | Don't fill it. Line charts break there, column charts skip that column; say so | "There's no data for July, so that spot is empty" |

## 2. Pick the charts

First decide what question the chart answers, then pick the chart. If the user names a chart, use it.

| Question | Chart | kind |
|---|---|---|
| Who is bigger, what's the ranking | Bar chart | `bar` |
| How much each month / year (in time order, one series) | Column chart | `column` |
| Where the trend is going, a few lines compared (in time order) | Line chart | `line` |
| How big each part is (up to 6 parts) | Donut / waffle chart | `donut` / `waffle` |
| The total at each point in time, and what it's made of | Stacked column chart | `column` + `stack: true` (or `stacked`) |
| Two or more numbers per item side by side (this year vs last, actual vs plan) | Grouped bar / column | `bar` / `column` + `series` |
| Which items are bigger, and what each is made of | Stacked bar | `bar` + `series` + `stack: true` |
| How the mix differs between items (channel share by store, share by quarter) | 100% stacked bar / column | `bar` / `column` + `series` + `stack: "percent"` |
| How A became B: what added and what took away | Waterfall chart | `waterfall` |
| A few key numbers and how they compare | KPI cards | `kpi` |
| How much each item changed between two points in time | Dumbbell chart | `dumbbell` |
| Did each item hit its target | Bullet chart | `bullet` |
| Highs and lows for every day of a year: busy and quiet seasons, weekends vs. weekdays | Calendar heatmap (one row for the year) | `calendar` |
| Each day month by month, to find specific days (holidays, promotions, the best day) | Month calendar heatmap (12 small months) | `calendarMonths` |
| A ranking of products, stores or people, with pictures (menu, product wall, store photos) | Image cards | `imageCards` |
| Numbers by region (US states, Chinese provinces) | Tile map | `tileMap` |
| Whether two numbers move together (price and cups sold, ticket size and repeat rate) | Scatter plot | `scatter` |
| Scoring one to three items on several measures (a store health check) | Radar chart | `radar` |
| Several columns of exact numbers per item (a scorecard, a detail list) | Table | `table` |
| Several questions on one page | Dashboard | `dashboard` |

A few rules:
- One chart answers one question. If the data answers several questions, make several charts.
- Categories with no natural order (stores, products) go in a bar chart, not a column chart.
- Shares of **one** whole: donut or waffle. Shares compared **across several items**: 100% stacked bar (stores) or column (time).
- The parts of a share chart must add up to one whole. Things that aren't parts of a whole (such as overlapping metrics) can't go in a donut or waffle chart.
- Two sets of numbers in different units (such as sales and cups sold) go in two charts. Don't force them into one.
- With only 1–2 numbers, use KPI cards instead of a chart.
- The two calendars take the same data: the calendar heatmap shows **patterns across the year**; the month calendar is for **finding specific days**. Use both if both questions matter.
- Use image cards only when the pictures help (telling which product or store it is). Without pictures, a bar chart is clearer.
- **Reports and decks get at most 6 charts by default** (a row of KPI cards counts as one). Add more only if the user asks.
- **Each set of numbers goes in one chart.** Don't show the same values again as a grouped bar, a dumbbell and a table; pick the one that answers the question best. A KPI card with the overall total is fine.
- A dumbbell chart works when each item's change is about as large as the gaps between items. When the changes are small next to those gaps (stores between 24 and 47 that each moved 1–3), the dots sit on top of each other; chart the change itself instead (`bar` of the % change).
- A scatter plot shows that two numbers move together, never that one causes the other (section 7). With fewer than 8 points, check whether a bar chart is clearer.
- Every measure on a radar chart must be on the same scale (scores, percentages). Convert different units to scores first (for example, the best item on each measure = 100) and say how in the subtitle. At most 3 items and 3–8 measures; for more items use a table or a grouped bar chart.
- The tile map knows US states and Chinese provinces only. For cities, sales territories and other regions, use a bar chart.

### Common requests → report plans

Most requests are a question, not a chart name. Match the request to a plan below, suggest it to the user with one line per chart ("this chart answers ..."), and drop any chart the data can't support (say which and why). Plans work for a dashboard, a report or slides alike.

| The user says something like | Plan (in order) |
|---|---|
| "How did we do this year / this month?" (a review) | KPI cards vs. last period → monthly trend (`column` or `line`) → ranking by store / product (`bar`) → who drove the growth (a `bar` of each store's change, with the total change in the title; use a `waterfall` only when the changes are large next to the total, or the change segments are too thin to see) → what it's made of (`donut` or `waffle`) → if there are costs: why profit changed (`waterfall`) |
| "Which store / product has a problem?" | KPI cards → who missed the target (`bullet`) → who dropped vs. last year (`dumbbell`) → when it dropped (`calendar`, or `line` by week) |
| "How is this product / category doing?" | Ranking with pictures (`imageCards`, or `bar` without pictures) → its trend (`line`) → where it sells (`bar` + `stack: "percent"` by store or channel) |
| "Are we on track for the target?" | Completion as KPI cards → each item vs. its target (`bullet`) → actual vs. plan by month (`column` + `series`) |
| "When are our busy and quiet seasons?" | Every day of the year (`calendar`) → by month (`column`) → weekdays vs. weekends (`column` of daily averages by weekday) → specific days to plan around (`calendarMonths`) |
| "Where does the money come from?" | Shares of the whole (`donut` or `waffle`) → how the mix differs by store or quarter (`bar` / `column` + `stack: "percent"`) → what changed the total (`waterfall`) |
| "Compare A and B" (stores, years, plans) | The overall gap in one number (KPI cards) → how much each changed (`bar` of the % change; `dumbbell` when the changes are as large as the gaps between items) → the actual values, only if still needed (`bar` + `series` or `table`, not both) → several measures at once (`radar`, up to 3 items) |
| "Where do we sell well?" | By region (`tileMap`) → regional ranking (`bar`) → details for the top regions (`table`) |
| "Is X related to Y?" (price and sales, promotions and visits) | Both numbers together (`scatter`) → each one's trend (`line`; never two units in one chart) |
| "Give me a scorecard" | Key numbers (KPI cards) → several numbers per item (`table`) → who missed the target (`bullet`) |

If the request fits none of these, build the plan from the table above: one question per chart, at most 6 charts.

## 3. Choose the output

| The user wants | `DOC.mode` | What they get |
|---|---|---|
| One or a few chart images | `charts` | **PNG files**: export them from the page yourself (section 5) and hand over the files. The page stays next to them as the tool for other sizes and colors |
| A dashboard image | `charts` with one `dashboard` chart | One page with KPI cards and 2–6 charts, as 16:9 or a long phone image |
| A report to read or send | `report` | One long web page: title, key findings, one section per chart with its explanation, and notes on the data. Prints neatly to A4 PDF |
| A slide deck, no template of their own | `slides` | An HTML deck (16:9, arrow keys to move, F for full screen, prints one slide per PDF page) in the 3 built-in themes |
| A slide deck in their own template or another slide skill | see section 6 | The storyline and charts in that deck's colors; the deck's look stays theirs |

### Images: wide or tall

When the user wants images, pick the size from the chart and the data, unless they named a size or where it will go (phone or social post → 3:4; slides or a work chat → 16:9).

- **Wide, 16:9**: things laid out left to right: time on the horizontal axis (`column`, `line`, `waterfall`, column `stack`), the one-row `calendar`, `scatter`, the US `tileMap`, grouped columns.
- **Tall, 3:4**: lists that run down the page: `bar`, `dumbbell` and `bullet` with more than 6 rows, `table` with more than 6 rows, `imageCards` with more than 6 cards, the China `tileMap`, `calendarMonths`.
- **Either**: shares (`donut`, `waffle`), `radar`, `kpi`, and lists of 6 rows or fewer. Use 16:9 unless the use points to a phone.
- **Transparent background** ("chart only"): only when the user asks for it, for example to paste into their own slide template.

### Write the story first (report and slides)

Before filling in `DOC`, write the storyline as a list: one line per section, each a **finding**, not a label ("December was the best month", not "Monthly sales"). Order: the overall picture first, then the biggest finding, then the details, then what to watch. 4–8 sections is plenty. Each section has one chart and 0–4 short points. Points say what the chart shows, with numbers from the data; no guessed reasons.

## 4. Fill in `DOC`

`DOC` is one object. Fields for every mode:

| Field | Required | Notes |
|---|---|---|
| `mode` | yes | `charts`, `report` or `slides` |
| `title` | yes | Page, report or deck title |
| `subtitle` | no | One line under the title |
| `author`, `date` | no | Shown under the title (report) or on the cover (slides). Use today's date for `date` (from the system clock, for example by running `date`); leave it out if unsure, never make one up |
| `theme` | no | `latte` Oat Latte (default), `mist` Mist Blue, `navy` Midnight Navy (dark), or an object with custom colors (section 6). Charts and reports also get buttons to switch |
| `lang` | no | Language of the text built into the charts and page (legends, "Total", month names, buttons): `"en"` by default; use `"zh"` when the user writes in Chinese. Write titles, subtitles and names in the user's language too |
| `sign` | no | A credit line, for example `"Store Ops Team"`. Not shown if left out |

**`charts` mode**: `DOC.charts` is an array of charts.
```json
{"mode": "charts", "title": "Sales charts", "charts": [{"kind": "bar", "title": "...", "rows": [...]}, {"kind": "dashboard", "title": "...", "panels": [...]}]}
```

**`report` and `slides` modes**: `DOC.summary` is 2–4 key findings (one sentence each); `DOC.sections` is the storyline, one chart per section; `DOC.notes` says where the data came from and how it was summarized. Each section is a chart object (formats below) plus:
- `title`: the finding, shown as the section heading or the slide headline. On slides keep it to one line (about 45 characters).
- `subtitle`: the unit and time range, for example "Monthly sales, $ thousands".
- `points`: 0–4 short sentences shown next to the chart (slides, and reports on wide screens; a printed report puts them under the chart). On slides, 2–3 points of under 60 characters each read best.
- `text`: (report only) a short paragraph instead of, or before, the points.
- `width`: (report only) `"half"` makes a half-width section; two neighbouring half-width sections share a row on wide screens. Use it for small charts such as shares or bar charts of 6 rows or fewer; a half-width section without a partner takes the full row. KPI cards, the one-row calendar, tables and image cards always take the full row. Leave it out to put the chart and its points side by side.
- `kind: "text"`: a section with points and no chart.
- In `slides` mode, `DOC.kicker` is a small label above the title on the cover, for example "Annual review"; `section.kicker` does the same on a slide.

```json
{"mode": "slides", "title": "2025 coffee shop review", "subtitle": "Sales, stores and channels across 6 stores", "author": "NeoSun", "date": "2026-01-15",
 "summary": ["Sales grew 5.2% to $215.3k, driven by more cups sold", "Delivery more than doubled and is catching up with dine-in"],
 "sections": [
  {"kind": "column", "title": "December was the best month", "subtitle": "Monthly sales, $ thousands", "rows": [{"name": "Jan", "a": 15.2}, {"name": "Feb", "a": 12.1}],
   "points": ["$24.0k in December, the highest of the year", "February was the low point at $12.1k"]},
  {"kind": "bar", "title": "Tech Park and Riverside lead", "subtitle": "2025 sales by store, $ thousands", "rows": [{"name": "Tech Park", "a": 46.9}, {"name": "Riverside", "a": 45.7}]}
 ],
 "notes": ["Made-up data for 6 stores", "Sales are summed by month and by store from daily sales"]}
```

### Chart formats

**Fill in values at full precision** (for example `45.0839`); don't round them first. The page shows one decimal place by itself. The change on KPI cards and the % change at the right of a dumbbell chart are calculated by the page from `a` and `b`: if `a` and `b` were rounded, those percentages won't match the text or the other charts.

Every chart has `kind` (from section 2), `title`, an optional `subtitle` and `rows`. Optional: `unit` (a short unit after each value, such as `"k"` or `"%"`; longer units go in the subtitle) and `file` (download file name in `charts` mode). Keep category names short (about 12 characters or fewer): on a crowded axis, long names get small text or only every other one is shown. Values can be numbers or numeric strings (`33.6`, `"33.6"`, `"1,280"`). In `charts` mode the title is drawn on the image: about 35 characters fit, longer titles are set smaller, then cut off.

**Bar chart `bar`**: `rows: [{name, a}]`. Sorted from largest to smallest automatically, up to 15 rows. `highlight: "Riverside"` highlights only that row and greys out the rest.

**More than one number per row** (bar and column alike): add `series` with the names and write each row as `{name, v: [one value per series]}`. Then `stack` picks the look:
- not set: **grouped**, bars side by side (up to 4 series, 12 rows). Bars are sorted by the last series, usually the latest.
- `true`: **stacked**, parts end to end with the total at the end (up to 5 series, 16 rows). Sorted by total.
- `"percent"`: **100% stacked**, every row adds up to 100%, with the % written in each part (up to 5 series, 16 rows). Bars are sorted by the first series' share; put the part you want to compare first.
- `sort: false` keeps your order (bars only; columns always keep it). Only positive values are drawn in these modes.
```json
{"kind": "bar", "stack": "percent", "title": "Campus relies most on delivery", "subtitle": "Share of sales by channel, 2025", "series": ["Delivery", "Dine-in", "Pickup"],
 "rows": [{"name": "Main St", "v": [9.2, 20.1, 4.3]}, {"name": "Campus", "v": [13.2, 9.1, 3.2]}]}
```
```json
{"kind": "bar", "title": "Which of our 6 stores sells the most", "subtitle": "2025 sales, $ thousands",
 "rows": [{"name": "Main St", "a": 33.6}, {"name": "Riverside", "a": 45.7}, {"name": "Tech Park", "a": 46.9}]}
```

**Column chart `column`**: `rows: [{name, a}]`. Drawn in the order given, up to 24 columns; negative values are fine. `highlight` works the same way.
```json
{"kind": "column", "title": "Monthly sales in 2025", "subtitle": "$ thousands", "highlight": "Dec",
 "rows": [{"name": "Jan", "a": 15.2}, {"name": "Feb", "a": 12.1}, {"name": "Mar", "a": 16.8}]}
```

**Line chart `line`**: `series` holds the line names (up to 4); `rows: [{name, v: [one value per line]}]`. Drawn in the order given, up to 60 points. Write `null` for a missing value and the line breaks there.
```json
{"kind": "line", "title": "Delivery is catching up with dine-in", "subtitle": "Cups per month, thousands", "series": ["Dine-in", "Delivery"],
 "rows": [{"name": "Jan", "v": [21.4, 9.8]}, {"name": "Feb", "v": [17.9, 9.1]}, {"name": "Mar", "v": [22.6, 11.5]}]}
```

**Donut chart `donut`**: `rows: [{name, a}]`, positive values only. With more than 6 parts, the 6th largest onward are merged into "Other". The total goes in the middle; `totalLabel` replaces the word "Total".
```json
{"kind": "donut", "title": "Where 2025 sales came from", "subtitle": "By category", "unit": "k",
 "rows": [{"name": "Coffee", "a": 161.2}, {"name": "Tea", "a": 26.9}, {"name": "Bakery", "a": 17.4}]}
```

**Stacked column chart `stacked`**: the same as `column` with `stack: true`. `series` holds the part names (up to 5, stacked bottom to top); `rows: [{name, v: [one value per part]}]`, up to 16 columns, positive values only. The total is written on top.
```json
{"kind": "stacked", "title": "Quarterly sales by channel", "subtitle": "$ thousands", "series": ["Dine-in", "Delivery", "Pickup"],
 "rows": [{"name": "Q1", "v": [28.4, 9.6, 6.1]}, {"name": "Q2", "v": [31.2, 13.8, 7.8]}]}
```

**Waterfall chart `waterfall`**: the first row is the starting value (such as last year's profit); each row after it is an increase (positive) or decrease (negative), up to 14 rows. The last column is calculated automatically and named with `endLabel`. **Check the calculated end value against the end value in the user's data. If they don't match, something is missing: tell the user first.**
```json
{"kind": "waterfall", "title": "Why profit went up this year", "subtitle": "$ thousands", "endLabel": "2025 profit",
 "rows": [{"name": "2024 profit", "a": 28.5}, {"name": "Sales up", "a": 12.6}, {"name": "Beans", "a": -4.8}]}
```

**KPI cards `kpi`**: `rows: [{name, a: current, b: comparison (optional), unit}]`, up to 6. With `b`, the change is shown; `labelB` is the text after it, for example "vs last year".
```json
{"kind": "kpi", "title": "2025 at a glance", "subtitle": "Compared with 2024", "labelB": "vs last year",
 "rows": [{"name": "Sales ($)", "a": 215.3, "b": 204.6, "unit": "k"}, {"name": "Repeat rate", "a": 38.5, "b": 35.1, "unit": "%"}]}
```

**Dumbbell chart `dumbbell`**: `rows: [{name, a: start, b: end}]`; `labelA` / `labelB` name the two points in time. Sorted by end value, largest first, with the percentage change on the right. Works best with up to 8 rows.
```json
{"kind": "dumbbell", "title": "Sales by store: 2024 vs 2025", "subtitle": "$ thousands", "labelA": "2024", "labelB": "2025",
 "rows": [{"name": "Main St", "a": 31.8, "b": 33.6}, {"name": "Riverside", "a": 42.9, "b": 45.7}]}
```

**Waffle chart `waffle`**: same as the donut chart, `rows: [{name, a}]`; 100 squares, 1 square = 1%.
```json
{"kind": "waffle", "title": "Where 2025 sales came from", "subtitle": "By category, 1 square = 1%", "unit": "k",
 "rows": [{"name": "Coffee", "a": 161.2}, {"name": "Tea", "a": 26.9}]}
```

**Bullet chart `bullet`**: `rows: [{name, a: actual, b: target}]`. Sorted by how much of the target was reached; bars below target are red. Works best with up to 8 rows.
```json
{"kind": "bullet", "title": "2025 sales vs target by store", "subtitle": "$ thousands",
 "rows": [{"name": "Main St", "a": 33.6, "b": 32}, {"name": "Tech Park", "a": 46.9, "b": 50}]}
```

**Calendar heatmap `calendar`**: `rows: [{name: date, a: value}]`, one row per day. Write dates as `2025-01-03` (year first); Excel date serial numbers also work. Only the year with the most data is drawn; several rows for the same day are added up.
```json
{"kind": "calendar", "title": "Daily sales in 2025", "subtitle": "Darker means a busier day", "unit": "",
 "rows": [{"name": "2025-01-01", "a": 5120}, {"name": "2025-01-02", "a": 4380}]}
```

**Month calendar heatmap `calendarMonths`**: same data as the calendar heatmap. Twelve small months make up the year (3×4 portrait, 6×2 landscape); the best day of the year is outlined, and the lowest and highest values are written at the top right.
```json
{"kind": "calendarMonths", "title": "Daily sales, month by month", "subtitle": "Outlined: the best day of the year", "unit": "",
 "rows": [{"name": "2025-01-01", "a": 5120}, {"name": "2025-01-02", "a": 4380}]}
```

**Image cards `imageCards`**: `rows: [{name, img: picture, sub: small caption (optional), a: main value, b: second value (optional)}]`. One card per item: the picture on top, then the name, main value, second value and a bar compared with the #1 item. Ranked by the main value, largest first; the top 3 ranks use the accent color. Works best with 8–12 cards; at most 24.
- `labelB` is the text before the second value, for example "vs last year". With `bPercent: true` the second value shows as a percentage: 0.061 becomes +6.1%.
- `imageRatio`: 1 is square (default), 0.75 landscape, 1.33 portrait. Pictures fill the frame and are cropped.
- `topN`: how many top ranks use the accent color, 3 by default. `sort: false` keeps the input order.
- **Pictures must be `data:image/jpeg;base64,...`** (png and webp work too). URLs and file paths are not accepted: URLs need the internet and break "Download PNG".
- If the user gives a folder of pictures, match file names to `name` and ask about any that don't match. Shrink each picture to 400 px on the long side, save as JPEG, then convert to base64 (about 20–40 KB each). Otherwise the page gets very large.
- Pictures embedded in Excel cells may not map reliably to rows. After matching, list which picture went with which row and ask the user to confirm.
- Items without a picture show "No image". Never fill in with an unrelated picture.
```json
{"kind": "imageCards", "title": "Best sellers in 2025", "subtitle": "Sales, $ thousands", "unit": "k", "labelB": "vs last year", "bPercent": true,
 "rows": [{"name": "Latte", "sub": "Coffee", "a": 53.0, "b": 0.061, "img": "data:image/jpeg;base64,/9j/4AAQ..."},
          {"name": "Croissant", "sub": "Bakery", "a": 11.8, "b": 0.050, "img": "data:image/jpeg;base64,/9j/4AAQ..."}]}
```

**Tile map `tileMap`**: `rows: [{name: region, a: value}]`. One tile per region in roughly the right place, with no borders and no internet needed. Knows the 50 US states plus DC ("California" or "CA") and China's 34 provincial regions ("Guangdong" or "GD", including Taiwan, Hong Kong and Macao). `region: "us"` or `"cn"` is optional; it is detected from the names. Names that don't match are left out; list them when you deliver. The landscape version lists the top 10 on the right.
```json
{"kind": "tileMap", "title": "Online orders cluster on the coasts", "subtitle": "2025 online orders by state, thousands", "unit": "k",
 "rows": [{"name": "CA", "a": 9.1}, {"name": "New York", "a": 7.4}, {"name": "TX", "a": 6.8}]}
```

**Scatter plot `scatter`**: `rows: [{name, a: x value, b: y value}]`, up to 300 points. `labelA` and `labelB` name the axes (with units). `highlight: ["Latte"]` colors a few points and grays out the rest. The dashed lines are the averages of each number (`average: false` hides them). With many points only the highlighted points and the highest, lowest, leftmost and rightmost get names. No trend line is drawn.
```json
{"kind": "scatter", "title": "Lattes sell most, pour-over least", "subtitle": "Price and cups sold per item, 2025", "labelA": "Price ($)", "labelB": "Cups sold (thousands)", "highlight": ["Latte"],
 "rows": [{"name": "Latte", "a": 22, "b": 24.1}, {"name": "Pour-over", "a": 32, "b": 2.9}]}
```

**Radar chart `radar`**: one row per measure; `series` names the items compared (up to 3): `rows: [{name: measure, v: [item 1 score, item 2 score]}]`, 3–8 measures. `max` is the full score (for example 100); without it the axis is rounded up from the data. With a single item, each score is written next to its measure.
```json
{"kind": "radar", "title": "Tech Park is bigger, Campus grows", "subtitle": "Each measure scored against the best of 6 stores (= 100)", "series": ["Tech Park", "Campus"], "max": 100,
 "rows": [{"name": "Sales", "v": [100, 54]}, {"name": "Growth", "v": [61, 97]}, {"name": "Delivery share", "v": [62, 100]}]}
```

**Table `table`**: `columns` names the columns (up to 5); `rows: [{name, v: [one value per column]}]`. `formats` sets each column: `"num"` (default), `"pct"` (0.938 shows as 93.8%), `"delta"` (a change: 0.039 shows as ▲ 3.9%, up in the accent color, down in red). `units` adds a unit after each column's numbers. Sorted by the first column, largest first (`sort: 2` sorts by the third column, `sort: false` keeps the order). The first column gets a small bar (`bar: false` removes it, `bar: 2` puts it on the third column). The number of rows depends on the canvas height: about 15 in a 3:4 image.
```json
{"kind": "table", "title": "Store scorecard, 2025", "columns": ["Sales", "vs last year", "Cups", "Target hit"],
 "formats": ["num", "delta", "num", "pct"], "units": ["k", "", "k", ""],
 "rows": [{"name": "Tech Park", "v": [46.9, 0.039, 22.5, 0.938]}, {"name": "Riverside", "v": [45.7, 0.063, 21.9, 1.039]}]}
```

**Dashboard `dashboard`**: puts 2–7 charts on one page. Each item in `panels` is a chart, written exactly like the single charts above (`theme`, `file`, `sign` and `lang` go on the dashboard only, or on `DOC` when it sits in `DOC.charts`).
- When the first panel is KPI cards, it takes the whole top row; leave out its `title` in that case.
- The other charts: 2–3 per row in 16:9, up to two rows; one per row, stacked down, in the long phone image.
- Panels are smaller than single charts, so keep each `title` short (about 20 characters) and put units in the `subtitle`.
- At most 1 row of KPI cards + 6 charts per page. If you need more, split into two dashboards.
- Two downloads: 16:9 (slides, screens) and a long phone image.
```json
{"kind": "dashboard", "title": "2025 coffee shop dashboard", "subtitle": "6 stores · data through 2025-12-31", "file": "dashboard",
 "panels": [
  {"kind": "kpi", "labelB": "vs last year", "rows": [{"name": "Sales ($)", "a": 215.3, "b": 204.6, "unit": "k"}, {"name": "Repeat rate", "a": 38.5, "b": 35.1, "unit": "%"}]},
  {"kind": "column", "title": "December sold the most", "subtitle": "Monthly sales, $k", "rows": [{"name": "Jan", "a": 15.2}, {"name": "Feb", "a": 12.1}]},
  {"kind": "bar", "title": "Tech Park is #1", "subtitle": "Sales by store, $k", "rows": [{"name": "Main St", "a": 33.6}, {"name": "Tech Park", "a": 46.9}]},
  {"kind": "donut", "title": "Coffee is 3/4 of sales", "subtitle": "Sales by category", "unit": "k", "rows": [{"name": "Coffee", "a": 161.2}, {"name": "Tea", "a": 26.9}]}
 ]}
```


## 5. Create the page

1. **Let your data script write `DOC` into the page**; don't type the numbers by hand. Copy `template.html` from this skill's folder (the folder this SKILL.md is in):
```python
import json, pathlib
tpl = pathlib.Path("<skill folder>/template.html").read_text(encoding="utf-8")
DOC = {"mode": "report", "title": "...", "sections": [...]}             # every number comes from variables computed above
html = tpl.replace("var DOC = {};", "var DOC = " + json.dumps(DOC, ensure_ascii=False) + ";", 1)
pathlib.Path("report.html").write_text(html, encoding="utf-8")
```
   Name the file after the output, for example `charts.html`, `report.html` or `slides.html`, in the user's working folder.
2. Only if you can't run code: copy the file (for example `cp <skill folder>/template.html report.html`) and replace the line `var DOC = {};` with your object. Either way, don't change anything else in the template, and don't trim the drawing code.
   - If you can't run commands, read `template.html` and write it out unchanged except for that line.
   - If `template.html` is missing (for example only this file was shared), get it from https://github.com/NeoSunxz/ai-data-report-skill/blob/main/skills/data-report/template.html or ask the user for it. Don't write your own drawing code.
3. **If the user wanted images, export them as PNG files** next to the page, one per chart in the size chosen in section 3. Canvas ids: `chart-<n>-16x9`, `chart-<n>-3x4`, `chart-<n>-chart` (transparent), `chart-<n>-long` (phone-length dashboard). With Python and Playwright:
```python
# Export PNGs from the page (needs Playwright: pip install playwright && playwright install chromium)
import base64, pathlib
from playwright.sync_api import sync_playwright
page_file, shots = "charts.html", [("chart-1-16x9", "growth-by-store.png")]   # (canvas id, file name)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(pathlib.Path(page_file).resolve().as_uri()); pg.wait_for_timeout(1000)
    for cid, name in shots:
        url = pg.evaluate("id => document.getElementById(id).toDataURL('image/png')", cid)
        pathlib.Path(name).write_bytes(base64.b64decode(url.split(",")[1]))
    b.close()
```
   Then open the PNG for the user. If there's no way to run a headless browser, say so, open the page instead, and tell the user which download button to click.
4. Otherwise, if you can run commands, open the page for the user: `open report.html` (macOS), `start report.html` (Windows), `xdg-open report.html` (Linux).
5. Tell the user how to use it:
   - `charts`: open in Chrome or Edge; every chart has download buttons; the buttons at the top switch the theme.
   - `report`: open in a browser; "Print / save as PDF" at the top makes an A4 PDF.
   - `slides`: open in a browser; ← → or click to move, F for full screen; print to save as PDF, one slide per page.
6. If you can run a headless browser (such as Playwright), check the result yourself before handing it over: open the page, look at every chart (and every slide), and fix text that is cut off or crowded. You can also export PNGs by calling `toDataURL('image/png')` on each `<canvas>`; ids are `chart-<n>-3x4`, `chart-<n>-16x9`, `chart-<n>-chart` (transparent) and `chart-<n>-long` in `charts` mode, and `chart-<n>` in reports and slides.

### When image or PDF export is blocked

If exporting PNG or PDF fails (for example a sandbox won't let you start a browser), go in this order:

1. Use the Playwright method above.
2. If a sandbox blocks it, ask the user once for permission to run it outside the sandbox; say it stays offline and installs nothing.
3. If they say no, or it still fails, hand over the page, tell the user which button to click (download PNG / Print, save as PDF), and say why it couldn't be exported automatically.

**Never redraw the charts with another library** (matplotlib, ECharts, Excel charts and so on) **and never rewrite the report as a document without charts** (Word, Markdown, a text-only PDF): the chart styles, colors and number rules would be lost.

**Make PDFs only through a browser**: the user clicks "Print / save as PDF" at the top of the page, or you open the page with Playwright, wait 1 second for the charts to draw, then `pg.emulate_media(media="print")` and `pg.pdf(path="report.pdf", format="A4", print_background=True)`. Tools that don't run the page's JavaScript (WeasyPrint, wkhtmltopdf / pdfkit, xhtml2pdf, pandoc, Word or LibreOffice conversion) produce PDFs with blank chart areas. Don't make a PDF unless the user asks; the report page already prints to A4.

## 6. Working with other slide skills and templates

Other presentation skills (such as frontend-slides) and the user's own templates own the look of their decks. **Don't restyle their slides, don't add your CSS, fonts or navigation to their deck, and don't replace their layout.** Your job there is the content: the storyline (section 3) and the charts, drawn in the deck's colors.

1. **Agree who builds the deck.** If another slide skill is in use, give it the storyline as a list: for each slide, the headline (the finding), the chart, and 2–3 points. Let it build the slides, then add the charts as below.
2. **Read the deck's colors and font.** From the deck's CSS variables or the template's theme, take: the background behind the chart (`card`), the main text color (`ink`), a muted text color (`ink2`), the accent color (`acc`), up to 6 other colors for categories (`cats`) and the body font (`font`). Use hex colors like `#1A1A2E`. Only `card`, `ink` and `acc` are required; the rest are worked out from them.
3. **HTML decks: embed the charts.** Copy the drawing code from `template.html`, everything from `/* ===== CHARTS_JS START ===== */` to `/* ===== CHARTS_JS END ===== */`, into one `<script>` near the end of their file, unchanged. Put a canvas where each chart goes, then add the loader once:
```html
<canvas class="xc-chart" width="1950" height="1050" style="width:100%;height:auto"
  data-chart='{"kind":"line","series":["Dine-in","Delivery"],"rows":[{"name":"Q1","v":[21,10]},{"name":"Q2","v":[22,14]}]}'></canvas>

<script>/* drawing code from template.html, CHARTS_JS START to CHARTS_JS END */</script>
<script>
(function () {
  var theme = { card: "#14121F", ink: "#F4F1EA", ink2: "#9C97B0", acc: "#FF6B4A", font: "Georgia" };
  function drawAll() {
    Array.prototype.forEach.call(document.querySelectorAll("canvas.xc-chart"), function (cv) {
      var c = JSON.parse(cv.getAttribute("data-chart"));
      Charts[c.kind](cv.getContext("2d"), c, { bare: true, theme: c.theme || theme, lang: c.lang || "en", fontScale: 1.3 });
    });
  }
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(drawAll);
})();
</script>
```
   - `bare: true` draws only the chart: no title (the slide has its headline), no card, a transparent background.
   - Size the canvas at about 1.5× the space it takes on the slide, in the same proportions, so it stays sharp. `fontScale` makes the chart's text bigger for slides (1.3) or leaves it as is for documents (1).
   - The drawing code adds one global, `Charts`. If the deck already has a global with that name, tell the user instead of renaming things in their file.
   - Escape `'` inside `data-chart` as `&#39;`.
4. **PowerPoint, Keynote, Google Slides or any other tool**: make a `charts` page with `DOC.theme` set to the template's colors, and use the "chart only" transparent PNGs. They drop onto any slide background.
5. **Reports in someone else's format**: the same two routes work: embedded canvases with `fontScale: 1` for HTML, transparent PNGs for documents.

## 7. Check, then explain what you delivered

Before delivering, reread every sentence you wrote (titles, points, summaries, the final message) and fix any that break these rules:

- **Every number must be in the data or calculated from it.** No industry averages, benchmarks or "typical" figures unless the user gave them.
- **Moving together is not a cause.** Write "sales and temperature rose together", not "sales rose because of the heat". Give a reason only if the user or the data states it, and say where it came from.
- **Different numbers of days: compare daily averages.** Months have different lengths (28 days in February, 31 in July) and leap years add a day (February 2024 had 29). Convert to per-day figures before saying which month did better or worse. February 2025 grew only 1.7% over February 2024 in total, but 5.4% per day.
- **Small amounts of data get careful words.** With fewer than about 6 time points, or groups of fewer than about 30 rows, say "only N months so far" and don't call it a trend. One unusual day is "one day", not a pattern.
- **Percentages of small numbers show the counts too**: "up 50% (from 4 to 6)".
- **Reconcile with your script.** Check every number in titles, points, summaries and your final message against what the charts will show, including what the page calculates: the change on KPI cards is `(a − b) ÷ b` and the % at the right of a dumbbell chart is `(b − a) ÷ a`, both to one decimal place. Also check that each number is attached to the right item ("November was highest": is it really November?): for "first", "second", "the two biggest" and similar, take the name and the number from the same row of your script's sorted data instead of pairing them from memory. Fix any mismatch and check again.
- **No chart repeats another.** If two charts show the same values, drop one. Numbers derived from each other (a total and an average, a value and its % change) must agree.
- **No vague claims.** Replace "significantly", "sharply", "much better" with the number. If there is no number for it, delete the sentence.
- **Don't forecast** unless the user asks; if they do, label it as a projection and say how it was worked out.
- **Recommendations need a basis.** When the user asks for recommendations, tie each one to a finding in the report and phrase it as something to consider. No invented numbers and no predicted effects ("should lift sales 10%").
- **Red-flag words.** Search what you wrote for: significant(ly), sharply, dramatically, because, due to, driven by, caused, will, expected, forecast, industry average, typical, trend. Recheck every hit against the rules above; keep it only if the data backs it.

Give the user a table with one row per chart (for a dashboard, one per panel; for a report or deck, one per section): the headline, the question it answers, the columns used, and how they were summarized ("raw data" if not summarized). Also list anything cut or merged (rows over the limit, categories merged into "Other") and anything cleaned up in step 1.

End with one or two sentences on what stands out, based only on what the data shows ("December had the highest sales, $24k", "Delivery cups doubled over the year"). Don't guess at reasons.

Then give a one-line verdict (never "Ready to use" unless every number reconciled): **"Ready to use"**, or **"Ready to use, but note: ..."** with what the reader must know (a missing month, categories merged into "Other", a small sample, a number you couldn't verify).

Finish by offering next steps in one line. After a single chart: one specific extra chart, plus another size if it would help. Otherwise: change a chart / switch the colors / turn it into another output (slides, a report, a dashboard or a PDF).

## 8. Limits

- Text uses the fonts on the computer (or the deck's font when given), so letter shapes differ slightly between machines.
- Each chart has a row limit (see the chart formats); anything beyond it isn't drawn. With a lot of data, summarize or filter first.
- Hovering over a chart shows its values, but there is no clicking or filtering, and pages must be regenerated when the data changes. For a dashboard that filters and refreshes on its own, use a dedicated reporting tool.
- Values show at most one decimal place (two for KPI values under 10), with thousands separators above 1,000.
- Image card pictures are stored inside the page, so many or large pictures make it big. Shrink them first (section 4).
- Built-in slides are deliberately plain: one headline, one chart, a few points. For animated or highly designed decks, use a dedicated presentation skill and section 6.
