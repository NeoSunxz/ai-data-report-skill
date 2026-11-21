import pathlib, re
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent
examples = root / "examples"

with sync_playwright() as p:
    b = p.chromium.launch()
    for name in ["demo.html", "report.html", "slides.html"]:
        pg = b.new_page(viewport={"width": 1400, "height": 1000})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.on("console", lambda m: errs.append("console: " + m.text[:120]) if m.type == "error" else None)
        pg.goto((examples / name).resolve().as_uri())
        pg.wait_for_timeout(2200)
        r = pg.evaluate("""() => {
          const cvs=[...document.querySelectorAll('canvas')];
          let blank=0;
          cvs.forEach(c=>{try{
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            const s=new Set(); for(let i=0;i<d.length;i+=4*997) s.add(d[i]+','+d[i+1]+','+d[i+2]);
            if(s.size<=2) blank++;}catch(e){}});
          return {canvases:cvs.length, blank,
                  aria:cvs.filter(c=>c.getAttribute('aria-label')).length,
                  tables:document.querySelectorAll('details.dt').length,
                  overflowX:document.documentElement.scrollWidth>window.innerWidth};
        }""")
        pg.emulate_media(media="print")
        pg.wait_for_timeout(300)
        pdf = pg.pdf(print_background=True, prefer_css_page_size=True)
        sizes = set()
        for mb in re.findall(rb"/MediaBox\s*\[([^\]]+)\]", pdf):
            v = [float(x) for x in mb.split()]
            sizes.add("%.0fx%.0fmm" % ((v[2]-v[0])/72*25.4, (v[3]-v[1])/72*25.4))
        print("%-12s canvases=%-3d blank=%-2d aria=%-3d tables=%-2d overflow=%-5s pdf=%s %s" % (
            name, r["canvases"], r["blank"], r["aria"], r["tables"],
            r["overflowX"], ", ".join(sorted(sizes)), errs[:1] if errs else ""))
        pg.close()
    b.close()
