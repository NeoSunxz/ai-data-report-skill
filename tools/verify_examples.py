# -*- coding: utf-8 -*-
"""校验示例：图里的数据、正文里写的数字、KPI 三者是否自洽。
   直接读 DOC，不硬编码任何期望值。"""
import re, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent / "examples"
ok = True

def fail(msg):
    global ok
    ok = False
    print("   FAIL " + msg)

def check(name):
    print("\n" + "=" * 66)
    print(name)
    print("=" * 66)
    h = (root / name).read_text(encoding="utf-8")
    d = json.loads(re.search(r"var DOC = (\{.*?\n\});", h, re.S).group(1))
    secs = d["sections"]
    num = lambda s: float(re.sub(r"[^\d.\-]", "", s)) if re.search(r"\d", s) else None

    kpi = next((s for s in secs if s["kind"] == "kpi"), None)
    col = next((s for s in secs if s["kind"] == "column"), None)
    bar = next((s for s in secs if s["kind"] == "bar" and "a" in s["rows"][0]), None)
    line = next((s for s in secs if s["kind"] == "line"), None)
    don = next((s for s in secs if s["kind"] == "donut"), None)
    wf = next((s for s in secs if s["kind"] == "waterfall"), None)

    # 1. 销售额：KPI / 月度 / 门店 / 品类 必须一致
    sales_kpi = next(r["a"] for r in kpi["rows"] if "Sales" in r["name"])
    groups = {
        "monthly": sum(r["a"] for r in col["rows"]) if col else None,
        "stores": sum(r["a"] for r in bar["rows"]) if bar else None,
        "categories": sum(r["a"] for r in don["rows"]) if don else None,
    }
    print("销售额 KPI = %.1f" % sales_kpi)
    for k, v in groups.items():
        if v is None:
            continue
        if abs(v - sales_kpi) > 0.15:
            fail("%s 合计 %.1f ≠ KPI %.1f（差 %+.1f）" % (k, v, sales_kpi, v - sales_kpi))
        else:
            print("   OK %s 合计 %.1f" % (k, v))

    # 2. 杯数：各渠道逐月相加 = KPI
    cups_kpi = next(r["a"] for r in kpi["rows"] if "Cups" in r["name"])
    if line:
        n_series = len(line["rows"][0]["v"])
        tot = sum(sum(r["v"]) for r in line["rows"])
        print("杯数 KPI = %.1fk，折线图 %d 条线逐月相加 = %.1fk" % (cups_kpi, n_series, tot))
        if abs(tot - cups_kpi) > 0.15:
            fail("折线合计 %.1f ≠ KPI %.1f（差 %+.1f）" % (tot, cups_kpi, tot - cups_kpi))
        else:
            print("   OK 折线合计与 KPI 一致")

    # 3. 平均单价 = 销售额 / 杯数
    row = next((r for r in kpi["rows"] if "price" in r["name"].lower() or "Avg" in r["name"]), None)
    if row:
        derived = sales_kpi * 1000 / (cups_kpi * 1000)
        print("平均每杯 KPI=%.2f，销售额÷杯数=%.2f" % (row["a"], derived))
        if abs(row["a"] - derived) > 0.02:
            fail("平均每杯 %.2f ≠ 算出来的 %.2f" % (row["a"], derived))
        else:
            print("   OK 平均每杯由销售额÷杯数得出")
        if "ticket" in row["name"].lower():
            fail("用了 average ticket，但数据里没有订单数")

    # 4. 正文里出现的每个百分数，要能在数据里找到出处
    allpts = []
    for s in secs:
        allpts += s.get("points") or []
    allpts += d.get("summary") or []
    for p in allpts:
        for m in re.finditer(r"(\d+(?:\.\d+)?)\s*%", p):
            v = float(m.group(1))
            lo, hi = v - 0.6, v + 0.6
            cands = []
            if bar and "top 2" in p:
                top2 = sum(sorted((r["a"] for r in bar["rows"]), reverse=True)[:2])
                cands.append(top2 / sales_kpi * 100)
            if kpi:
                for r in kpi["rows"]:
                    if isinstance(r.get("b"), (int, float)) and r["b"]:
                        cands.append((r["a"] - r["b"]) / abs(r["b"]) * 100)
            if line and ("of cups" in p or "share" in p.lower()):
                # 首月和末月各渠道的占比都要算
                for ri in (0, -1):
                    row_i = line["rows"][ri]
                    tot_m = sum(row_i["v"])
                    if tot_m:
                        for v in row_i["v"]:
                            cands.append(v / tot_m * 100)
            if not cands:
                print("   ?  百分数 %s%% 无法自动核对：%s" % (m.group(1), p[:56]))
            elif not any(lo <= c <= hi for c in cands):
                fail("百分数 %s%% 在数据里找不到出处：%s" % (m.group(1), p[:60]))

    # 5. 利润桥：终点 = 起点 + 各项之和
    if wf:
        cum = wf["rows"][0]["a"] + sum(r["a"] for r in wf["rows"][1:])
        print("利润桥 终点 = %.1f" % cum)
        for p in wf.get("points") or []:
            m = re.search(r"ended at \$([\d.]+)k", p)
            if m and abs(float(m.group(1)) - cum) > 0.15:
                fail("正文写 %.1f，利润桥算出来 %.1f" % (float(m.group(1)), cum))
            m = re.search(r"up \$([\d.]+)k", p)
            if m:
                delta = cum - wf["rows"][0]["a"]
                if abs(float(m.group(1)) - delta) > 0.15:
                    fail("正文写涨 %.1f，实际 %+.1f" % (float(m.group(1)), delta))
        print("   OK 终点与正文一致" if ok else "")

    # 6. 红词
    blob = json.dumps({k: v for k, v in d.items() if k != "notes"}, ensure_ascii=False).lower()
    for w in ["driven by", "because", "due to", "caused", "significant", "sharply", "dramatically"]:
        if w in blob:
            fail("出现因果/夸张词：%r" % w)

for n in ["report.html", "slides.html"]:
    check(n)

print("\n" + ("全部通过 OK" if ok else "有问题 FAIL"))
