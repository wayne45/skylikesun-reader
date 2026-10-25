繁體中文 | [English](README.en.md)

# skylikesun 閱讀器

一個純靜態網頁，用來管理 https://skylikesun.blogspot.com 的文章：標記已讀、略過，或放進自訂分類。手機和電腦都能用，進度透過私人 GitHub Gist 在裝置之間同步。

## 檔案

| 檔案 | 用途 |
| --- | --- |
| `index.html` | 閱讀器網頁（不需要 build） |
| `posts.json` | 文章清單（標題、日期、連結、原作者標籤） |
| `fetch_posts.py` | 抓取 Blogger feed，把新文章合併進 `posts.json` |
| `.github/workflows/update-posts.yml` | 每天兩次（台灣時間 11:50 和 23:50）執行 `fetch_posts.py`，有變動就自動 commit |

## 本機執行

```bash
python3 fetch_posts.py            # 選用：更新 posts.json
python3 -m http.server 8000       # 然後開啟 http://localhost:8000
```

請用 HTTP 開啟，`file://` 無法載入 `posts.json`。

## 同步設定（GitHub Gist）

進度會先存在瀏覽器的 localStorage，所以離線也能用。要在多台裝置間共用，網頁可以把進度同步到你自己 GitHub 帳號下的**私人（secret）Gist**。Gist 裡只有一個檔案 `state.json`，內容是文章 id、狀態、分類和時間戳，不含文章內容。

### 1. 建立只有 `gist` 權限的 token

GitHub CLI 無法建立 personal access token，請用網頁建立。下面的連結已預先選好權限和名稱：

```bash
open "https://github.com/settings/tokens/new?scopes=gist&description=skylikesun-reader"
```

1. 選擇有效期限（token 過期後同步會失敗，需要重新建立）。
2. 確認**只勾選 `gist`**。
3. 按 **Generate token**，複製 `ghp_...` 開頭的 token。GitHub 只會顯示一次。

### 2. 在閱讀器使用

在每台裝置（電腦、手機）上：

1. 開啟閱讀器，點 **⚙︎**。
2. 把 token 貼到 **GitHub token** 欄位。
3. 按**立即同步**。

第一次同步會尋找描述為 `skylikesun-reader state` 的 Gist，找不到就自動建立一個私人 Gist。其他裝置會自動找到同一個。你可以在 https://gist.github.com 看到它。

之後每次修改後約 3 秒，以及每次回到這個分頁時，都會自動同步。**⚙︎** 旁邊會顯示同步狀態。

### 注意事項

- token 只存在該裝置的 localStorage，只會傳送給 `api.github.com`。請不要 commit 它。
- 設定裡的**移除 token** 只會從該裝置移除。要完全撤銷，請到 https://github.com/settings/tokens 刪除。
- 兩台裝置以每篇文章的時間戳合併，兩邊離線時各自的修改都會保留。
- 沒有 token 也能在本機使用。可用設定裡的**匯出 / 匯入**手動備份或搬移 `state.json`。

## 使用方式

- 點狀態按鈕依序切換：未讀 → 已讀 → 略過。手機上向右滑是已讀，向左滑是略過。
- 🏷 可以替文章指定分類。分類管理在 **⚙︎ → 管理分類**。
- 篩選條件有狀態、原作者標籤、自訂分類、年月和標題搜尋。列表上方的批次列可以把狀態或分類套用到目前篩選出的所有文章。
- **⚙︎ → 點開文章時自動標為已讀**：開啟文章時直接標為已讀。沒開的話，回到網頁時會詢問。
