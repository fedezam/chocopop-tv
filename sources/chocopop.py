import requests, json, logging
from bs4 import BeautifulSoup
from typing import List, Optional
from .base import StreamItem

FEED_URL = "https://www.chocopopflow.com/feeds/posts/default?alt=json&max-results=5000"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean_url(url):
    if not url: return None
    url = url.strip()
    return url.replace("http:", "https:", 1) if url.startswith("http:") else (url if url.startswith("https://") else None)

def scrape_chocopop() -> List[StreamItem]:
    logging.info("📡 Scraping...")
    resp = requests.get(FEED_URL, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    entries = data.get("feed", {}).get("entry", [])
    items = []
    
    for entry in entries:
        title = entry.get("title", {}).get("$t", "").strip()
        content = entry.get("content", {}).get("$t", "")
        if not content: continue
        
        soup = BeautifulSoup(content, "html.parser")
        sv = soup.find("div", class_="sv-data")
        if not sv: continue
        
        # 🔥 DETECCIÓN EXACTA: buscar 'Serie' en category[].term
        cats = [c.get("term") for c in entry.get("category", [])]
        if "Serie" in cats or "Series" in cats:
            item_type = "serie"
        elif "Evento" in cats or " vs " in title:
            item_type = "evento"
        else:
            item_type = "pelicula"
        
        thumbs = entry.get("media$thumbnail", [])
        poster = clean_url(thumbs[0].get("url")) if thumbs else None
        
        direct = clean_url(sv.get("data-stream"))
        seasons_raw = sv.get("data-seasons") if item_type == "serie" else None
        
        # Fallback: primer episodio como stream
        fallback = None
        if item_type == "serie" and seasons_raw and seasons_raw.strip() not in ["", "null", "[]"]:
            try:
                s = json.loads(seasons_raw)
                if isinstance(s, list) and s and s[0].get("eps"):
                    fallback = clean_url(s[0]["eps"][0].get("url"))
            except: pass
        
        final_stream = direct or fallback
        
        item = StreamItem(
            title=title, type=item_type, year=sv.get("data-year"),
            poster=poster, stream=final_stream, seasons=seasons_raw,
            genre=sv.get("data-genre"), source="chocopop"
        )
        # ✅ Incluir si tiene stream O es serie con seasons
        if item.stream or (item_type == "serie" and seasons_raw):
            items.append(item)
    
    logging.info(f"✅ {len(items)} items: {{'serie': {sum(1 for i in items if i.type=='serie')}}}")
    return items
