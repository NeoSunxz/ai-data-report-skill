import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "skills/data-report/template.html").read_text(encoding="utf-8")

for name in ["demo.html", "report.html", "slides.html"]:
    p = root / "examples" / name
    old = p.read_text(encoding="utf-8")
    m_old = re.search(r"<title>(.*?)</title>", old, re.S)
    m_new = re.search(r"<title>(.*?)</title>", tpl, re.S)
    title_old = m_old.group(1) if m_old else ""
    m_doc = re.search(r"var DOC = (\{.*?\n\});", old, re.S)
    if not m_doc:
        print("DOC not found in", name); sys.exit(1)
    doc = m_doc.group(1)
    new = tpl
    if title_old and m_new:
        new = new.replace("<title>" + m_new.group(1) + "</title>", "<title>" + title_old + "</title>", 1)
    new = new.replace("var DOC = {};", "var DOC = " + doc + ";", 1)
    p.write_text(new, encoding="utf-8")
    print(name, "rebuilt")
