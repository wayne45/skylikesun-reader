#!/usr/bin/env python3
"""Fetch all posts from the Blogger feed into posts.json (merges with existing)."""
import json, sys, urllib.request
from pathlib import Path

BASE = "https://skylikesun.blogspot.com/feeds/posts/default?alt=json&max-results=150&start-index=%d"
OUT = Path(__file__).parent / "posts.json"

def fetch(start):
    with urllib.request.urlopen(BASE % start, timeout=60) as r:
        return json.load(r)["feed"]

def main():
    posts, start = {}, 1
    if OUT.exists():
        posts = {p["id"]: p for p in json.loads(OUT.read_text())}
    while True:
        feed = fetch(start)
        entries = feed.get("entry", [])
        if not entries:
            break
        for e in entries:
            link = next((l["href"] for l in e["link"] if l["rel"] == "alternate"), "")
            pid = e["id"]["$t"].split("post-")[-1]
            posts[pid] = {
                "id": pid,
                "title": e["title"]["$t"],
                "date": e["published"]["$t"][:10],
                "url": link,
                "labels": [c["term"] for c in e.get("category", [])],
            }
        print(f"fetched {start}..{start + len(entries) - 1}", file=sys.stderr)
        start += len(entries)
        if len(entries) < 150:
            break
    out = sorted(posts.values(), key=lambda p: p["date"], reverse=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(out)} posts -> {OUT}", file=sys.stderr)

main()
