# 地理空間データ照会Webアプリ（JSTT社内検証用）

不動産情報ライブラリAPI（国土交通省）を、緯度経度を指定してブラウザから照会するツール。
`mlit-geospatial-mcp` と同一のロジックをVercel Serverless Functionとして移植したもの。

## 構成
- `public/index.html` … フロントエンド（緯度経度入力・API選択・結果表示）
- `api/query.py` … バックエンド（Vercel Python Serverless Function）
- `lib/` … `mlit-geospatial-mcp` のロジックをそのまま移植（request_processor / utils）
- `vercel.json` … Vercelビルド設定
- `requirements.txt` … Python依存パッケージ

## デプロイ手順（Vercel）

### 1. GitHubリポジトリを作成してpush
```
cd webapp
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/<あなたのアカウント>/jstt-geo-tool.git
git push -u origin main
```

### 2. Vercelでプロジェクトを作成
1. https://vercel.com にログイン（既存のJSTT Vercelアカウントでよい）
2. 「Add New」→「Project」→ 上記GitHubリポジトリを選択
3. Framework Presetは「Other」のままでOK（vercel.jsonが自動認識される）

### 3. 環境変数を設定（Settings → Environment Variables）
| 変数名 | 値 | 必須 |
|---|---|---|
| `LIBRARY_API_KEY` | 不動産情報ライブラリのAPIキー | 必須 |
| `ACCESS_TOKEN` | 任意の合言葉（社内共有用） | 推奨 |

`ACCESS_TOKEN` を設定した場合、フロントエンドの「アクセストークン」欄に同じ値を入力しないと照会できなくなる。
社外に誤ってURLが漏れた場合の簡易的な防止策として設定を推奨する（本格的な認証ではない点に留意）。

### 4. デプロイ
環境変数を保存後、「Deploy」をクリック。数分でURLが発行される。

## 動作確認
発行されたURLにアクセスし、緯度経度（例：43.06788044783783, 141.3541094042721）を入力して「照会する」をクリック。

## 注意事項
- α版データのため、開示資料への転記前に必ず一次資料と突き合わせること
- サーバーレス環境のためファイル保存機能（save_file）は無効化済み
- 不動産情報ライブラリAPIの利用規約の範囲内で利用すること（連続大量リクエスト禁止）
