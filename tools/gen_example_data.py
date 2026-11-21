# -*- coding: utf-8 -*-
"""生成报告/幻灯片的示例数据。所有数字由本脚本算出，写进 DOC，
   保证 KPI、月度、门店、渠道、品类、利润桥互相自洽。"""
import json, pathlib, re

# ---------- 基础数据（唯一的来源） ----------
STORES = ["Tech Park", "Riverside", "Main St", "Airport", "Old Town", "Campus"]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# 2025 每月销售额（千元），12 月最高、2 月最低
SALES_M2025 = [15.2, 12.1, 16.8, 17.5, 18.9, 20.4, 22.6, 23.1, 19.7, 18.2, 19.4, 21.4]
# 2024 每月销售额，用于算同比
SALES_M2024 = [14.6, 11.8, 15.9, 16.8, 17.9, 19.4, 21.5, 21.9, 18.6, 17.4, 18.5, 20.3]

SALES_2025 = round(sum(SALES_M2025), 1)   # 227.9 → 用它做所有分母
SALES_2024 = round(sum(SALES_M2024), 1)
CUPS_2025 = 65200.0      # 全年杯数
CUPS_2024 = 60800.0
REPEAT_2025, REPEAT_2024 = 38.5, 35.1

# 每杯均价：由销售额 ÷ 杯数算出，不手填
AVG_2025 = SALES_2025 * 1000 / CUPS_2025
AVG_2024 = SALES_2024 * 1000 / CUPS_2024

# 门店占当月比例（6 家，加起来 = 1）
STORE_W = [0.215, 0.209, 0.155, 0.171, 0.121, 0.129]
assert abs(sum(STORE_W) - 1) < 1e-9

# 渠道：每月杯数占比（dine-in, delivery, pickup），三者相加 = 1
CH_DINE = [0.47,0.36,0.43,0.44,0.45,0.44,0.43,0.42,0.41,0.40,0.39,0.38]
CH_DLV  = [0.20,0.21,0.24,0.25,0.26,0.28,0.29,0.30,0.31,0.32,0.33,0.35]
CH_PICK = [1 - a - b for a, b in zip(CH_DINE, CH_DLV)]

# 品类：占销售额比例，相加 = 1
CAT_W = {"Coffee": 0.703, "Tea": 0.125, "Bakery": 0.092, "Desserts": 0.080}
assert abs(sum(CAT_W.values()) - 1) < 1e-9

# ---------- 计算 ----------
def pct(a, b): return (a - b) / abs(b) * 100

store_sales = {s: round(SALES_2025 * w, 1) for s, w in zip(STORES, STORE_W)}
# 抹平四舍五入误差
diff = round(SALES_2025 - sum(store_sales.values()), 1)
store_sales[STORES[0]] = round(store_sales[STORES[0]] + diff, 1)
assert abs(sum(store_sales.values()) - SALES_2025) < 0.05

# 每月杯数按当月销售额比例分配
scales = [v / SALES_2025 for v in SALES_M2025]
cups_m = [round(CUPS_2025 * x, 0) for x in scales]
cups_m[-1] += CUPS_2025 - sum(cups_m)
assert abs(sum(cups_m) - CUPS_2025) < 1

# 每月按渠道拆三份，用最大余数法凑整到 0.1k，保证每月三份相加正好等于当月杯数
def split3(total, w):
    """把 total 按权重 w 拆成 3 个 0.1k 的整数单位，加起来正好 = total"""
    units = round(total * 10)
    raw = [units * x for x in w]
    base = [int(x) for x in raw]
    rest = units - sum(base)
    order = sorted(range(3), key=lambda i: raw[i] - base[i], reverse=True)
    for i in order[:rest]:
        base[i] += 1
    return [u / 10 for u in base]

dine, dlv, pick = [], [], []
for c, w in zip(cups_m, zip(CH_DINE, CH_DLV, CH_PICK)):
    a, b, d = split3(c / 1000, w)
    dine.append(a); dlv.append(b); pick.append(d)

# 逐月各自取整会累积漂移（每月最多 0.05k），让最后一个月吸收掉，
# 保证「三个渠道加起来 = 全年杯数」这条在图上也算得对
drift = round(CUPS_2025 / 1000 - (sum(dine) + sum(dlv) + sum(pick)), 1)
if drift:
    pick[-1] = round(pick[-1] + drift, 1)

TOTAL_CH = sum(dine) + sum(dlv) + sum(pick)
assert abs(TOTAL_CH - CUPS_2025 / 1000) < 0.05, (TOTAL_CH, CUPS_2025 / 1000)

# 每月三个渠道之和必须等于当月杯数（最后一个月除外，它吸收了全局漂移）
for i, c in enumerate(cups_m[:-1]):
    s = dine[i] + dlv[i] + pick[i]
    assert abs(s - c / 1000) < 0.05, ("month %d" % (i + 1), s, c / 1000)

cat_sales = {k: round(SALES_2025 * w, 1) for k, w in CAT_W.items()}
cdiff = round(SALES_2025 - sum(cat_sales.values()), 1)
cat_sales["Coffee"] = round(cat_sales["Coffee"] + cdiff, 1)

top2 = sum(sorted(store_sales.values(), reverse=True)[:2])
top2_share = top2 / SALES_2025 * 100

# 利润桥
PROFIT_2024 = 28.5
sales_up = round(SALES_2025 - SALES_2024, 1)
wf = [("2024 profit", PROFIT_2024), ("Sales up", sales_up), ("Beans", -4.8),
      ("Rent", -2.1), ("Staff", -3.4), ("Delivery fees", -1.9), ("New menu", 3.2)]
PROFIT_2025 = round(sum(v for _, v in wf), 1)
neg_total = round(sum(v for _, v in wf if v < 0), 1)

# ---------- 校验 ----------
print("SALES_2025 = %.1f   (KPI / monthly / stores / categories 必须一致)" % SALES_2025)
print("  sum monthly  = %.1f" % sum(SALES_M2025))
print("  sum stores   = %.1f" % sum(store_sales.values()))
print("  sum categories = %.1f" % sum(cat_sales.values()))
print("CUPS_2025 = %.0f" % CUPS_2025)
print("  sum dine+dlv+pick = %.1f (= %.1fk)" % ((sum(dine)+sum(dlv)+sum(pick))*1000, sum(dine)+sum(dlv)+sum(pick)))
print("AVG price/cup = %.2f (2025)  %.2f (2024)" % (AVG_2025, AVG_2024))
print("top2 share = %.1f%%" % top2_share)
print("profit 2025 = %.1f, change = %+.1f" % (PROFIT_2025, PROFIT_2025 - PROFIT_2024))

DOC = {
 "title": "2025 coffee shop review",
 "subtitle": "Sales, stores and channels across 6 stores",
 "author": "NeoSun",
 "date": "2026-01-15",
 "lang": "en",
 "summary": [
   "Sales grew %.1f%% to $%.1fk from %.1f%% more cups sold" % (pct(SALES_2025, SALES_2024), SALES_2025, pct(CUPS_2025, CUPS_2024)),
   "Delivery went from %.1fk to %.1fk cups a month over the year" % (dlv[0], dlv[-1]),
   "December was the best month; Tech Park is the top store"
 ],
 "notes": [
   "Made-up coffee shop data for 6 stores, 2025 vs 2024",
   "Sales are summed by month, by store and by category; all three add up to $%.1fk" % SALES_2025,
   "Average price per cup is sales divided by cups sold, not average order value",
   "Shares are rounded so they add up to 100%%"
 ],
 "mode": "report",
 "sections": [
  {"kind": "kpi",
   "title": "Sales grew %.1f%%, but the average price per cup fell" % pct(SALES_2025, SALES_2024),
   "subtitle": "2025 vs 2024", "labelB": "vs last year",
   "rows": [
     {"name": "Sales ($)", "a": SALES_2025, "b": SALES_2024, "unit": "k"},
     {"name": "Cups sold", "a": round(CUPS_2025/1000, 1), "b": round(CUPS_2024/1000, 1), "unit": "k"},
     {"name": "Avg price / cup ($)", "a": round(AVG_2025, 2), "b": round(AVG_2024, 2), "unit": ""},
     {"name": "Repeat rate", "a": REPEAT_2025, "b": REPEAT_2024, "unit": "%"}
   ],
   "points": [
     "Cups sold rose %.1f%%, more than sales" % pct(CUPS_2025, CUPS_2024),
     "Average price per cup fell from $%.2f to $%.2f" % (AVG_2024, AVG_2025),
     "Repeat rate up %.1f points" % (REPEAT_2025 - REPEAT_2024)
   ]},

  {"kind": "column", "title": "December was the best month",
   "subtitle": "Monthly sales, $ thousands", "highlight": "Dec",
   "rows": [{"name": m, "a": v} for m, v in zip(MONTHS, SALES_M2025)],
   "points": [
     "$%.1fk in December, the highest of the year" % SALES_M2025[-1],
     "%s was the low point at $%.1fk" % (MONTHS[SALES_M2025.index(min(SALES_M2025))], min(SALES_M2025)),
     "The 12 months add up to $%.1fk" % SALES_2025
   ]},

  {"kind": "bar", "title": "Tech Park and Riverside lead",
   "subtitle": "2025 sales by store, $ thousands",
   "rows": [{"name": s, "a": v} for s, v in sorted(store_sales.items(), key=lambda x: -x[1])],
   "points": [
     "The top 2 stores bring in %.0f%% of sales" % top2_share,
     "All 6 stores add up to $%.1fk" % SALES_2025
   ]},

  {"kind": "line", "title": "Delivery is catching up with dine-in",
   "subtitle": "Cups per month, thousands",
   "series": ["Dine-in", "Delivery", "Pickup"],
   "rows": [{"name": m, "v": [a, b, c]} for m, a, b, c in zip(MONTHS, dine, dlv, pick)],
   "points": [
     "Delivery cups rose from %.1fk to %.1fk a month" % (dlv[0], dlv[-1]),
     "Dine-in fell from %.0f%% to %.0f%% of cups sold" % (
       dine[0] / (dine[0] + dlv[0] + pick[0]) * 100,
       dine[-1] / (dine[-1] + dlv[-1] + pick[-1]) * 100)
   ]},

  {"kind": "donut", "title": "Coffee is about seven tenths of sales",
   "subtitle": "2025 sales by category", "unit": "k",
   "rows": [{"name": k, "a": v} for k, v in sorted(cat_sales.items(), key=lambda x: -x[1])]},

  {"kind": "waterfall", "title": "Why profit went up",
   "subtitle": "$ thousands", "endLabel": "2025 profit",
   "rows": [{"name": n, "a": v} for n, v in wf],
   "points": [
     "Higher sales added $%.1fk" % sales_up,
     "Beans, rent, staff and delivery fees took away $%.1fk" % abs(neg_total),
     "Profit ended at $%.1fk, up $%.1fk" % (PROFIT_2025, PROFIT_2025 - PROFIT_2024)
   ]}
 ]
}

# ---------- 写进两个示例 ----------
root = pathlib.Path(__file__).resolve().parent.parent
doc_json = json.dumps(DOC, ensure_ascii=False, indent=1)

for name in ["report.html", "slides.html"]:
    p = root / "examples" / name
    h = p.read_text(encoding="utf-8")
    h2 = re.sub(r"var DOC = \{.*?\n\};", "var DOC = " + doc_json + ";", h, count=1, flags=re.S)
    if h2 == h:
        print("!! DOC not replaced in", name); raise SystemExit(1)
    p.write_text(h2, encoding="utf-8")
    print(name, "DOC updated (%d bytes)" % len(doc_json))

# slides.json 供参考
(root / "examples" / "_doc_check.json").write_text(doc_json, encoding="utf-8")
