import json, logging
from pathlib import Path
from datetime import datetime
from sources.chocopop import scrape_chocopop

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
OUTPUT_DIR = Path("data"); OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    catalog = [i.to_dict() for i in scrape_chocopop()]
    
    # Dedup
    seen = {}
    for item in catalog:
        key = f"{item['title'].lower().strip()}|{item.get('year','')}|{item.get('type','')}"
        if key not in seen: seen[key] = item
    final = sorted(seen.values(), key=lambda x: x["title"])
    now = datetime.now().isoformat()
    
    (OUTPUT_DIR / "chocopop_catalog.json").write_text(
        json.dumps({"updated": now, "total": len(final), "items": final}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Light version
    light = []
    for i in final:
        e = {k: i[k] for k in ["title","type","year","poster","stream","event_date","event_status"] if k in i}
        if i.get("seasons"): e["seasons"] = i["seasons"]
        light.append(e)
    (OUTPUT_DIR / "tvbox_index.json").write_text(
        json.dumps({"updated": now, "items": light}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    logging.info(f"🎉 Guardado: {len(final)} títulos")

if __name__ == "__main__":
    main()
