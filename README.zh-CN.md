# Excel Charts Skill：用 AI 把 Excel / CSV 画成汇报用的图和看板

一个给 Claude Code 等 AI 助手用的 **Skill**：把 Excel、CSV 或粘贴的表格，画成能直接放进 PPT、汇报和手机里的图，也能拼成一页数据看板。不用安装，不联网：AI 生成一个 HTML 文件，用浏览器打开就能下载 PNG。

[English](README.md) · 作者 **NeoSun**

![看板示例](examples/dashboard-16x9.png)

## 能做什么

- **11 种图**：条形图、柱形图、折线图、环形图、堆积柱形图、瀑布图、数字卡、哑铃图、华夫饼图、子弹图、日历热力图。
- **看板**：一排数字卡加 2–6 张图拼成一页，可以下载 16:9 和手机长图两种。
- **每张图两个尺寸**：3:4 发手机，16:9 放 PPT。
- **3 套配色**：燕麦拿铁、雾霾蓝、深夜蓝（深色），一键切换。
- **不懂数据也能用**：AI 先问 3 个问题（给谁看、最关心哪几个数、和什么比）；表格里有多个 sheet、合并单元格、日期写成文字这类情况，它会先整理，再告诉你改了什么。
- **不编数**：图里的每个数都来自你的表格，汇总时会说明怎么算的。
- **中英文**：图里的文字可以是中文或英文（`lang: "zh"` / `"en"`）。示例图是英文的；用中文跟 AI 说，它就出中文图。

## 安装

**Claude Code**：把 `skills/excel-charts` 文件夹复制到 `~/.claude/skills/`（所有项目可用）或项目里的 `.claude/skills/`。

```bash
git clone https://github.com/NeoSunxz/excel-charts-skill.git
cp -r excel-charts-skill/skills/excel-charts ~/.claude/skills/
```

**其他 AI 助手**：把 `skills/excel-charts/SKILL.md` 当附件发给它，说「按这份说明做」。Skill 正文是英文，用中文跟 AI 说话就行，它会出中文图。

## 怎么用

1. 把表格交给 AI，说「画成图」或者「帮我做个看板」。
2. AI 会生成一个 HTML 文件，用 Chrome 或 Edge 打开。
3. 点每张图下面的按钮下载 PNG。

想先看效果，直接用浏览器打开 [`examples/demo.html`](examples/demo.html)，里面是虚构的咖啡店数据。

## 限制

- 出的是静态图片，不能点选、筛选；数据更新了要重新生成。
- 每种图有行数上限（比如条形图最多 15 行、折线图最多 4 条线），数据多时要先汇总。
- 图里的文字用电脑自带字体，不同电脑上字形略有差别。
- 网页只在你的浏览器里运行，数据不会上传。

## 开源协议

[MIT](LICENSE) © NeoSun
