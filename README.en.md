[繁體中文](README.md) | English

# skylikesun reader

A static web page for tracking which posts of https://skylikesun.blogspot.com you have read, skipped, or sorted into your own categories. Works on phone and desktop, and syncs progress between devices through a private GitHub Gist.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The reader page (no build step) |
| `posts.json` | Post list (title, date, link, original labels) |
| `fetch_posts.py` | Fetches the Blogger feed and merges new posts into `posts.json` |
| `.github/workflows/update-posts.yml` | Runs `fetch_posts.py` twice a day (11:50 and 23:50 Asia/Taipei) and commits changes |

## Run locally

```bash
python3 fetch_posts.py            # optional: refresh posts.json
python3 -m http.server 8000       # then open http://localhost:8000
```

Open it over HTTP; `file://` cannot load `posts.json`.

## Sync setup (GitHub Gist)

Your progress is stored in the browser (localStorage) first, so it works offline. To share it between devices, the page can sync it to a **secret Gist** in your own GitHub account. The Gist holds one file, `state.json`, with post ids, statuses, categories and timestamps. No article content.

### 1. Create a token with only the `gist` scope

GitHub CLI cannot create personal access tokens, so use the web page. This link pre-selects the scope and name:

```bash
open "https://github.com/settings/tokens/new?scopes=gist&description=skylikesun-reader"
```

1. Choose an expiration (when it expires, sync fails until you create a new token).
2. Make sure **only `gist`** is checked.
3. Click **Generate token** and copy the `ghp_...` value. GitHub shows it only once.

### 2. Use it in the reader

On each device (computer, phone):

1. Open the reader and tap **⚙︎**.
2. Paste the token into the **GitHub token** field.
3. Tap **立即同步** (Sync now).

The first sync looks for a Gist described `skylikesun-reader state` and creates a secret one if none exists. Other devices find the same Gist automatically. You can see it at https://gist.github.com.

After that, the page syncs by itself about 3 seconds after each change and whenever you return to the tab. The status next to **⚙︎** shows the sync state.

### Notes

- The token is stored only in that device's localStorage. It is never sent anywhere except `api.github.com`. Do not commit it.
- **移除 token** in the settings removes it from the device. To revoke it completely, delete it at https://github.com/settings/tokens.
- Two devices merge per post by the latest timestamp, so offline edits on both sides are kept.
- Without a token the page still works locally. Use **匯出 / 匯入** in the settings to back up or move `state.json` by hand.

## Using the reader

- Tap the status button to cycle unread → read → skipped. On a phone, swipe right for read and left for skipped.
- 🏷 assigns categories to a post. Manage categories under **⚙︎ → 管理分類**.
- Filters cover status, original label, custom category, month and title search. The bar above the list applies a status or category to every post in the current filter.
- **⚙︎ → 點開文章時自動標為已讀** marks a post read when you open it. Otherwise the page asks when you come back.
