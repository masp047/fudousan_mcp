# SHINTATSU 地理空間MCP連携（不動産情報照会Webアプリ）完成図書 v1.0

## 本書の位置づけ

本書は、日本信達株式会社（SHINTATSU／NIHON SHINTATSU）不動産営業部の「地理空間MCP連携（不動産情報照会Webアプリ）」プロジェクトについて、**将来にわたり一次情報源となる単一のマスタードキュメント**である。本書1ファイルから、システム仕様書／詳細仕様書／ソース管理台帳／実装管理（構築手順）／成果発表資料／コスト管理／次期エンハンス記録の各派生ドキュメントを生成できることをゴールとする。

- 各章に **【用途】タグ**（どの派生ドキュメント向けか）を付す。
- 事実と推定を峻別する。確定情報のみ断定し、推定は「推定」と明記する。不明は「未確認」と記す。
- 時刻はgitコミット時刻（一次情報）から抽出している（第18章）。

## マスク方針（MASK_POLICY）

- 機密値（APIキー・アクセストークン・秘密鍵）は**本書に非掲載**。保管先のみ記す。
- 具体的には `LIBRARY_API_KEY`（不動産情報ライブラリAPIキー）および `ACCESS_TOKEN`（社内共有パスフレーズ）の**値は本書に載せない**。いずれもVercelの環境変数（Sensitive）に格納。
- 公開URL・リポジトリURLは秘匿情報を含まないため掲載する。

## 目次

- 0. ドキュメント管理情報
- 1. エグゼクティブサマリ【発表資料】
- 2. システム概要・目的・背景・非機能要件【システム仕様書】
- 3. 用語集【全用途】
- 4. システム構成【仕様書/詳細】
- 5. 使用サービス・技術スタック・リソース一覧【ソース/実装/コスト】
- 6. 機能仕様【システム仕様書】
- 7. 詳細仕様【詳細仕様書】
- 8. ソースコード管理【ソース管理】
- 9. 実装・構築手順【実装管理】
- 10. 設定値・シークレット管理【セキュリティ】
- 11. 運用・保守マニュアル【運用】
- 12. テスト記録【品質】
- 13. コスト管理【コスト管理】
- 14. リスク・制約・既知の問題【運用/エンハンス】
- 15. 次期エンハンス候補【エンハンス記録】
- 16. 意思決定ログ【仕様書/発表】
- 17. つまづき・課題と解決【発表/実装】
- 18. 時刻付きタイムライン＆工数データ【コスト/発表】
- 19. 成果発表資料用サマリ／スライド構成案【発表資料】
- 20. 確定リソース値の索引【全用途】
- 付録Y. 運用手順書（README）全文
- 付録Z. ソースコード・設定ファイル全文

---

## 0. ドキュメント管理情報

| 項目 | 内容 |
| :--- | :--- |
| 文書名 | SHINTATSU 地理空間MCP連携（不動産情報照会Webアプリ）完成図書 |
| 版 | v1.0 |
| ステータス | 確定（デプロイ・動作確認済み。Phase3ダウンロード機能まで反映） |
| 記載基準日（AS_OF_DATE） | 2026-07-23 |
| 基準タイムゾーン | Asia/Tokyo（JST, UTC+9） |
| 作成主体 | 日本信達株式会社 不動産営業部（開発補助：Claude Code） |
| 関連リポジトリ | GitHub `masp047/fudousan_mcp`（ブランチ `claude/new-session-dxvd17`） |
| 本番URL | https://fudousanmcp.vercel.app |
| 更新ルール | 仕様変更・機能追加のたびに版を上げ、第16章（意思決定ログ）と第18章（タイムライン）へ追記する |

【用途】全用途

---

## 1. エグゼクティブサマリ　【発表資料】

**目的**：国土交通省「不動産情報ライブラリ」APIの30項目（地価・用途地域・ハザード・人口・周辺施設等）を、**緯度経度を入力するだけでブラウザから一括照会**できる社内ツールを、低コストで複数人が使える形で提供する。

**成果（確定）**：
- MLIT「地理空間MCP Server」（α版）のPythonロジックを、MCPプロトコル層を除去して **Vercel Python Serverless Function** に移植。
- **緯度経度1欄入力 → 30APIを並列照会 → 日本語ラベルの表で表示 → CSV/JSONダウンロード** までを実装。
- 日本信達（SHINTATSU）ブランドガイドに準拠したUI（正規ロゴ・カラー・書体）を適用。
- 本番URL **https://fudousanmcp.vercel.app** を発行、実データ取得を確認済み（例：小樽市祝津近傍で30項目中15項目にデータあり）。

**成果物**：GitHubリポジトリ（本番連携）、Vercel本番デプロイ、完成図書（本書）。

**工数（第18章に詳細）**：git確定の稼働アンカーで**下限 約2時間27分**（初回構築セッション）。デプロイ・ブラウザ検証・Phase3・本書作成を含む**現実的推定は約4〜6時間**（推定）。

**コスト**：Vercel Hobby/無料枠およびGitHub無料枠の範囲内で稼働（第13章）。追加の月額固定費は現時点で発生していない（推定：利用量が無料枠内のため）。

**横展開**：緯度経度さえあれば全国の物件評価・市場調査に利用可能。将来はGoogle Workspaceドメイン制限やxlsx出力等へ拡張余地あり（第15章）。

---

## 2. システム概要・目的・背景・非機能要件　【システム仕様書】

### 2.1 背景
- 不動産情報ライブラリ（国土交通省）が地価公示・用途地域・ハザード情報等をAPIで提供。
- MLITは「地理空間MCP Server」（α版、2026年2月公開）を公開。ただし**MCPはローカル実行専用**（Claude Desktop経由）で、社内の複数人がブラウザから使う用途には不向き。
- そこで、MCPの中核ロジック（`request_processor` / `utils`）を流用し、**Webアプリ（Vercel）として再実装**する方針とした。

### 2.2 目的
緯度経度を入力すると、不動産情報ライブラリの**30項目**を一括取得し、**非エンジニアが読める形**で表示・ダウンロードできること。社内複数人がURL共有で利用可能にすること。

### 2.3 適用範囲（SCOPE）
- 対象：不動産営業部の物件評価・市場調査における一次情報の下調べ（社内検証用α版）。
- 対象外：開示資料への無検証転記（α版データのため一次資料突合が前提）、一般公開、外部提供。

### 2.4 非機能要件
| 区分 | 要件・現状 |
| :--- | :--- |
| 可用性 | Vercelサーバーレス（従量・自動スケール）。SLAはVercelプランに準拠。 |
| 性能 | 30API並列実行。初回照会は概ね10〜30秒（外部API応答依存、推定）。 |
| セキュリティ | 簡易アクセストークン（合言葉）方式。APIキーはサーバー側環境変数に隔離。 |
| 保守性 | 単一HTML（フロント）＋薄いServerless（API）＋移植ロジック（lib）。日本語ラベル辞書で表示を制御。 |
| 国際化 | 日本語UI固定。 |
| データ鮮度 | α版データを含む。転記前に一次資料突合を必須とする旨をUIに明記。 |

【用途】システム仕様書

---

## 3. 用語集　【全用途】

| 用語 | 説明 |
| :--- | :--- |
| 不動産情報ライブラリ（reinfolib） | 国土交通省の不動産・地理空間情報提供サービス。本アプリのデータ源。 |
| MCP（Model Context Protocol） | LLMツール連携の標準プロトコル。MLITが地理空間MCP Serverを公開。 |
| 地理空間MCP Server / mlit-geospatial-mcp | MLIT公開のMCP実装（GitHub: chirikuuka/mlit-geospatial-mcp）。本アプリのロジック移植元。 |
| Vercel | フロント＋サーバーレス関数をデプロイするホスティング。 |
| Serverless Function | リクエスト毎に起動する関数。本アプリの `api/query.py`。 |
| GeoJSON | 地理空間データのJSON形式。`FeatureCollection` / `Feature` / `properties` を持つ。 |
| Feature / properties | GeoJSONの1地物と、その属性（項目=値の辞書）。本アプリの「地点」と「項目」。 |
| XIT/XCT/XPT/XKT | reinfolib各APIのコード体系（例：XKT002＝用途地域）。 |
| ACCESS_TOKEN | 社内共有用の簡易合言葉。URL漏洩時の簡易防止策（本格認証ではない）。 |
| LIBRARY_API_KEY | 不動産情報ライブラリのAPIキー（機密）。 |

【用途】全用途

---

## 4. システム構成　【仕様書/詳細】

### 4.1 アーキテクチャ（論理構成）

```
[利用者ブラウザ]
   │  ① 緯度経度・対象年・トークン・取得API選択
   ▼
[Vercel 静的配信]  public/index.html（フロント：入力UI・結果整形・CSV/JSON出力）
   │  ② GET /api/query?lat=..&lon=..&apis=..&year=..&token=..
   ▼
[Vercel Python Serverless]  api/query.py（トークン検証・範囲検証・payload整形）
   │  ③ handle_request(payload)
   ▼
[移植ロジック lib/]  request_processor（GeospatialService）＋ utils
   │  ④ 逆ジオコーダ／タイル座標変換／30API並列呼び出し
   ▼
[外部]  不動産情報ライブラリ API（XIT/XCT/XPT/XKT）, 国土地理院 逆ジオコーダ/ジオコーダ
   │  ⑤ GeoJSON等を集約
   ▼
[Vercel Serverless] → JSON応答 → [ブラウザ] 日本語ラベルの表で表示・DL
```

### 4.2 物理配置
- **配信**：Vercel（Team `mas-p047-s-projects` / Project `fudousan_mcp` / Production alias `fudousanmcp.vercel.app`）。
- **ソース**：GitHub `masp047/fudousan_mcp`（Vercelと連携、対象ブランチへのpushで自動再デプロイ）。
- **ビルド**：`vercel.json` の `builds` で `@vercel/python`（`api/query.py`＋`lib/**`同梱）と `@vercel/static`（`public/**`）を明示。

### 4.3 データフロー（手順）
1. ブラウザで緯度経度（Googleマップ形式「緯度, 経度」）を入力し「照会する」。
2. フロントが `/api/query` にGET。トークン設定時は `token` を付与。
3. `query.py` がトークン検証→日本範囲検証→`target_apis`/`year`整形→`handle_request`。
4. `GeospatialService` が国土地理院逆ジオコーダで市区町村コード取得、タイル座標変換、対象APIを **`run_in_executor` で並列実行**。
5. 各APIはGeoJSON（`FeatureCollection`）を返し、点は距離、面は重なりで絞り込み。
6. 集約結果（`input` / `api_results` / `map_url`）をJSONで返却。
7. フロントが各APIのfeature単位で「項目/値」表を生成、英語・コードのキーを日本語ラベルへ変換して表示。CSV/JSONでDL可能。

【用途】仕様書／詳細仕様書

---

## 5. 使用サービス・技術スタック・リソース一覧　【ソース/実装/コスト】

| 区分 | 名称・値 | 識別子・備考 |
| :--- | :--- | :--- |
| ソース管理 | GitHub | `masp047/fudousan_mcp` / ブランチ `claude/new-session-dxvd17`（デフォルトブランチ） |
| ホスティング | Vercel | Team `mas-p047-s-projects` / Project `fudousan_mcp` |
| 本番URL | Vercel Production | https://fudousanmcp.vercel.app |
| ランタイム（サーバー） | Python（Vercel `@vercel/python`） | エントリ `api/query.py`（`BaseHTTPRequestHandler`） |
| フロント | 静的HTML/CSS/JS（単一ファイル） | `public/index.html` |
| Pythonライブラリ | requests, pydantic, shapely, pyproj | `requirements.txt` |
| Webフォント | Google Fonts（Inter / Noto Sans JP / Noto Serif JP） | ブラウザ読込 |
| 外部API（主） | 不動産情報ライブラリ API | `https://www.reinfolib.mlit.go.jp/ex-api/external`（XIT/XCT/XPT/XKT系） |
| 外部API（補） | 国土地理院 逆ジオコーダ | `https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress` |
| 外部API（補） | 国土地理院 ジオコーダ | `https://msearch.gsi.go.jp/address-search/AddressSearch` |
| ロジック移植元 | mlit-geospatial-mcp | GitHub `chirikuuka/mlit-geospatial-mcp`（α版） |
| フィールド対訳の出典 | reinfolib 各API IF仕様 | 参照：GitHub `y-ssk/real-estate-map`（docs/api-if-spec） |
| ローカル環境（デプロイ実施） | macOS + Node.js v26.5.0 / npm 11.17.0 / Vercel CLI 56.5.0 | 利用者のMacから `vercel --prod` 実施 |

【用途】ソース管理／実装管理／コスト管理

---

## 6. 機能仕様（F-n）　【システム仕様書】

| ID | 機能 | 概要 |
| :--- | :--- | :--- |
| F-1 | 座標入力 | 緯度・経度を1欄でGoogleマップ形式「緯度, 経度」で入力。全角カンマ・空白区切りも許容。 |
| F-2 | 取得項目選択 | 30項目をカテゴリ別チェックボックスで選択。全選択／選択解除。未選択は全30項目。 |
| F-3 | 対象年指定 | 対象年（任意、既定2024、2005〜2026、上下ボタンで増減）。 |
| F-4 | アクセストークン | `ACCESS_TOKEN` 設定時、合言葉一致で照会許可（未設定時は誰でも可）。 |
| F-5 | 照会実行 | `/api/query` を呼び出し、30APIを並列取得。進捗・件数を表示。 |
| F-6 | 結果表示 | API別カード → 地点(feature)別の折りたたみ → 「項目/値」表。先頭地点は展開。 |
| F-7 | 日本語ラベル化 | 英語・コードのフィールド名を日本語へ変換（辞書＋動的パターン）。 |
| F-8 | 数値整形 | 価格を3桁区切り（整数）、面積を3桁区切り＋小数第2位で表示。 |
| F-9 | 生データ表示 | 各カードに「生データ(JSON)」の折りたたみを併設（一次資料突合用）。 |
| F-10 | 地図リンク | 不動産情報ライブラリ地図への `map_url` リンクを表示。 |
| F-11 | CSVダウンロード | 「API番号/API名/地点番号/項目/値」形式・UTF-8 BOM付き・カンマ含む値をクオート。 |
| F-12 | JSONダウンロード | `input`/`queried_at`/API別`data`（GeoJSON）/`map_url` を保存。 |
| F-13 | 入力バリデーション | 座標形式・日本範囲（緯度20〜46・経度122〜154）・住所解決可否を検証しエラー明示。 |

【用途】システム仕様書

---

## 7. 詳細仕様　【詳細仕様書】

### 7.1 APIエンドポイント（本アプリ）
- `GET /api/query`
  - クエリ：`lat`（必須, float）, `lon`（必須, float）, `apis`（任意, カンマ区切り整数。空=全30）, `year`（任意, int）, `token`（`ACCESS_TOKEN`設定時必須）
  - 応答（成功）：`{"status":"success","data":{"input":{...},"api_results":[...],"map_url":"...","saved_file_paths":[]}}`
  - 応答（エラー）：`query.py`由来は `{"status":"error","message":"..."}`、`handler.py`由来は `{"status":"error","data":"..."}`（HTTP200）。フロントは双方に対応。
  - CORS：`Access-Control-Allow-Origin: *`（`do_OPTIONS` 実装）。

### 7.2 主要バリデーション
- 座標数値化失敗 → 400「lat/lonは必須の数値パラメータです」。
- 日本範囲外（緯度20〜46・経度122〜154外）→ 400「緯度・経度が日本の範囲外です…」（緯度経度の取り違え検出）。
- 逆ジオコーダで住所解決不可（海上・国外）→ `ValueError`（明快な日本語メッセージ）。

### 7.3 30APIとreinfolibコードの対応（データモデルの中核）

| No | API名（本アプリ） | reinfolibコード | 主なキーの例 |
| :-- | :--- | :--- | :--- |
| 1 | 不動産取引価格（取引価格・成約価格）情報 | XIT001 | TradePrice, Area, CityPlanning（英語キー） |
| 2 | 鑑定評価書情報 | XCT001 | 「標準地 …」（日本語キー） |
| 3 | 地価公示・地価調査のポイント（点） | XPT002 | u_current_years_price_ja, location_number_ja |
| 4 | 都市計画区域・区域区分 | XKT001 | prefecture, city_code, kubun_id, area_classification_ja |
| 5 | 用途地域 | XKT002 | youto_id, use_area_ja, u_building_coverage_ratio_ja |
| 6 | 立地適正化計画 | XKT003 | kubun_name_ja, area_classification_ja |
| 7 | 小学校区 | XKT004 | A27_001, A27_004_ja |
| 8 | 中学校区 | XKT005 | A32_001, A32_004_ja |
| 9 | 学校 | XKT006 | P29_004_ja, P29_003_name_ja |
| 10 | 保育園・幼稚園等 | XKT007 | preSchoolName_ja, welfareFacility…Code |
| 11 | 医療機関 | XKT010 | P04_002_ja, P04_001_name_ja |
| 12 | 福祉施設 | XKT011 | P14_008_ja, P14_005_name_ja |
| 13 | 将来推計人口（250mメッシュ） | XKT013 | MESH_ID, PT00_YYYY 等（年次テンプレート） |
| 14 | 防火・準防火地域 | XKT014 | fire_prevention_ja |
| 15 | 駅別乗降客数 | XKT015 | S12_001_ja, S12_009…057 |
| 16 | 災害危険区域 | XKT016 | A48_005_ja, A48_012 |
| 17 | 図書館 | XKT017 | P27_005_ja |
| 18 | 市区町村役場等 | XKT018 | P05_003_ja |
| 19 | 自然公園地域 | XKT019 | OBJ_NAME_ja, AREA_SIZE |
| 20 | 大規模盛土造成地マップ | XKT020 | embankment_classification |
| 21 | 地すべり防止地区 | XKT021 | region_name, landslide_area |
| 22 | 急傾斜地崩壊危険区域 | XKT022 | public_notice_date, landslide_area |
| 23 | 地区計画 | XKT023 | plan_name, plan_type_ja |
| 24 | 高度利用地区 | XKT024 | advanced_name, advanced_type_ja |
| 25 | 液状化発生傾向図 | XKT025 | liquefaction_tendency_level |
| 26 | 洪水浸水想定区域（想定最大規模） | XKT026 | A31a_202, A31a_205 |
| 27 | 高潮浸水想定区域 | XKT027 | A49_003 |
| 28 | 津波浸水想定 | XKT028 | A40_003 |
| 29 | 土砂災害警戒区域 | XKT029 | A33_001, A33_005 |
| 30 | 人口集中地区 | XKT031 | A16_003, A16_005 |

> 注：APIキーの種別により、reinfolibは英語キー（XIT001）・コードキー（国土数値情報系 A/P/S…）・日本語キー（XCT001）が混在する。フロントの `LABELS` 辞書＋`humanizeKey()` でこれを日本語表示へ統一している。

### 7.4 主要関数一覧（フロント `public/index.html`）
| 関数 | 役割 |
| :--- | :--- |
| `renderResultBody` | API結果1件をfeature別に整形し、生JSON折りたたみを付与 |
| `renderFeature` | 地点(feature)を折りたたみ表示（見出し＝代表値＋座標） |
| `renderKvTable` | properties を「項目/値」表に。内部フィールド除外・空値スキップ・価格/面積整形 |
| `fieldKind` | キーが価格/面積かを判定（3桁区切りの対象） |
| `humanizeKey` | フィールド名→日本語ラベル（辞書優先→動的パターン→原文） |
| `featureLabel` | 見出しに使う代表値（所在地・名称等）を探索 |
| `buildCsv` / `buildJson` | ダウンロード用データ生成 |

### 7.5 主要関数一覧（バックエンド `lib/`）
| 関数/クラス | 役割 |
| :--- | :--- |
| `handle_request(payload)` | `RequestModel` 検証→`GeospatialService.process_request` 実行→`{status,data}` 返却 |
| `GeospatialService.converted_coordinate` | タイル座標変換・逆ジオコーダ・住所解決不可の明快エラー |
| `GeospatialService.process_request` | 対象API並列実行・地図URL生成・（サーバーレスではファイル保存無効） |
| `BasePointApi` / `BasePolygonApi` | 点＝距離絞り込み／面＝重なり絞り込みの基底 |
| `RequestModel`（pydantic） | `target_apis` 空なら全30に展開、条件フィールドの整合 |
| `get_citycd`（逆ジオコーダ） | `results` が null/欠落でも安全に `(None,None)` |

### 7.6 送受信JSON例（概念）
- リクエスト（内部payload）：`{"coordinates":[{"lat":43.06,"lon":141.35}],"target_apis":[1,3,5],"save_file":false,"year":2024}`
- レスポンス：`{"status":"success","data":{"input":{"lat":43.06,"lon":141.35},"api_results":[{"file_name":"….geojson","data":{"type":"FeatureCollection","features":[…]}}, null, …],"map_url":"https://…","saved_file_paths":[]}}`

【用途】詳細仕様書

---

## 8. ソースコード管理　【ソース管理】

- リポジトリ：GitHub `masp047/fudousan_mcp`
- 対象ブランチ：`claude/new-session-dxvd17`（Vercelのデフォルト＝本番対象ブランチ）
- Vercel連携：対象ブランチへのpushで自動再デプロイ
- コミット総数：15（第18章に全一覧・時刻）
- バックアップ状況：GitHub（リモート）＋Vercel（デプロイ成果物）。ローカルは利用者Mac（`~/fudousan_mcp`）。

### 8.1 ファイル一覧（行数）

| ファイル | 行 | 区分 |
| :--- | --: | :--- |
| README.md | 48 | 本プロジェクト |
| .gitignore | 25 | 本プロジェクト |
| vercel.json | 18 | 本プロジェクト（改修） |
| requirements.txt | 4 | 本プロジェクト |
| api/query.py | 110 | 本プロジェクト（実装・改修） |
| public/index.html | 889 | 本プロジェクト（実装・改修：主要成果物） |
| lib/request_processor/handler.py | 45 | 移植（mlit-geospatial-mcp） |
| lib/request_processor/service/geospatial_service.py | 211 | 移植＋改修（住所解決エラー） |
| lib/request_processor/service/apis/base_api.py | 174 | 移植 |
| lib/request_processor/service/apis/real_estate_api1〜30.py | 各10〜118 | 移植（30ファイル） |
| lib/request_processor/models/api_models.py | 143 | 移植 |
| lib/request_processor/enums/api_enum.py | 121 | 移植 |
| lib/request_processor/common/{requester,point_filter,polygon_filter,change_address}.py | 26/66/63/100 | 移植 |
| lib/utils/const.py | 67 | 移植 |
| lib/utils/reverse_geocoder.py | 25 | 移植＋改修（安全化） |
| lib/utils/{coordinates_conversion,geocoder,map_url_generator,payload,logger_config,definitions}.py | 65/22/351/45/17/18 | 移植 |
| public/logo_horizontal.png | (画像) | SHINTATSU正規ロゴ |

### 8.2 SOURCE_FILES（本書 付録Zに全文収録する範囲）
本プロジェクトで**新規実装・改修した中核ファイル**を全文収録する：`public/index.html`, `api/query.py`, `vercel.json`, `requirements.txt`, `.gitignore`, `README.md`, `lib/request_processor/handler.py`, `lib/request_processor/service/geospatial_service.py`, `lib/request_processor/service/apis/base_api.py`, `lib/request_processor/models/api_models.py`, `lib/utils/reverse_geocoder.py`, `lib/utils/const.py`, 代表として `real_estate_api1.py`・`real_estate_api2.py`・`real_estate_api3.py`。

> 事実：`real_estate_api4〜30.py` および `lib` のその他ユーティリティは移植元 `chirikuuka/mlit-geospatial-mcp` から**構造上ほぼ同一**で、本アプリでは未改修（`reverse_geocoder.py`・`geospatial_service.py` を除く）。本書では冗長化を避けるため代表ファイルのみ全文収録し、残りは上記一覧で台帳管理する。

【用途】ソース管理

---

## 9. 実装・構築手順（再現手順）　【実装管理】

> 前提：GitHubアカウント、Vercelアカウント、不動産情報ライブラリのAPIキー（承認済）。以下は本プロジェクトで実施した手順（macOS/zsh・利用者Mac）。

### 9.1 リポジトリ準備
1. Webアプリ一式をリポジトリ直下に配置（`api/`・`lib/`・`public/`・`vercel.json`・`requirements.txt`・`README.md`）。
2. `.gitignore` 追加（`.env`・`__pycache__` 等除外。**APIキーはコミットしない**）。
3. `git add -A && git commit && git push -u origin claude/new-session-dxvd17`。

### 9.2 Vercel CLIによるデプロイ
```
cd ~
git clone https://github.com/masp047/fudousan_mcp.git
cd fudousan_mcp
git checkout claude/new-session-dxvd17
npm i -g vercel            # 初回のみ（Node.js必須）
vercel login              # JSTT/SHINTATSUのVercelアカウントでログイン
vercel                    # Create a new project → 既定名 → ./ → Customize:No
vercel env add LIBRARY_API_KEY production   # Sensitive:Yes → 値を貼付（本書非掲載）
vercel env add ACCESS_TOKEN production      # Sensitive:Yes → 合言葉を貼付（本書非掲載）
git pull origin claude/new-session-dxvd17   # vercel.json 改修の取り込み
vercel --prod             # 本番デプロイ → Production alias 発行
```
- 初回は `vercel` の自動検出が `api/query.py` を単一Pythonアプリと誤認しビルド失敗 → `vercel.json` を `builds`（`@vercel/python`＋`@vercel/static`）明示に改修して解決（第16・17章）。
- 「`Due to builds existing …`」警告は仕様どおり（builds優先）で問題なし。

### 9.3 動作確認
- `https://fudousanmcp.vercel.app` を開く（デプロイ保護なし＝公開アクセス可を確認）。
- 緯度経度・トークンを入力し「照会する」。実データ表示を確認。

【用途】実装管理

---

## 10. 設定値・シークレット管理　【セキュリティ】

| 変数名 | 用途 | 保管先 | 値 |
| :--- | :--- | :--- | :--- |
| `LIBRARY_API_KEY` | 不動産情報ライブラリAPIキー | Vercel環境変数（Production, Sensitive） | **本書非掲載** |
| `ACCESS_TOKEN` | 社内共有の簡易合言葉 | Vercel環境変数（Production, Sensitive） | **本書非掲載**（社内で別途共有） |

- APIキーは**サーバー側のみ**で使用（`lib/utils/const.py` が `os.getenv("LIBRARY_API_KEY")` で読込）。フロント・リポジトリには一切含めない。
- `ACCESS_TOKEN` は「URL漏洩時の簡易防止策」であり本格認証ではない（本格的なアクセス制御が必要になった場合は再設計）。
- Sensitive設定のため、Vercel上でも後から値を読み出せない（更新は再登録）。

【用途】セキュリティ

---

## 11. 運用・保守マニュアル　【運用】

### 11.1 変更方法 早見表
| やりたいこと | 操作 |
| :--- | :--- |
| 表示ラベルの日本語追加・修正 | `public/index.html` の `LABELS` に `キー: "日本語"` を追記 |
| 価格/面積の3桁区切り対象追加 | `PRICE_KEYS` / `AREA_KEYS`（同ファイル）へキー追加 |
| 対象年の既定/範囲変更 | `#year` の `value`/`min`/`max` を変更 |
| ブランド色・書体変更 | `:root` のCSS変数を変更 |
| 合言葉の変更 | Vercelで `ACCESS_TOKEN` を再登録し再デプロイ |
| 反映 | 対象ブランチへ `git push`（自動再デプロイ）→ `Cmd+Shift+R` で確認 |

### 11.2 禁止事項
- APIキー・合言葉をリポジトリ／フロント／本書に**書かない**。
- α版データを**無検証で開示資料に転記しない**（一次資料突合が前提）。
- 連続大量リクエスト（利用規約遵守）。

【用途】運用

---

## 12. テスト記録　【品質】

| 実施日時（JST・推定/確定） | 項目 | 結果 |
| :--- | :--- | :--- |
| 2026-07-22 夜（確定：デプロイ直後） | 本番URL表示（フロント描画・デプロイ保護なし） | OK |
| 2026-07-22 夜（確定） | 実データ照会（小樽市祝津近傍 43.06788, 141.35411 相当） | OK（30項目中15項目にデータ、想定どおり） |
| 2026-07-22 夜（確定） | 緯度経度取り違え時のエラー表示 | OK（範囲チェックで検出、`'results'`クラッシュ解消） |
| 2026-07-22 夜（確定） | 英語ラベルの日本語化（API4/5/6 等） | OK（IF仕様に基づく辞書で表示） |
| 継続（コード検証） | 全Pythonファイル byte-compile／import チェーン | OK |
| 継続（コード検証） | フロントJS `node --check`／CSVビルダーのモック検証 | OK |
| （制約） | 開発実行環境からの外部API直接照会 | 不可（egressポリシーによりreinfolib/vercel/GSIへの接続遮断） |

> 注：本ツールの実データ取得テストは、ネットワーク制限のない利用者ブラウザ（本番URL）で実施・確認した。

【用途】品質

---

## 13. コスト管理　【コスト管理】

| 区分 | 内容 | 金額・見込み |
| :--- | :--- | :--- |
| GitHub | プライベート/パブリックリポジトリ | 無料枠（推定） |
| Vercel | Serverless＋静的配信 | 無料/Hobby枠内で稼働（推定：利用量が小規模のため） |
| 不動産情報ライブラリAPI | 利用申請・APIキー | 無償（申請承認済） |
| 国土地理院 ジオコーダ | 逆ジオコーダ/ジオコーダ | 無償 |
| Google Fonts | Webフォント配信 | 無償 |
| 人的工数 | 開発・デプロイ・検証・文書化 | 第18章参照（確定下限 約2h27m／現実的推定 約4〜6h） |

> クォータ注意：Vercelの無料枠には実行時間・帯域の上限がある。多人数・高頻度利用時はプラン見直しを推奨（推定）。

【用途】コスト管理

---

## 14. リスク・制約・既知の問題　【運用/エンハンス】

| # | 種別 | 内容 | 対応/回避 |
| :-- | :--- | :--- | :--- |
| R-1 | データ品質 | α版データを含み、正確性は保証されない | UI・本書に明記、一次資料突合を必須化 |
| R-2 | セキュリティ | `ACCESS_TOKEN` は簡易合言葉（推測余地あり、`jstt-` 接頭辞） | 本格認証が必要になれば再設計（R-6） |
| R-3 | 依存 | 外部API（reinfolib/GSI）の仕様変更・障害に依存 | フィールド辞書・エラー整形で緩和、変化時に追随 |
| R-4 | 表示 | 未辞書のフィールド/コード値は原文表示となる場合あり | 発見都度 `LABELS` 追加（運用手順） |
| R-5 | 性能 | 30API並列でも初回は10〜30秒（外部応答依存） | 必要APIのみ選択で短縮可 |
| R-6 | アクセス制御 | Google Workspaceドメイン制限は未対応 | 将来の再アーキテクチャ候補（第15章 E-3） |
| R-7 | ランタイム | Vercelの新Python自動検出と`builds`の相互作用 | `builds`明示で固定済（第17章） |

【用途】運用／エンハンス

---

## 15. 次期エンハンス候補（E-n）　【エンハンス記録】

| ID | 内容 | 目的 |
| :-- | :--- | :--- |
| E-1 | Excel（.xlsx）直接出力、地点横持ちCSV、API別シート | 実務での二次加工を容易に |
| E-2 | コード値の名称変換（診療科目コード等）・未辞書フィールドの継続整備 | 可読性向上 |
| E-3 | 本格アクセス制御（Google Workspaceドメイン制限／SSO） | 社外流出リスク低減 |
| E-4 | 住所→緯度経度の順引き入力（ジオコーダ活用） | 座標を持たない利用者の利便 |
| E-5 | 人口・世帯数など件数系の3桁区切り、重要項目の抜き出し表示 | 視認性向上 |
| E-6 | 照会履歴・お気に入り地点・地図プレビュー | 反復業務の効率化 |
| E-7 | 結果のPDF/帳票化（物件カルテ） | 報告書作成の自動化 |

【用途】エンハンス記録

---

## 16. 意思決定ログ　【仕様書/発表】

| # | 決定 | 理由 |
| :-- | :--- | :--- |
| D-1 | MCPではなくWebアプリ（Vercel）で提供 | MCPはローカル専用。社内複数人がブラウザ利用するため |
| D-2 | GAS(JS全面書換)ではなくVercel(Python移植)継続 | 既存Pythonロジックを活かし工数削減 |
| D-3 | デプロイはCLIだが実行は利用者Mac | 開発環境のegress制限でVercel APIへ到達不可のため |
| D-4 | `vercel.json` を `builds` 明示に改修 | 新Python自動検出のビルド失敗を確実に回避 |
| D-5 | デフォルトブランチ＝作業ブランチのままデプロイ | `main`不要（Vercelはデフォルトブランチを本番対象） |
| D-6 | 結果は生JSONでなく日本語ラベルの表で表示 | 非エンジニアの実務利用のため |
| D-7 | フィールド対訳は推測せずIF仕様（第三者GitHub）から取得 | 法規制・都市計画データの誤ラベル防止 |
| D-8 | 緯度経度を1欄化しGoogleマップ形式を内部分割 | 入力の手間削減（Google Mapsから貼付） |
| D-9 | CSVは生値・BOM付き、JSONは生データ保持 | Excel互換と再処理性の両立 |
| D-10 | SHINTATSUブランドガイド準拠（色/書体/正規ロゴ） | 社内制作物の統一 |

【用途】仕様書／発表

---

## 17. つまづき・課題と解決（Lessons Learned）　【発表/実装】

| 事象 | 原因 | 解決 |
| :--- | :--- | :--- |
| 初回`vercel`デプロイでビルド失敗（No python entrypoint） | 新Vercel Python自動検出が `api/query.py` を単一アプリと誤認 | `vercel.json` を `builds`（python＋static）＋`routes`明示に改修 |
| 照会が「エラー: 200」としか出ない | handler由来エラーは `data` に入るがフロントは `message` のみ参照 | フロントを `message`/`data` 両対応に修正 |
| 無効座標で `'results'` クラッシュ | 経度に緯度を誤入力（海上）→逆ジオコーダ応答に `results` 無く KeyError | 入口の日本範囲チェック＋逆ジオコーダ安全化＋住所解決不可の明快エラー |
| 結果が英語/生JSONで実務に使えない | reinfolibが英語・コードキーを返す／初期実装が生JSON表示 | 表形式化＋IF仕様準拠の日本語ラベル辞書＋動的パターン |
| Windows前提の手順がMacで不一致 | 引き継ぎ時の想定環境差 | Mac(zsh)向け手順に切替え、リポジトリを新規clone |
| 開発環境から本番/外部APIへ到達不可 | 組織のegressポリシー（reinfolib/vercel/GSI遮断） | 実データ検証は利用者ブラウザ（本番URL）で実施 |

【用途】発表／実装

---

## 18. 時刻付きタイムライン＆工数データ　【コスト/発表】

**情報源**：本リポジトリのgitコミット時刻（`git log`、Asia/Tokyo換算）。会話単位の時刻は保持しない前提で、**コミットという確実なアンカー時刻**のみを基準とする。

### 18.1 マイルストーン表（全コミット）

| # | 日時(JST) | ハッシュ | 前アンカー差 | 出来事（要旨） |
| :-- | :--- | :--- | :--- | :--- |
| 1 | 2026-07-22 21:34 | a90e2b4 | — | Webアプリ一式を追加（初期実装） |
| 2 | 2026-07-22 21:48 | 60c0218 | +14m | エラー表示の修正（message/data両対応） |
| 3 | 2026-07-22 22:15 | 26c6716 | +27m | Vercelビルド修正（builds明示） |
| 4 | 2026-07-22 22:43 | a4a03ec | +28m | 結果を表形式で描画 |
| 5 | 2026-07-22 22:48 | bb5924f | +5m | 無効座標のハンドリング |
| 6 | 2026-07-22 22:52 | 29ca83d | +4m | 英語ラベルの日本語化（初期） |
| 7 | 2026-07-22 22:59 | 332bd60 | +7m | SHINTATSUブランド適用＋文字2倍 |
| 8 | 2026-07-22 23:10 | 0de009d | +11m | レイアウト幅拡張（10%）・部署名変更 |
| 9 | 2026-07-22 23:16 | 1434271 | +6m | レイアウト幅5% |
| 10 | 2026-07-22 23:22 | 9b30557 | +6m | タイトルをMCP解説ページへリンク |
| 11 | 2026-07-22 23:33 | e98f403 | +11m | 対象年入力・価格/面積の3桁区切り |
| 12 | 2026-07-22 23:46 | 96982fe | +12m | 全APIフィールドの日本語ラベル |
| 13 | 2026-07-22 23:55 | ae8a93d | +9m | 緯度経度の1欄化（Googleマップ貼付） |
| 14 | 2026-07-23 00:00 | 0b7a0b5 | +6m | 「Googleマップからコピー」リンク化 |
| 15 | 2026-07-23 23:04 | 3164cbd | +23h03m | Phase3：CSV/JSONダウンロード |

### 18.2 稼働セッションと工数
- **セッションA（初回構築）**：#1〜#14、2026-07-22 21:34:14 → 07-23 00:00:54。全アンカー間隔 < 30分＝連続稼働。**確定稼働（下限）＝ 2時間26分40秒（≒2.44h）**。
- **セッションB（Phase3）**：#15 単発（07-23 23:04）。内部アンカー無し＝コミットのみでは工数測定不可。
- **カレンダー経過**：#1〜#15で約25.5時間。うち **アイドル（#14→#15の日跨ぎ）約23時間**。

### 18.3 未計測作業（コミットに現れない稼働・推定）
- 初回のリポジトリ準備・ローカルclone、Vercel CLIログイン／プロジェクト作成／環境変数登録／本番デプロイ。
- ブラウザでの反復動作確認（複数回のスクリーンショット確認）。
- フィールド対訳のためのWeb調査（IF仕様の収集）。
- 本完成図書の作成。

### 18.4 実稼働の現実的推定（レンジ）
- セッションA：確定下限2.44h＋デプロイ/検証/調査の未計測分を加味し **約3.0〜4.0h（推定）**。
- セッションB＋本書作成：**約1.0〜2.0h（推定）**。
- **合計：約4.0〜6.0h（推定）**。

### 18.5 工数計算用CSV
```csv
通番,日付,時刻(JST),種別,前アンカー差(分),区分,出来事
1,2026-07-22,21:34,commit,,セッションA,初期実装
2,2026-07-22,21:48,commit,14,セッションA,エラー表示修正
3,2026-07-22,22:15,commit,27,セッションA,Vercelビルド修正
4,2026-07-22,22:43,commit,28,セッションA,表形式描画
5,2026-07-22,22:48,commit,5,セッションA,無効座標対応
6,2026-07-22,22:52,commit,4,セッションA,日本語化(初期)
7,2026-07-22,22:59,commit,7,セッションA,ブランド適用+2倍
8,2026-07-22,23:10,commit,11,セッションA,幅10%/部署名
9,2026-07-22,23:16,commit,6,セッションA,幅5%
10,2026-07-22,23:22,commit,6,セッションA,タイトルリンク
11,2026-07-22,23:33,commit,11,セッションA,対象年/桁区切り
12,2026-07-22,23:46,commit,12,セッションA,全API日本語ラベル
13,2026-07-22,23:55,commit,9,セッションA,緯度経度1欄化
14,2026-07-23,00:00,commit,6,セッションA,Googleマップリンク
15,2026-07-23,23:04,commit,1383,セッションB,Phase3 DL機能
```

【用途】コスト管理／発表

---

## 19. 成果発表資料用サマリ／スライド構成案　【発表資料】

**キーメッセージ**：「緯度経度を貼るだけで、国交省30項目を日本語で即照会・ダウンロード」。

推奨スライド構成（SHINTATSUブランド：紺見出し・赤罫・Noto Serif/Sans・正規ロゴ）：
1. 表紙：地理空間MCP連携（不動産情報照会ツール）／SHINTATSU 不動産営業部
2. 背景・課題：MLIT地理空間MCPはローカル専用 → 社内共有できない
3. 解決：MCPロジックをWebアプリ化（Vercel）、緯度経度→30項目
4. デモ：入力→結果（日本語表）→CSV/JSONダウンロード
5. アーキテクチャ図（第4章）
6. 取得できる30項目（不動産/都市計画/施設/防災/人口）
7. 工夫：日本語ラベル辞書・桁区切り・エラー堅牢化・ブランド適用
8. つまづきと解決（第17章の要点）
9. コスト・工数（無料枠中心／推定4〜6h）
10. 今後：xlsx出力・アクセス制御・住所順引き（第15章）
11. まとめ・横展開

【用途】発表資料

---

## 20. 確定リソース値の索引　【全用途】

| キー | 値 |
| :--- | :--- |
| プロジェクト名 | 地理空間MCP連携（不動産情報照会Webアプリ） |
| 作成主体 | 日本信達株式会社 不動産営業部 |
| GitHub | masp047/fudousan_mcp |
| ブランチ（デフォルト/本番対象） | claude/new-session-dxvd17 |
| Vercel Team | mas-p047-s-projects |
| Vercel Project | fudousan_mcp |
| 本番URL | https://fudousanmcp.vercel.app |
| Serverlessエンドポイント | GET /api/query |
| フロント | public/index.html（889行） |
| サーバー | api/query.py（110行） |
| Python依存 | requests, pydantic, shapely, pyproj |
| 取得API数 | 30（XIT/XCT/XPT/XKT系） |
| 外部：reinfolib | https://www.reinfolib.mlit.go.jp/ex-api/external |
| 外部：GSI逆ジオコーダ | https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress |
| 移植元 | chirikuuka/mlit-geospatial-mcp |
| 環境変数 | LIBRARY_API_KEY, ACCESS_TOKEN（いずれもVercel Sensitive・本書非掲載） |
| コミット総数 | 15 |
| 初回コミット | 2026-07-22 21:34 JST（a90e2b4） |
| 最終コミット（本書時点） | 2026-07-23 23:04 JST（3164cbd） |
| 確定稼働下限 | 2時間26分40秒（セッションA） |

【用途】全用途

---

## 完成チェックリスト（自己点検）

- [x] 0〜20章＋付録Y/Zをすべて含む（欠落なし）
- [x] 機密は非掲載/マスク、所在のみ記載（LIBRARY_API_KEY・ACCESS_TOKEN）
- [x] 時刻は一次情報（gitコミット）から抽出し確定/推定を峻別
- [x] SOURCE_FILES（中核ファイル）を全文収録（付録Z）。移植の重複ファイルは台帳管理と明記
- [x] 全編で識別子・数値・固有名を索引（第20章）と一致
- [x] 構築手順が再現可能な粒度（第9章）
- [x] 各章に【用途】タグ
- [x] 単一.mdで完結＋3点セット（本書＋実ソース＋README）を提示

---

## 付録Y. 運用手順書（README）全文

（以下、`README.md` の全文）

```markdown
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

```

---

## 付録Z. ソースコード・設定ファイル全文

> 本プロジェクトで新規実装・改修した中核ファイルの全文。`real_estate_api4〜30.py` 等の移植ファイルは第8章の台帳を参照（構造上ほぼ同一・未改修）。

### Z-1. public/index.html（フロントエンド：主要成果物）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>地理空間MCP（Model Context Protocol） | SHINTATSU</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root {
    /* SHINTATSU ブランドカラー */
    --red: #b04123;
    --navy: #1C2951;
    --blue: #4A69CF;
    --ink: #161820;
    --ink-sub: #4A4F5A;
    --mute: #8A8F99;
    --paper: #FBFAF7;
    --paper-alt: #F2F0EA;
    --line: rgba(28,41,81,.16);
    --rule-red: rgba(176,65,35,.55);
    --accent: #b04123;              /* 後方互換 */
    --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    --sans: "Noto Sans JP", "Inter", "Hiragino Sans", sans-serif;
    --serif: "Noto Serif JP", "Hiragino Mincho ProN", serif;
    --en: "Inter", "Noto Sans JP", sans-serif;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    font-size: 20px;
    line-height: 1.7;
  }
  header {
    padding: 44px 5% 32px;
    border-bottom: 1px solid var(--line);
  }
  header .brand-logo {
    height: 76px;
    width: auto;
    display: block;
    margin-bottom: 24px;
  }
  header .eyebrow {
    font-family: var(--en);
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.3em;
    color: var(--red);
    text-transform: uppercase;
  }
  header h1 {
    margin: 12px 0 0;
    font-family: var(--serif);
    font-size: 44px;
    font-weight: 700;
    color: var(--navy);
    padding-bottom: 14px;
  }
  header h1::after {
    content: "";
    display: block;
    width: 96px;
    height: 3px;
    background: var(--red);
    margin-top: 14px;
  }
  header h1 a {
    color: inherit;
    text-decoration: underline;
    text-decoration-color: var(--rule-red);
    text-decoration-thickness: 2px;
    text-underline-offset: 6px;
  }
  header h1 a:hover { color: var(--red); }
  header p {
    margin: 8px 0 0;
    font-size: 26px;
    color: var(--ink-sub);
    max-width: none;
  }
  main {
    max-width: none;
    margin: 0 auto;
    padding: 32px 5%;
  }
  .panel {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 28px;
    margin-bottom: 28px;
  }
  .panel h2 {
    font-family: var(--serif);
    font-size: 26px;
    font-weight: 700;
    color: var(--navy);
    margin: 0 0 20px;
  }
  .coord-row {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
  }
  .field {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    min-width: 220px;
  }
  .field label {
    font-size: 24px;
    color: var(--ink-sub);
  }
  .field label a {
    color: var(--red);
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  input[type=text], input[type=number], input[type=password] {
    font-family: var(--en);
    font-variant-numeric: tabular-nums;
    font-size: 28px;
    padding: 12px 14px;
    border: 1px solid var(--line);
    border-radius: 6px;
    background: #fff;
    color: var(--ink);
  }
  input:focus { outline: 2px solid var(--red); outline-offset: 1px; }

  .api-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 8px 28px;
  }
  .api-group { margin-bottom: 16px; }
  .api-group h3 {
    font-size: 22px;
    font-weight: 700;
    color: var(--red);
    margin: 18px 0 8px;
    letter-spacing: 0.03em;
  }
  .api-item {
    display: flex;
    align-items: baseline;
    gap: 10px;
    font-size: 25px;
    padding: 5px 0;
  }
  .api-item input {
    margin: 0;
    width: 22px;
    height: 22px;
    accent-color: var(--red);
  }

  .actions {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-top: 24px;
    flex-wrap: wrap;
  }
  button {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 28px;
    padding: 14px 30px;
    border: none;
    border-radius: 8px;
    background: var(--red);
    color: #fff;
    cursor: pointer;
  }
  button:disabled { opacity: 0.5; cursor: default; }
  button.secondary {
    background: transparent;
    color: var(--red);
    border: 1px solid var(--red);
  }
  .status {
    font-family: var(--sans);
    font-size: 24px;
    color: var(--ink-sub);
  }

  #results { display: flex; flex-direction: column; gap: 18px; }
  .result-card {
    background: #fff;
    border: 1px solid var(--line);
    border-left: 6px solid var(--red);
    border-radius: 8px;
    padding: 22px 26px;
  }
  .result-card.empty { border-left-color: var(--line); opacity: 0.6; }
  .result-card h4 {
    margin: 0 0 14px;
    font-family: var(--serif);
    font-size: 28px;
    font-weight: 700;
    color: var(--navy);
  }
  .result-card .count {
    font-family: var(--en);
    font-size: 22px;
    color: var(--ink-sub);
    font-weight: 400;
  }
  pre {
    background: var(--paper-alt);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 14px;
    font-family: var(--mono);
    font-size: 23px;
    overflow-x: auto;
    max-height: 520px;
    margin: 0;
  }
  .feature {
    border: 1px solid var(--line);
    border-radius: 6px;
    margin-top: 12px;
    background: #fff;
  }
  .feature > summary {
    cursor: pointer;
    padding: 14px 16px;
    font-size: 25px;
    font-weight: 700;
    color: var(--navy);
    list-style: none;
  }
  .feature > summary::-webkit-details-marker { display: none; }
  .feature > summary::before { content: "▸ "; color: var(--red); }
  .feature[open] > summary::before { content: "▾ "; }
  .feat-body { padding: 0 16px 16px; }
  .kv {
    width: 100%;
    border-collapse: collapse;
    font-size: 25px;
  }
  .kv th, .kv td {
    text-align: left;
    vertical-align: top;
    padding: 10px 14px;
    border-top: 1px solid var(--line);
  }
  .kv th {
    width: 42%;
    color: var(--ink-sub);
    font-weight: 600;
    background: var(--paper-alt);
  }
  .kv td {
    font-family: var(--sans);
    font-variant-numeric: tabular-nums;
    font-size: 24px;
    color: var(--ink);
    word-break: break-word;
  }
  .geo {
    font-family: var(--en);
    font-size: 22px;
    color: var(--mute);
    font-weight: 400;
  }
  .raw-toggle { margin-top: 16px; }
  .raw-toggle > summary {
    cursor: pointer;
    font-size: 23px;
    color: var(--ink-sub);
    list-style: revert;
  }
  .map-link {
    display: inline-block;
    margin-top: 20px;
    font-size: 25px;
    color: var(--red);
  }
  footer {
    max-width: none;
    margin: 0 auto;
    padding: 16px 5% 56px;
    font-size: 22px;
    color: var(--ink-sub);
  }
  footer .brand-line {
    color: var(--navy);
    font-weight: 700;
    margin-bottom: 6px;
  }
</style>
</head>
<body>

<header>
  <img class="brand-logo" src="/logo_horizontal.png" alt="NIHON SHINTATSU Co., Ltd. &mdash; Trust and Achievements">
  <div class="eyebrow">不動産営業部　ー　検証用プロトタイプ</div>
  <h1><a href="https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_fr17_000001_00047.html" target="_blank" rel="noopener">地理空間MCP（Model Context Protocol）</a></h1>
  <p>不動産情報ライブラリAPI（国土交通省）を緯度経度から照会します。α版データを含むため、開示資料への転記前に必ず一次資料と突き合わせてください。</p>
</header>

<main>

  <div class="panel">
    <h2>1. 対象地点</h2>
    <div class="coord-row">
      <div class="field" style="flex: 2 1 360px;">
        <label for="latlon">緯度・経度（<a href="https://www.google.com/maps" target="_blank" rel="noopener">Googleマップからコピー</a>）</label>
        <input type="text" id="latlon" placeholder="例: 43.1814586884606, 141.02923643780812">
      </div>
      <div class="field" style="max-width: 140px;">
        <label for="year">対象年（任意）</label>
        <input type="number" id="year" value="2024" min="2005" max="2026" step="1">
      </div>
      <div class="field" style="max-width: 200px;" id="token-field">
        <label for="token">アクセストークン</label>
        <input type="password" id="token" placeholder="必要な場合のみ">
      </div>
    </div>
  </div>

  <div class="panel">
    <h2>2. 取得する項目（未選択なら全30項目）</h2>
    <div id="api-checkboxes"></div>
    <div class="actions">
      <button class="secondary" type="button" id="select-all">全選択</button>
      <button class="secondary" type="button" id="select-none">選択解除</button>
    </div>
  </div>

  <div class="actions" style="margin-bottom: 20px;">
    <button type="button" id="run">照会する</button>
    <span class="status" id="status"></span>
  </div>

  <div class="actions" id="result-actions" style="display: none; margin-bottom: 16px;">
    <button type="button" class="secondary" id="dl-csv">CSVでダウンロード</button>
    <button type="button" class="secondary" id="dl-json">JSONでダウンロード</button>
  </div>

  <div id="results"></div>

</main>

<footer>
  <div class="brand-line">日本信達株式会社 / SHINTATSU</div>
  データ出典：不動産情報ライブラリ（国土交通省）／このツールは社内検証用のα版連携です。取得値の正確性は保証されません。
</footer>

<script>
const API_NAMES = {
  1: "不動産価格（取引価格・成約価格）情報", 2: "鑑定評価書情報", 3: "地価公示・地価調査のポイント",
  4: "都市計画区域・区域区分", 5: "用途地域", 6: "立地適正化計画",
  7: "小学校区", 8: "中学校区", 9: "学校", 10: "保育園・幼稚園等",
  11: "医療機関", 12: "福祉施設", 17: "図書館", 18: "市区町村役場等",
  13: "将来推計人口(250mメッシュ)", 15: "駅別乗降客数", 30: "人口集中地区",
  16: "災害危険区域", 20: "大規模盛土造成地マップ", 21: "地すべり防止地区",
  22: "急傾斜地崩壊危険区域", 25: "液状化発生傾向図", 26: "洪水浸水想定区域",
  27: "高潮浸水想定区域", 28: "津波浸水想定", 29: "土砂災害警戒区域",
  14: "防火・準防火地域", 23: "地区計画", 24: "高度利用地区", 19: "自然公園地域"
};
// 英語/コードのフィールド名 → 日本語ラベル。
// 出典: 不動産情報ライブラリ 各API IF仕様（XIT/XCT/XPT/XKT系）
const LABELS = {
  // 共通
  prefecture: "都道府県", prefecture_name: "都道府県名", prefecture_name_ja: "都道府県名",
  prefecture_code: "都道府県コード", city_code: "市区町村コード", city_name: "市区町村名",
  group_code: "行政コード", address: "所在地", region_name: "区域名",
  notice_number: "告示番号", notice_number_s: "告示番号S", notice_date: "告示年月日",
  first_decision_date: "当初決定日", decision_date: "設定年月日",
  decision_classification: "設定区分", decision_maker: "設定者名",
  decision_type_ja: "設定区分名", kubun_id: "区分コード", kubun_name_ja: "区域名",
  area_classification_ja: "区域区分", target_year: "対象年",
  charge_ministry_code: "所管省庁コード", charge_ministry_name: "所管省庁名",
  landslide_area: "指定面積（ha）",

  // API1 不動産取引価格情報 (XIT001)
  PriceCategory: "価格情報区分", Type: "種類", Region: "地域",
  MunicipalityCode: "市区町村コード", Prefecture: "都道府県名", PrefectureCode: "都道府県コード",
  Municipality: "市区町村名", DistrictName: "地区名", DistrictCode: "地区コード",
  TradePrice: "取引価格（総額）", PricePerUnit: "坪単価", UnitPrice: "単価（㎡あたり）",
  FloorPlan: "間取り", Area: "面積（㎡）", LandShape: "土地の形状", Frontage: "間口（m）",
  TotalFloorArea: "延床面積（㎡）", BuildingYear: "建築年", Structure: "建物の構造",
  Use: "用途", Purpose: "今後の利用目的", Direction: "前面道路：方位",
  Classification: "前面道路：種類", Breadth: "前面道路：幅員（m）", CityPlanning: "都市計画",
  CoverageRatio: "建蔽率（%）", FloorAreaRatio: "容積率（%）", Period: "取引時期",
  Renovation: "改装", Remarks: "取引の事情等", NearestStation: "最寄駅：名称",
  TimeToNearestStation: "最寄駅：距離（分）", Year: "年", Quarter: "四半期", name: "名称",

  // API3 地価公示・地価調査ポイント (XPT002)
  point_id: "地点ID", target_year_name_ja: "対象年", land_price_type: "地価区分",
  use_category_name_ja: "用途区分名", standard_lot_number_ja: "標準地/基準地番号",
  city_county_name_ja: "郡市名", ward_town_village_name_ja: "区町村名", place_name_ja: "地名",
  residence_display_name_ja: "住居表示", location_number_ja: "所在及び地番",
  u_current_years_price_ja: "当年価格", last_years_price: "前年価格",
  year_on_year_change_rate: "対前年変動率", u_cadastral_ja: "地積",
  frontage_ratio: "間口比率", depth_ratio: "奥行き比率", building_structure_name_ja: "構造",
  u_ground_hierarchy_ja: "地上階層", u_underground_hierarchy_ja: "地下階層",
  front_road_name_ja: "前面道路区分", front_road_azimuth_name_ja: "前面道路の方位",
  front_road_width: "前面道路の幅員", front_road_pavement_condition: "前面道路の舗装状況",
  side_road_azimuth_name_ja: "側道の方位", side_road_name_ja: "側道区分",
  gas_supply_availability: "ガスの有無", water_supply_availability: "水道の有無",
  sewer_supply_availability: "下水道の有無", nearest_station_name_ja: "最寄り駅名",
  proximity_to_transportation_facilitites: "交通施設との近接区分",
  u_road_distance_to_nearest_station_name_ja: "最寄り駅までの道路距離",
  usage_status_name_ja: "利用現況", current_usage_status_of_surrounding_land_name_ja: "周辺の利用現況",
  area_division_name_ja: "区域区分", regulations_use_category_name_ja: "法規制・用途区分",
  regulations_altitude_district_name_ja: "法規制・高度地区",
  regulations_fireproof_name_ja: "法規制・防火/準防火",
  u_regulations_building_coverage_ratio_ja: "法規制・建蔽率",
  u_regulations_floor_area_ratio_ja: "法規制・容積率",
  regulations_forest_law_name_ja: "法規制・森林法", regulations_park_law_name_ja: "法規制・公園法",

  // API4 区域区分 (XKT001) / API6 立地適正化 (XKT003)

  // API5 用途地域 (XKT002)
  youto_id: "用途地域コード", use_area_ja: "用途地域",
  u_floor_area_ratio_ja: "容積率", u_building_coverage_ratio_ja: "建蔽率",
  u_front_road_width_ja: "前面道路幅員", land_use_name_ja: "用途地域",

  // API14 防火・準防火 (XKT014)
  fire_prevention_ja: "防火・準防火地域",
  // API23 地区計画 (XKT023)
  plan_name: "計画名", plan_type_ja: "計画区分名",
  // API24 高度利用地区 (XKT024)
  advanced_name: "高度名称", advanced_type_ja: "高度区分名",

  // API7 小学校区 (XKT004)
  A27_001: "行政区域コード", A27_002: "設置主体", A27_003: "学校コード",
  A27_004_ja: "名称", A27_005: "所在地",
  // API8 中学校区 (XKT005)
  A32_001: "行政区域コード", A32_002: "設置主体", A32_003: "学校コード",
  A32_004_ja: "名称", A32_005: "所在地",
  // API9 学校 (XKT006)
  P29_001: "行政区域コード", P29_002: "学校コード", P29_003: "学校分類コード",
  P29_003_name_ja: "学校分類", P29_004_ja: "名称", P29_005_ja: "所在地",
  P29_006: "管理者コード", P29_007: "休校区分", P29_008: "キャンパスコード", P29_009_ja: "学校名備考",
  // API10 保育園・幼稚園 (XKT007)
  administrativeAreaCode: "行政区域コード", preSchoolName_ja: "名称", location_ja: "所在地",
  administratorCode: "管理者コード", schoolCode: "学校コード", schoolClassCode: "学校分類コード",
  schoolClassCode_name_ja: "学校分類", closeSchoolCode: "休校コード",
  welfareFacilityClassCode: "福祉施設大分類コード", welfareFacilityMiddleClassCode: "福祉施設中分類コード",
  welfareFacilityMinorClassCode: "福祉施設小分類コード",
  // API11 医療機関 (XKT010)
  P04_001: "医療機関分類コード", P04_001_name_ja: "医療機関分類", P04_002_ja: "施設名称",
  P04_003_ja: "所在地", P04_004: "診療科目1", P04_005: "診療科目2", P04_006: "診療科目3",
  P04_007: "開設者分類", P04_008: "病床数", P04_009: "救急告示病院", P04_010: "災害拠点病院",
  medical_subject_ja: "診療科目",
  // API12 福祉施設 (XKT011)
  P14_001: "都道府県名", P14_002: "市区町村名", P14_003: "行政区域コード", P14_004_ja: "所在地",
  P14_005: "福祉施設大分類コード", P14_005_name_ja: "福祉施設大分類", P14_006: "福祉施設中分類コード",
  P14_006_name_ja: "福祉施設中分類", P14_007: "福祉施設小分類コード", P14_008_ja: "名称",
  P14_009: "管理者コード", P14_010: "位置正確度コード",
  // API13 将来推計人口メッシュ (XKT013)
  MESH_ID: "分割地域メッシュコード", SHICODE: "行政区域コード",
  // API15 駅別乗降客数 (XKT015)
  S12_001_ja: "駅名", S12_001c: "駅コード", S12_001g: "グループコード", S12_002_ja: "運営会社",
  S12_003_ja: "路線名", S12_004: "鉄道区分", S12_005: "事業者種別",
  S12_009: "2011年乗降客数", S12_013: "2012年乗降客数", S12_017: "2013年乗降客数",
  S12_021: "2014年乗降客数", S12_025: "2015年乗降客数", S12_029: "2016年乗降客数",
  S12_033: "2017年乗降客数", S12_037: "2018年乗降客数", S12_041: "2019年乗降客数",
  S12_045: "2020年乗降客数", S12_049: "2021年乗降客数", S12_053: "2022年乗降客数",
  S12_057: "2023年乗降客数",
  // API16 災害危険区域 (XKT016)
  A48_001: "都道府県名", A48_002: "市町村名", A48_003: "代表行政コード", A48_004: "指定主体区分",
  A48_005_ja: "区域名", A48_006: "所在地", A48_007: "指定理由コード", A48_007_name_ja: "指定理由",
  A48_008_ja: "指定理由詳細", A48_009: "告示年月日", A48_010: "告示番号", A48_011: "根拠条例",
  A48_012: "面積", A48_013: "縮尺", A48_014: "その他",
  // API17 図書館 (XKT017)
  P27_001: "行政区域コード", P27_002: "公共施設大分類", P27_003: "公共施設小分類コード",
  P27_003_name_ja: "公共施設小分類", P27_004: "文化施設分類コード", P27_004_name_ja: "文化施設分類",
  P27_005_ja: "名称", P27_006_ja: "所在地", P27_007: "管理者コード", P27_008: "階数", P27_009: "建築年",
  // API18 市区町村役場等 (XKT018)
  P05_001: "行政区域コード", P05_002: "施設分類コード", P05_002_name_ja: "施設分類",
  P05_003_ja: "名称", P05_004_ja: "所在地",
  // API19 自然公園地域 (XKT019)
  OBJECTID: "シェープID", PREFEC_CD: "都道府県コード", AREA_CD: "地区コード", CTV_NAME: "市町村名",
  FIS_YEAR: "年度", THEMA_NO: "主題番号", LAYER_NO: "レイヤ番号", AREA_SIZE: "面積（ha）",
  IOSIDE_DIV: "内外区分", REMARK_STR: "備考", Shape_Leng: "シェープ長", Shape_Area: "シェープ面積",
  OBJ_NAME_ja: "シェープ名",
  // API20 大規模盛土造成地 (XKT020)
  embankment_classification: "盛土区分", embankment_number: "盛土番号",
  // API22 急傾斜地崩壊危険区域 (XKT022)
  public_notice_date: "公示年月日", public_notice_number: "公示番号",
  // API25 液状化発生傾向図 (XKT025)
  mesh_code: "メッシュコード", topographic_classification_code: "微地形区分コード",
  topographic_classification_name_ja: "微地形区分", liquefaction_tendency_level: "液状化発生傾向",
  note: "説明",
  // API26 洪水浸水想定区域 (XKT026)
  A31a_201: "河川番号", A31a_202: "河川名", A31a_203: "河川管理番号",
  A31a_204: "河川管理者", A31a_205: "浸水深ランク",
  // API27 高潮浸水想定区域 (XKT027)
  A49_001: "都道府県名", A49_002: "都道府県コード", A49_003: "浸水深区分",
  // API28 津波浸水想定 (XKT028)
  A40_001: "都道府県名", A40_002: "都道府県コード", A40_003: "津波浸水深の区分",
  // API29 土砂災害警戒区域 (XKT029)
  A33_001: "現象の種類", A33_002: "区域区分", A33_003: "都道府県コード", A33_004: "区域番号",
  A33_005: "区域名", A33_006: "所在地", A33_007: "公示日", A33_008: "特別警戒未指定フラグ",
  // API30 人口集中地区 (XKT031)
  A16_001: "DID識別子", A16_002: "行政区域コード", A16_003: "市区町村名", A16_004: "人口集中地区符号",
  A16_005: "人口", A16_006: "面積", A16_007: "前回人口", A16_008: "前回面積",
  A16_009: "人口集中地区の人口割合", A16_010: "人口集中地区の面積割合", A16_011: "国勢調査年度",
  A16_012: "人口（男）", A16_013: "人口（女）", A16_014: "世帯数",
};

const GROUPS = [
  ["不動産取引・評価", [1,2,3]],
  ["都市計画", [4,5,6,14,23,24]],
  ["教育・保育", [7,8,9,10]],
  ["医療・福祉・生活", [11,12,17,18]],
  ["人口・交通", [13,15,30]],
  ["防災・ハザード", [16,20,21,22,25,26,27,28,29]],
  ["自然環境", [19]],
];

const wrap = document.getElementById("api-checkboxes");
GROUPS.forEach(([label, ids]) => {
  const group = document.createElement("div");
  group.className = "api-group";
  group.innerHTML = `<h3>${label}</h3>`;
  const grid = document.createElement("div");
  grid.className = "api-grid";
  ids.forEach(id => {
    const item = document.createElement("label");
    item.className = "api-item";
    item.innerHTML = `<input type="checkbox" value="${id}"> ${id}. ${API_NAMES[id]}`;
    grid.appendChild(item);
  });
  group.appendChild(grid);
  wrap.appendChild(group);
});

// 直近の照会結果（ダウンロード用に保持）
let lastResult = null;

document.getElementById("select-all").onclick = () => {
  document.querySelectorAll('.api-item input').forEach(cb => cb.checked = true);
};
document.getElementById("select-none").onclick = () => {
  document.querySelectorAll('.api-item input').forEach(cb => cb.checked = false);
};

document.getElementById("run").onclick = async () => {
  const latlonRaw = document.getElementById("latlon").value.trim();
  const year = document.getElementById("year").value.trim();
  const token = document.getElementById("token").value.trim();
  const status = document.getElementById("status");
  const results = document.getElementById("results");
  const runBtn = document.getElementById("run");

  // 「緯度, 経度」を分割（Googleマップ形式。全角カンマ・空白区切りも許容）
  const parts = latlonRaw.split(/[,、\s]+/).filter(s => s !== "");
  if (parts.length < 2 || isNaN(Number(parts[0])) || isNaN(Number(parts[1]))) {
    status.textContent = "緯度・経度を「43.1814586884606, 141.02923643780812」の形式で入力してください";
    return;
  }
  const lat = parts[0];  // Googleマップは「緯度, 経度」の順
  const lon = parts[1];

  const checked = Array.from(document.querySelectorAll('.api-item input:checked')).map(cb => cb.value);

  const params = new URLSearchParams({ lat, lon });
  if (checked.length) params.set("apis", checked.join(","));
  if (year) params.set("year", year);
  if (token) params.set("token", token);

  runBtn.disabled = true;
  status.textContent = "照会中...";
  results.innerHTML = "";
  lastResult = null;
  document.getElementById("result-actions").style.display = "none";

  try {
    const res = await fetch(`/api/query?${params.toString()}`);
    const json = await res.json();

    if (!res.ok || json.status === "error") {
      // エラーメッセージはquery.py由来(message)とhandler.py由来(data)の両形式に対応
      const errMsg = json.message || json.data || res.status;
      status.textContent = `エラー: ${errMsg}`;
      runBtn.disabled = false;
      return;
    }

    const data = json.data || {};
    const apiResults = data.api_results || [];
    const targetIds = checked.length ? checked.map(Number) : Object.keys(API_NAMES).map(Number).sort((a,b)=>a-b);

    status.textContent = `完了（${apiResults.filter(r => r).length} / ${apiResults.length} 件にデータあり）`;

    apiResults.forEach((r, idx) => {
      const apiId = targetIds[idx];
      const name = API_NAMES[apiId] || `API ${apiId}`;
      const card = document.createElement("div");

      if (!r || !r.data) {
        card.className = "result-card empty";
        card.innerHTML = `<h4>${apiId}. ${name} <span class="count">該当データなし</span></h4>`;
      } else {
        const features = (r.data && Array.isArray(r.data.features)) ? r.data.features : null;
        const countLabel = features ? `${features.length}件` : "";
        card.className = "result-card";
        card.innerHTML = `<h4>${apiId}. ${name} <span class="count">${countLabel}</span></h4>`;
        card.appendChild(renderResultBody(r.data, features));
      }
      results.appendChild(card);
    });

    if (data.map_url) {
      const link = document.createElement("a");
      link.href = data.map_url;
      link.target = "_blank";
      link.className = "map-link";
      link.textContent = "→ 不動産情報ライブラリの地図で確認する";
      results.appendChild(link);
    }

    // ダウンロード用に結果を保持し、ボタンを表示
    lastResult = { apiResults, targetIds, input: data.input || { lat, lon }, mapUrl: data.map_url || null, lat, lon };
    document.getElementById("result-actions").style.display = "flex";
  } catch (e) {
    status.textContent = `通信エラー: ${e}`;
  } finally {
    runBtn.disabled = false;
  }
};

// --- 結果を人が読める形に整形して描画する ---
function renderResultBody(data, features) {
  const box = document.createElement("div");

  if (features && features.length) {
    // GeoJSON: 地点(feature)ごとに項目表を作る
    features.forEach((f, i) => box.appendChild(renderFeature(f, i, features.length)));
  } else if (data && typeof data === "object") {
    // GeoJSON以外: そのままキー値表で表示
    box.appendChild(renderKvTable(data));
  }

  // 生データ(JSON)は折りたたみで残す（一次資料との突き合わせ・確認用）
  const raw = document.createElement("details");
  raw.className = "raw-toggle";
  const sum = document.createElement("summary");
  sum.textContent = "生データ (JSON) を表示";
  const pre = document.createElement("pre");
  pre.textContent = JSON.stringify(data, null, 2);
  raw.appendChild(sum);
  raw.appendChild(pre);
  box.appendChild(raw);

  return box;
}

function renderFeature(f, i, total) {
  const props = (f && f.properties && typeof f.properties === "object") ? f.properties : (f || {});
  const det = document.createElement("details");
  det.className = "feature";
  if (i === 0) det.open = true;  // 先頭は開いて表示

  let label = featureLabel(props);
  if (label.length > 40) label = label.slice(0, 40) + "…";
  const geo = geomLabel(f && f.geometry);

  const summary = document.createElement("summary");
  summary.innerHTML = `${i + 1}. ${escapeHtml(label)}` + (geo ? ` <span class="geo">(${escapeHtml(geo)})</span>` : "");
  det.appendChild(summary);

  const body = document.createElement("div");
  body.className = "feat-body";
  body.appendChild(renderKvTable(props));
  det.appendChild(body);
  return det;
}

function renderKvTable(obj) {
  const table = document.createElement("table");
  table.className = "kv";
  const rows = [];

  if (obj && typeof obj === "object" && !Array.isArray(obj)) {
    Object.keys(obj).forEach(k => {
      if (k.startsWith("_")) return;         // 内部フィールド(_id, _index等)は除外
      let val = formatValue(obj[k]);
      if (val === null) return;              // 空値はスキップ

      // 価格・面積は3桁区切りに整形（価格=整数、面積=小数第2位まで）
      const kind = fieldKind(k);
      if (kind && /^-?\d+(\.\d+)?$/.test(val)) {
        const n = Number(val);
        if (kind === "price") val = n.toLocaleString("ja-JP", { maximumFractionDigits: 0 });
        else if (kind === "area") val = n.toLocaleString("ja-JP", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      }

      rows.push([humanizeKey(k), val]);      // 英語/コードキーは日本語ラベルに変換

    });
  }

  if (!rows.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 2;
    td.innerHTML = '<span class="geo">表示できる項目がありません</span>';
    tr.appendChild(td);
    table.appendChild(tr);
    return table;
  }

  rows.forEach(([k, v]) => {
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.textContent = k;
    const td = document.createElement("td");
    td.textContent = v;
    tr.appendChild(th);
    tr.appendChild(td);
    table.appendChild(tr);
  });
  return table;
}

// 価格・面積フィールドの種別を判定（3桁区切り整形の対象）
const PRICE_KEYS = new Set(["TradePrice", "PricePerUnit", "UnitPrice", "u_current_years_price_ja", "last_years_price"]);
const AREA_KEYS = new Set(["Area", "TotalFloorArea", "u_cadastral_ja", "landslide_area", "AREA_SIZE", "A48_012", "A16_006"]);
function fieldKind(k) {
  if (PRICE_KEYS.has(k)) return "price";
  if (AREA_KEYS.has(k)) return "area";
  // 日本語キー（鑑定評価 XCT001 等）
  if (/(価格|評価額|地価|単価|金額)/.test(k) && !/(区分|情報|時点|コード|番号)/.test(k)) return "price";
  if (/(面積|地積|延床)/.test(k) && !/(率|割合)/.test(k)) return "area";
  return null;
}

// フィールド名を日本語ラベルに変換（辞書優先 → 動的パターン → 原文）
function humanizeKey(k) {
  if (LABELS[k]) return LABELS[k];
  // 将来推計人口メッシュ (XKT013) の年次テンプレートフィールド
  let m;
  if ((m = k.match(/^PT00_(\d{4})$/))) return `総人口（${m[1]}）`;
  if ((m = k.match(/^PTN_?(\d{4})$/))) return `総数人口・秘匿なし（${m[1]}）`;
  if ((m = k.match(/^PTA_(\d{4})$/))) return `年少人口 0-14歳（${m[1]}）`;
  if ((m = k.match(/^PTB_(\d{4})$/))) return `生産年齢人口 15-64歳（${m[1]}）`;
  if ((m = k.match(/^PTC_(\d{4})$/))) return `高齢人口 65歳以上（${m[1]}）`;
  if ((m = k.match(/^PTD_(\d{4})$/))) return `75歳以上人口（${m[1]}）`;
  if ((m = k.match(/^PTE_(\d{4})$/))) return `80歳以上人口（${m[1]}）`;
  if ((m = k.match(/^RTA_(\d{4})$/))) return `年少人口比率（${m[1]}）`;
  if ((m = k.match(/^RTB_(\d{4})$/))) return `生産年齢人口比率（${m[1]}）`;
  if ((m = k.match(/^RTC_(\d{4})$/))) return `高齢化率（${m[1]}）`;
  if ((m = k.match(/^RTD_(\d{4})$/))) return `75歳以上人口比率（${m[1]}）`;
  if ((m = k.match(/^RTE_(\d{4})$/))) return `80歳以上人口比率（${m[1]}）`;
  if ((m = k.match(/^PT(\d{2})_(\d{4})$/))) return `5歳階級別人口 区分${m[1]}（${m[2]}）`;
  if ((m = k.match(/^HITOKU(\d{4})$/))) return `秘匿記号（${m[1]}）`;
  if ((m = k.match(/^GASSAN(\d{4})$/))) return `秘匿時の合算先メッシュ（${m[1]}）`;
  return k;
}

function formatValue(v) {
  if (v === null || v === undefined) return null;
  if (typeof v === "string") { const t = v.trim(); return t === "" ? null : t; }
  if (typeof v === "number" || typeof v === "boolean") return String(v);
  if (typeof v === "object") {
    try { const s = JSON.stringify(v); return (s === "{}" || s === "[]") ? null : s; }
    catch (e) { return String(v); }
  }
  return String(v);
}

// 地点の見出しに使う代表的な値を探す（所在地・名称など）
function featureLabel(props) {
  const candidates = [
    "所在地", "所在及び地番", "標準地 所在地 所在地番", "標準地 所在地 市区町村名",
    "名称", "施設名称", "施設名", "駅名", "学校名", "市区町村名",
    // 各API IF仕様の代表名フィールド
    "use_area_ja", "fire_prevention_ja", "plan_name", "advanced_name", "region_name",
    "place_name_ja", "location_number_ja", "standard_lot_number_ja",
    "P04_002_ja", "P14_008_ja", "P27_005_ja", "P05_003_ja",
    "P29_004_ja", "A27_004_ja", "A32_004_ja", "preSchoolName_ja",
    "S12_001_ja", "A48_005_ja", "A33_005", "OBJ_NAME_ja",
    "DistrictName", "Municipality", "NearestStation", "Prefecture",
    "city_name", "prefecture", "CTV_NAME",
    "location number ia", "address", "name",
  ];
  for (const key of candidates) {
    if (props[key] != null && String(props[key]).trim() !== "") return String(props[key]).trim();
  }
  for (const k of Object.keys(props)) {
    if (k.startsWith("_")) continue;
    const v = props[k];
    if (typeof v === "string" && v.trim() !== "") return v.trim();
  }
  return "データ";
}

function geomLabel(g) {
  if (!g || !g.coordinates) return "";
  if (g.type === "Point" && Array.isArray(g.coordinates) && g.coordinates.length >= 2) {
    const lon = Number(g.coordinates[0]), lat = Number(g.coordinates[1]);
    if (isFinite(lon) && isFinite(lat)) return `経度 ${lon.toFixed(6)}, 緯度 ${lat.toFixed(6)}`;
  }
  return g.type || "";
}

function escapeHtml(str) {
  return String(str).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

// --- 結果のダウンロード（CSV / JSON） ---
function downloadBlob(filename, text, mime) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function tsStamp() {
  const d = new Date();
  const p = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}`;
}

function csvCell(v) {
  const s = v == null ? "" : String(v);
  return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

// 表示と同じ日本語ラベルで、地点・項目・値を1行ずつのCSVに（Excel対応・BOM付き）
function buildCsv(res) {
  const rows = [["API番号", "API名", "地点番号", "項目", "値"]];
  res.apiResults.forEach((r, idx) => {
    const apiId = res.targetIds[idx];
    const apiName = API_NAMES[apiId] || `API ${apiId}`;
    const features = (r && r.data && Array.isArray(r.data.features)) ? r.data.features : [];
    if (!features.length) {
      rows.push([apiId, apiName, "", "（該当データなし）", ""]);
      return;
    }
    features.forEach((f, i) => {
      const props = (f && f.properties && typeof f.properties === "object") ? f.properties : (f || {});
      Object.keys(props).forEach(k => {
        if (k.startsWith("_")) return;
        const val = formatValue(props[k]);
        if (val === null) return;
        rows.push([apiId, apiName, i + 1, humanizeKey(k), val]);
      });
    });
  });
  return "﻿" + rows.map(r => r.map(csvCell).join(",")).join("\r\n");
}

function buildJson(res) {
  return JSON.stringify({
    input: res.input,
    queried_at: new Date().toISOString(),
    results: res.apiResults.map((r, idx) => ({
      api_id: res.targetIds[idx],
      api_name: API_NAMES[res.targetIds[idx]] || null,
      data: r ? r.data : null,
    })),
    map_url: res.mapUrl || null,
  }, null, 2);
}

document.getElementById("dl-csv").onclick = () => {
  if (!lastResult) return;
  downloadBlob(`不動産情報_${lastResult.lat}_${lastResult.lon}_${tsStamp()}.csv`, buildCsv(lastResult), "text/csv;charset=utf-8");
};
document.getElementById("dl-json").onclick = () => {
  if (!lastResult) return;
  downloadBlob(`不動産情報_${lastResult.lat}_${lastResult.lon}_${tsStamp()}.json`, buildJson(lastResult), "application/json");
};
</script>

</body>
</html>

```

### Z-2. api/query.py（Serverless Function）

```python
"""
Vercel Python Serverless Function
GET /api/query?lat=..&lon=..&apis=1,3,5&year=2024&token=..

不動産情報ライブラリAPIを、mlit-geospatial-mcpと同じロジックで呼び出し、
JSONで結果を返す。フロントエンド(public/index.html)から呼ばれる想定。
"""

import asyncio
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# lib配下（request_processor / utils）をimport可能にする
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from request_processor.handler import handle_request  # noqa: E402

# 簡易アクセストークン（Vercelの環境変数 ACCESS_TOKEN で設定。未設定なら誰でもアクセス可）
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def _json_response(handler: BaseHTTPRequestHandler, status: int, body: dict):
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(payload)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        # --- アクセストークンチェック ---
        if ACCESS_TOKEN:
            token = qs.get("token", [None])[0]
            if token != ACCESS_TOKEN:
                _json_response(self, 401, {"status": "error", "message": "unauthorized"})
                return

        # --- パラメータ取得 ---
        try:
            lat = float(qs.get("lat", [None])[0])
            lon = float(qs.get("lon", [None])[0])
        except (TypeError, ValueError):
            _json_response(
                self, 400, {"status": "error", "message": "lat/lonは必須の数値パラメータです"}
            )
            return

        # 日本国内の緯度経度かをざっくり検証（緯度と経度の取り違えを検出）
        if not (20.0 <= lat <= 46.0 and 122.0 <= lon <= 154.0):
            _json_response(
                self,
                400,
                {
                    "status": "error",
                    "message": (
                        "緯度・経度が日本の範囲外です。緯度と経度が入れ替わっていないか"
                        "ご確認ください（緯度は約20〜46、経度は約122〜154）。"
                    ),
                },
            )
            return

        apis_raw = qs.get("apis", [""])[0]
        if apis_raw.strip():
            try:
                target_apis = [int(x) for x in apis_raw.split(",") if x.strip()]
            except ValueError:
                _json_response(
                    self, 400, {"status": "error", "message": "apisはカンマ区切りの数値で指定してください"}
                )
                return
        else:
            target_apis = []  # 空 = 全API

        year_raw = qs.get("year", [None])[0]
        year = int(year_raw) if year_raw else None

        payload = {
            "coordinates": [{"lat": lat, "lon": lon}],
            "target_apis": target_apis,
            "save_file": False,  # サーバーレス環境ではファイル保存しない
        }
        if year:
            payload["year"] = year

        # --- 不動産情報ライブラリAPI呼び出し（mlit-geospatial-mcpと同一ロジック） ---
        try:
            result = asyncio.run(handle_request(payload))
        except Exception as e:  # noqa: BLE001
            _json_response(self, 500, {"status": "error", "message": str(e)})
            return

        _json_response(self, 200, result)

```

### Z-3. vercel.json（ビルド設定）

```json
{
  "builds": [
    {
      "src": "api/query.py",
      "use": "@vercel/python",
      "config": { "includeFiles": "lib/**" }
    },
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    { "src": "/api/query", "dest": "/api/query.py" },
    { "src": "/", "dest": "/public/index.html" },
    { "src": "/(.*)", "dest": "/public/$1" }
  ]
}

```

### Z-4. requirements.txt

```text
requests
pydantic
shapely
pyproj

```

### Z-5. .gitignore

```text
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/

# Environment / secrets
.env
.env.local
*.env

# Vercel
.vercel/

# OS / editor
.DS_Store
Thumbs.db
.idea/
.vscode/

# Logs / output
*.log
output/

```

### Z-6. lib/request_processor/handler.py

```python
"""
MCPリクエストハンドラ。

このモジュールは、MCPから受け取ったpayloadを処理し、不動産ライブラリAPI呼び出しを行う。

Functions:
    handle_request(payload: dict) -> dict:
        MCPからのリクエストを処理し、結果を返す。
"""

import logging
from pathlib import Path

from request_processor.models.api_models import RequestModel
from request_processor.service.geospatial_service import GeospatialService

logger = logging.getLogger(__name__)


async def handle_request(payload: dict) -> dict:
    """
    MCPから受け取ったpayloadを処理し、外部API呼び出しを行う。

    Args:
        payload (dict[str, Any]): MCPから渡されたpayload

    Returns:
        dict[str, Any]: 処理結果
            - status: "success" または "error"
            - data: 成功時はAPIレスポンス、失敗時はエラーメッセージ
    """

    logger.info("handle_request started")

    try:
        req = RequestModel(**payload)

        service_instance = GeospatialService()
        res = await service_instance.process_request(req)

        return {"status": "success", "data": res}

    except Exception as e:
        logger.error(f"処理エラー:{e}")
        return {"status": "error", "data": str(e)}

```

### Z-7. lib/request_processor/service/geospatial_service.py（改修：住所解決エラー）

```python
"""
地理空間サービスモジュール。

このモジュールは、座標変換や複数APIの並列呼び出しを行うサービスクラスを提供。

Classes:
    GeospatialService:
        内部ツールの中核処理を担当するクラス
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from request_processor.enums.api_enum import APIEnum
from request_processor.models.api_models import RequestModel
from utils.const import ZOOM
from utils.coordinates_conversion import (
    latlon_to_address,
    latlon_to_tile_fraction,
)
from utils.logger_config import setup_logger
from utils.map_url_generator import build_map_url


class GeospatialService:
    # 内部ツールの中核処理
    def __init__(self):
        self.logger = setup_logger(__name__)

    def converted_coordinate(self, coord):
        """
        座標をタイル座標や住所情報に変換。

        Args:
            coord: 緯度・経度を含むオブジェクト

        Returns:
            dict[str, float]: 変換後の座標情報
        """
        x, y, x_frac, y_frac = latlon_to_tile_fraction(coord.lat, coord.lon, ZOOM)
        muni_cd, lv_01_nm = latlon_to_address(coord.lat, coord.lon)

        # 住所に解決できない座標（海上・国外など）は明快なエラーにする
        if not muni_cd:
            raise ValueError(
                "指定された座標は日本国内の住所として解決できませんでした。"
                "緯度・経度が正しいか（入れ替わっていないか）ご確認ください。"
            )

        converted = {
            "lat": coord.lat,
            "lon": coord.lon,
            "x": x,
            "y": y,
            "x_frac": x_frac,
            "y_frac": y_frac,
            "muni_cd": muni_cd,
            "lv_01_nm": lv_01_nm,
        }
        return converted

    async def process_request(self, req: RequestModel):
        """
        リクエストを処理し、複数APIを並列で呼び出す。

        Args:
            req (RequestModel): 内部処理用にRequestModelに合わせて整形したpayload

        Returns:
            dict[str, object]: 入力座標とAPI結果を含む辞書、不動産ライブラリの地図URLも含む
        """

        # save_fileが未指定(None)またはnullの場合は保存確認を促すレスポンスを返す
        save_file_value = getattr(req, "save_file", None)
        if save_file_value is None:
            return {
                "status": "need_confirmation",
                "message": (
                    "【重要】取得結果のファイルを保存しますか？ "
                    "save_file=true/false を必ずユーザーに選択させてください。"
                    "自動でfalseにしないでください。"
                ),
            }
        # null（JSONからのNone相当）も明示的に判定
        if str(save_file_value).lower() == "null":
            return {
                "status": "need_confirmation",
                "message": (
                    "【重要】取得結果のファイルを保存しますか？ "
                    "保存するかしないかを（save_file=true/false） を必ずユーザーに選択させてください。"
                    "自動でfalseにしないでください。"
                ),
            }

        base_output_folder = "C:/output"
        file_paths = []

        now_folder = datetime.now().strftime("%Y%m%d%H%M")

        for c in req.coordinates:
            # 座標から変換処理
            converted = self.converted_coordinate(c)

            # リクエストのモデルをdictに変換
            req_dict = req.model_dump()

            # APIごとのインスタンス化
            apis = []
            for code in req.target_apis:
                api_enum = APIEnum.from_code(code)
                instance = api_enum.get_instance(
                    req_dict,
                    converted,
                )
                apis.append(instance)

            # exchange()を非同期で並列実行
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(None, api.exchange) for api in apis]
            api_results = await asyncio.gather(*tasks)

            # build_map_urlで地図URL生成
            map_url = build_map_url(c.lat, c.lon, req.target_apis, req_dict)

            # save_fileがTrueならファイル保存
            file_paths = []
            if hasattr(req, "save_file") and req.save_file:
                # 保存対象を一時的に集める
                save_targets = []
                for idx, result in enumerate(api_results):
                    # 完全な None をスキップ
                    if result is None:
                        continue

                    payload_to_write = result
                    file_name = None

                    if isinstance(result, dict):
                        # file_name の取得
                        if (
                            "file_name" in result
                            and isinstance(result["file_name"], str)
                            and result["file_name"].strip()
                        ):
                            file_name = result["file_name"].strip()

                        # data を抽出
                        if "data" in result:
                            data = result.get("data")

                            # data が None/空ならスキップ
                            if data is None:
                                continue

                            # data が dict/list で空ならスキップ
                            if isinstance(data, (dict, list)) and not data:
                                continue

                            # GeoJSON 想定: features が空のときはスキップ
                            if isinstance(data, dict):
                                features = data.get("features", None)
                                if isinstance(features, list) and len(features) == 0:
                                    continue

                            payload_to_write = data

                    # 保存対象が決まったらリストに追加
                    save_targets.append((idx, payload_to_write, file_name))

                # 保存対象が1つ以上ある場合のみフォルダ作成・保存
                if save_targets:
                    output_dir = getattr(req, "output_dir", None)
                    if (
                        output_dir
                        and isinstance(output_dir, str)
                        and output_dir.strip()
                    ):
                        output_folder = Path(output_dir.strip()) / now_folder
                    else:
                        output_folder = Path(base_output_folder) / now_folder
                    output_folder.mkdir(parents=True, exist_ok=True)

                    for idx, payload_to_write, file_name in save_targets:
                        if not file_name:
                            file_name = f"api_result_{idx + 1}.geojson"

                        file_path = output_folder / file_name
                        try:
                            with open(file_path, "w", encoding="utf-8") as f:
                                if isinstance(payload_to_write, (dict, list)):
                                    json.dump(
                                        payload_to_write,
                                        f,
                                        ensure_ascii=False,
                                        indent=2,
                                    )
                                else:
                                    f.write(str(payload_to_write))
                            file_paths.append(str(file_path))
                        except Exception as e:
                            self.logger.error(f"ファイル保存失敗: {file_path} - {e}")
                            file_paths.append(None)

        return {
            "input": {"lat": c.lat, "lon": c.lon},
            "api_results": api_results,
            "map_url": map_url,
            "saved_file_paths": file_paths,
        }

```

### Z-8. lib/request_processor/service/apis/base_api.py

```python
from abc import ABC, abstractmethod

from request_processor.common import requester
from request_processor.common.point_filter import (
    filter_distance,
    get_surrounding_tiles,
)
from request_processor.common.polygon_filter import overlap_judge
from utils.const import LIBRARY_API_KEY, ZOOM
from utils.logger_config import setup_logger


class BaseApi(ABC):
    """
    すべてのAPI処理クラスの基底となる抽象クラス。
    """

    def __init__(self, req_body: dict, converted: dict, **kwargs):
        """
        コンストラクタ。リクエストボディ、変換済みデータ、ロガーを初期化する。
        """
        self.req_body = req_body
        self.converted = converted
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod
    def exchange(self):
        """
        データ取得から加工までの一連の処理を実行する。
        サブクラスで必ず実装する。
        """
        pass


class BaseRealEstateApi(BaseApi):
    """
    不動産ライブラリのAPIを呼び出すクラスのための基底クラス。
    """

    API_CONFIG = {}

    @abstractmethod
    def _call_api(self):
        """APIを呼び出して生データを取得する。"""
        pass

    @abstractmethod
    def _process_data(self, data):
        """取得したデータを加工する。"""
        pass

    def exchange(self):
        self.logger.info(f"{self.API_CONFIG.get('name', '')} excange開始")
        try:
            raw_data = self._call_api()
            processed_data = self._process_data(raw_data)

            if processed_data is None:
                return None

            return {
                "file_name": f"{self.API_CONFIG.get('name', '')}.geojson",
                "data": processed_data,
            }
        except Exception as e:
            self.logger.error(f"{self.API_CONFIG.get('name', '')} excange エラー:{e}")
            return None


class BasePointApi(BaseRealEstateApi):
    """
    周辺4タイル分の情報を取得し、距離で絞り込むAPIのための基底クラス。
    """

    def _call_api(self):
        tiles = get_surrounding_tiles(
            self.converted["x"],
            self.converted["y"],
            self.converted["x_frac"],
            self.converted["y_frac"],
        )
        merged_geojson = {"type": "FeatureCollection", "features": []}

        for x, y in tiles:
            self.logger.info(f"x:{x}, y:{y}")
            params = self._build_params(x, y)

            try:
                response = requester.get(
                    url=self.API_CONFIG["path"],
                    params=params,
                    response_type=self.API_CONFIG["response_type"],
                    headers={
                        "Ocp-Apim-Subscription-Key": f"{LIBRARY_API_KEY}",
                        "Accept": "*/*",
                    },
                )
                if response and isinstance(response, dict) and response.get("features"):
                    merged_geojson["features"].extend(response["features"])

            except Exception as e:
                self.logger.error(f"{self.API_CONFIG.get('name', '')} 呼び出し失敗:{e}")
                raise

        return merged_geojson

    def _build_params(self, x, y):
        """APIリクエストのパラメータを構築する。サブクラスでオーバーライド可能。"""
        return {"response_format": "geojson", "z": ZOOM, "x": x, "y": y}

    def _process_data(self, data):
        if not data or not data.get("features"):
            self.logger.info(f"{self.API_CONFIG.get('name', '')}の該当データなし")
            return None

        distance = self.req_body.get("distance")
        filtered_features = filter_distance(
            features=data["features"],
            latlon=(self.converted["lat"], self.converted["lon"]),
            distance=distance,
        )
        if not filtered_features:
            self.logger.info(
                f"{self.API_CONFIG.get('name', '')}の該当データなし（絞り込み後）"
            )
            return None

        data["features"] = filtered_features
        return data


class BasePolygonApi(BaseRealEstateApi):
    """
    ポリゴンデータを取得し、座標との重なりで絞り込むAPIのための基底クラス。
    """

    def _call_api(self):
        params = self._build_params()
        return requester.get(
            url=self.API_CONFIG["path"],
            params=params,
            response_type=self.API_CONFIG["response_type"],
            headers={
                "Ocp-Apim-Subscription-Key": f"{LIBRARY_API_KEY}",
                "Accept": "*/*",
            },
        )

    def _build_params(self):
        """APIリクエストのパラメータを構築する。"""
        return {
            "response_format": "geojson",
            "z": ZOOM,
            "x": self.converted["x"],
            "y": self.converted["y"],
        }

    def _process_data(self, data):
        if not data or not data.get("features"):
            self.logger.info(f"{self.API_CONFIG.get('name', '')}の該当データなし")
            return None

        filtered_features = overlap_judge(
            features=data["features"],
            latlon=(self.converted["lat"], self.converted["lon"]),
        )
        if not filtered_features:
            self.logger.info(
                f"{self.API_CONFIG.get('name', '')}の該当データなし（絞り込み後）"
            )
            return None

        data["features"] = filtered_features
        return data

```

### Z-9. lib/request_processor/models/api_models.py

```python
from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic import BaseModel, field_validator, model_validator


# リクエストモデル
class coodinatesItem(BaseModel):
    lat: float
    lon: float


class RequestModel(BaseModel):
    coordinates: List[coodinatesItem]
    target_apis: Optional[List[int]] = None
    distance: Optional[int] = 425
    landmap_distance: Optional[int] = 50
    price_classification: Optional[str] = None
    year: Optional[int] = datetime.now().year - 1
    quarter: Optional[int] = None
    language: Optional[str] = None
    division: Optional[List[str]] = ["00", "03", "05", "07", "09", "10", "13", "20"]
    land_price_classification: Optional[str] = None
    use_category_code: Optional[List[str]] = None
    administrative_area_code: Optional[List[str]] = None
    welfare_facility_class_code: Optional[List[str]] = None
    welfare_facility_middle_class_code: Optional[List[str]] = None
    welfare_facility_minor_class_code: Optional[List[str]] = None
    prefecture_code: Optional[List[str]] = None
    district_code: Optional[List[str]] = None
    save_file: Optional[bool] = None
    output_dir: Optional[str] = None

    # 任意設定
    conditional_fields: ClassVar[Dict[str, List[int]]] = {
        "distance": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
        ],
        "price_classification": [1],
        "year": [1, 2, 3],
        "quarter": [1],
        "language": [1],
        "division": [2],
        "land_price_classification": [3],
        "use_category_code": [3],
        "administrative_area_code": [7, 8, 12, 16, 17, 21, 22, 30],
        "welfare_facility_class_code": [12],
        "welfare_facility_middle_class_code": [12],
        "welfare_facility_minor_class_code": [12],
        "prefecture_code": [19, 21, 22],
        "district_code": [19],
    }

    # target_apisが空なら全指定
    @field_validator("target_apis", mode="before")
    @classmethod
    def default_target_apis(cls, v):
        if not v:
            return [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
            ]
        return v

    # 必須チェック
    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Please specify one or more coordinates")
        return v

    @model_validator(mode="after")
    def validate_fields(self):
        target_apis_list = self.target_apis or []
        for field_name, required_values in RequestModel.conditional_fields.items():
            if hasattr(self, field_name):
                if not any(v in target_apis_list for v in required_values):
                    setattr(self, field_name, None)
        return self


# レスポンスモデル
class ResponseModel(BaseModel):
    status: str
    message: str

```

### Z-10. lib/utils/reverse_geocoder.py（改修：安全化）

```python
import requests

from utils.const import RE_RGEOCODER_URL


# 緯度経度から都道府県CD検索(国土地理院による逆ジオコーダ)
def get_citycd(lat, lon):
    response = requests.get(
        f"{RE_RGEOCODER_URL}?lat={lat}&lon={lon}",
        headers={"User-Agent": "REINS-Client"},
        verify=False,
    )
    if response.status_code == 200:
        result = response.json()
        # 海上・国外など住所に解決できない座標では results が null/欠落するため安全に取得
        results = result.get("results") if isinstance(result, dict) else None
        if not isinstance(results, dict):
            return None, None

        muni_cd = results.get("muniCd")      # 都道府県コード
        lv_01_nm = results.get("lv01Nm")     # 市区町村名
        return muni_cd, lv_01_nm

    else:
        return None, None

```

### Z-11. lib/utils/const.py

```python
import os

ZOOM = 15
MAP_URL_ZOOM = 16
SURVER_YEAR = 2025

####### 不動産ライブラリに関する定数定義 #######
# API情報
LIBRARY_API_KEY = os.getenv("LIBRARY_API_KEY")
LIBRARY_API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external"

####### 逆ジオコーダ（国土地理院） #######
RE_RGEOCODER_URL = "https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress"

####### ジオコーダ（国土地理院） #######
RGEOCODER_URL = "https://msearch.gsi.go.jp/address-search/AddressSearch"

####### 都道府県一覧 #######
PREFECTURE_MAP = {
    "01": "北海道",
    "02": "青森県",
    "03": "岩手県",
    "04": "宮城県",
    "05": "秋田県",
    "06": "山形県",
    "07": "福島県",
    "08": "茨城県",
    "09": "栃木県",
    "10": "群馬県",
    "11": "埼玉県",
    "12": "千葉県",
    "13": "東京都",
    "14": "神奈川県",
    "15": "新潟県",
    "16": "富山県",
    "17": "石川県",
    "18": "福井県",
    "19": "山梨県",
    "20": "長野県",
    "21": "岐阜県",
    "22": "静岡県",
    "23": "愛知県",
    "24": "三重県",
    "25": "滋賀県",
    "26": "京都府",
    "27": "大阪府",
    "28": "兵庫県",
    "29": "奈良県",
    "30": "和歌山県",
    "31": "鳥取県",
    "32": "島根県",
    "33": "岡山県",
    "34": "広島県",
    "35": "山口県",
    "36": "徳島県",
    "37": "香川県",
    "38": "愛媛県",
    "39": "高知県",
    "40": "福岡県",
    "41": "佐賀県",
    "42": "長崎県",
    "43": "熊本県",
    "44": "大分県",
    "45": "宮崎県",
    "46": "鹿児島県",
    "47": "沖縄県",
}

```

### Z-12. real_estate_api1.py（代表：XIT001 取引価格）

```python
from request_processor.common import requester
from request_processor.common.change_address import (
    get_cityname,
    get_district_name,
    get_pref_name,
)
from request_processor.service.apis.base_api import BaseRealEstateApi
from utils.const import LIBRARY_API_KEY, LIBRARY_API_URL
from utils.geocoder import get_latlon


class RealEstateApi1(BaseRealEstateApi):
    API_CONFIG = {
        "name": "不動産取引価格（取引価格・成約価格）情報",
        "path": f"{LIBRARY_API_URL}/XIT001",
        "response_type": "json",
    }

    def _call_api(self):
        # パラメータ生成
        headers = {
            "Ocp-Apim-Subscription-Key": f"{LIBRARY_API_KEY}",
            "Accept": "*/*",
        }
        params = {
            "year": self.req_body.get("year"),
            "city": self.converted["muni_cd"],
        }

        # 任意のパラメータを外部APIへのリクエストにセットする
        optional_param_mapping = {
            "priceClassification": "price_classification",
            "quarter": "quarter",
            "language": "language",
        }
        for api_key, req_key in optional_param_mapping.items():
            value = self.req_body.get(req_key)
            if value is not None:
                params[api_key] = value

        # 外部API呼び出し
        response = requester.get(
            url=self.API_CONFIG["path"],
            params=params,
            response_type=self.API_CONFIG["response_type"],
            headers=headers,
        )

        return response

    def _process_data(self, data):
        try:
            if not data or "data" not in data:
                self.logger.info("APIから有効なデータが取得できませんでした。")
                return None

            # 絞り込み処理
            # 住所（大字レベル）取得
            prefecture = get_pref_name(self.converted["muni_cd"])
            municipality = get_cityname(self.converted["muni_cd"])
            district_name = get_district_name(self.converted["lv_01_nm"])
            full_addr = f"{prefecture}{municipality}{district_name}"

            # 検索座標と同じ地名のデータを取得
            filter_data = [
                item
                for item in data["data"]
                if item.get("Prefecture") == prefecture
                and item.get("Municipality") == municipality
                and item.get("DistrictName") == district_name
            ]

            if not filter_data:
                self.logger.info("該当データなし")
                return None

            # ジオコーダで緯度経度を取得
            coordinates = get_latlon(full_addr)
            if coordinates is None or None in coordinates:
                self.logger.error(
                    f"不動産取引価格（取引価格・成約価格）情報のジオコーダ失敗: {full_addr}"
                )
                return None

            # GeoJSON形式に変換＋緯度経度追加
            features = [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": coordinates},
                    "properties": item,
                }
                for item in filter_data
            ]
            geojson = {"type": "FeatureCollection", "features": features}

        except Exception as e:
            self.logger.error(
                f"不動産取引価格（取引価格・成約価格）情報 excange エラー:{e}"
            )  # エラーは基底クラスで捕捉される
            raise  # 再スローして基底クラスに処理を委ねる

        return geojson

```

### Z-13. real_estate_api2.py（代表：XCT001 鑑定評価）

```python
from request_processor.common import requester
from request_processor.common.point_filter import filter_distance
from request_processor.service.apis.base_api import BaseRealEstateApi
from utils.const import LIBRARY_API_KEY, LIBRARY_API_URL


class RealEstateApi2(BaseRealEstateApi):
    API_CONFIG = {
        "name": "鑑定評価書情報",
        "path": f"{LIBRARY_API_URL}/XCT001",
        "response_type": "json",
    }

    def _call_api(self):
        # division分を回していく
        divisions = self.req_body.get("division", [None])
        results = {"data": []}
        # 都道府県CD
        muni_cd = self.converted["muni_cd"]
        area = muni_cd[:2]

        for div in divisions:
            # パラメータ生成
            headers = {
                "Ocp-Apim-Subscription-Key": f"{LIBRARY_API_KEY}",
                "Accept": "*/*",
            }
            params = {
                "year": self.req_body.get("year"),
                "area": area,
                "division": div,
            }

            # 外部API呼び出し
            try:
                response = requester.get(
                    url=self.API_CONFIG["path"],
                    params=params,
                    response_type=self.API_CONFIG["response_type"],
                    headers=headers,
                )
                # "data"キーがあり、中身がリストであることを確認
                data = response.get("data")
                if not data or not isinstance(data, list):
                    continue
                results["data"].extend(data)
            except Exception as e:
                self.logger.error(f"鑑定評価書情報API 呼び出し失敗:{e}")

        return results

    def _process_data(self, data):
        try:
            # APIから有効なデータが取得できなかった、またはdataキーがない、またはdataが空リストの場合
            if not data or "data" not in data or not data["data"]:
                self.logger.info("APIから有効なデータが取得できませんでした。")
                return None

            # json→geojsonへ変換、座標情報付与
            features = [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(item["位置座標 経度"]),
                            float(item["位置座標 緯度"]),
                        ],
                    },
                    "properties": item,
                }
                for item in data["data"]
            ]

            # 距離での絞り込み
            distance = self.req_body.get("distance")
            filtered_features = filter_distance(
                features=features,
                latlon=(self.converted["lat"], self.converted["lon"]),
                distance=distance,
            )
            if not filtered_features:
                self.logger.info(
                    "鑑定評価書情報APIの該当データなし（距離での絞り込み後）"
                )
                return None

            geojson = {"type": "FeatureCollection", "features": filtered_features}
            return geojson

        except Exception as e:
            self.logger.error(f"鑑定評価書情報API excange エラー:{e}")
            raise

```

### Z-14. real_estate_api3.py（代表：XPT002 地価公示）

```python
from request_processor.common import requester
from request_processor.common.point_filter import filter_distance, get_surrounding_tiles
from utils.const import LIBRARY_API_KEY, LIBRARY_API_URL, ZOOM
from utils.logger_config import setup_logger


class RealEstateApi3:
    API_CONFIG = {
        "name": "地価公示・地価調査のポイント（点）",
        "path": f"{LIBRARY_API_URL}/XPT002",
        "response_type": "geojson",
    }

    def __init__(self, req_body: dict, converted: dict):
        # ラムダから渡されたリクエストデータ
        self.req_body = req_body
        # 座標変換済データ
        self.converted = converted
        self.logger = setup_logger(__name__)

    def _call_get_api(self):
        # 4タイル分取得
        tiles = get_surrounding_tiles(
            self.converted["x"],
            self.converted["y"],
            self.converted["x_frac"],
            self.converted["y_frac"],
        )

        merged_geojson = {"type": "FeatureCollection", "features": []}

        for x, y in tiles:
            self.logger.info(f"ｘ：{x},y:{y}")
            # パラメータ生成
            headers = {
                "Ocp-Apim-Subscription-Key": f"{LIBRARY_API_KEY}",
                "Accept": "*/*",
            }
            params = {
                "response_format": "geojson",
                "z": ZOOM,
                "x": x,
                "y": y,
                "year": self.req_body.get("year"),
            }
            # 任意のパラメータ
            optional_param_mapping = {
                "priceClassification": "land_price_classification",
                "useCategoryCode": "use_category_code",
            }

            for api_key, req_key in optional_param_mapping.items():
                value = self.req_body.get(req_key)
                if value is not None:
                    if isinstance(value, list):
                        # リストをカンマ区切りの文字列に変換
                        params[api_key] = ",".join(map(str, value))
                    else:
                        params[api_key] = value

            # 外部API呼び出し
            try:
                response = requester.get(
                    url=self.API_CONFIG["path"],
                    params=params,
                    response_type=self.API_CONFIG["response_type"],
                    headers=headers,
                )
                if not response or not isinstance(response, dict):
                    continue

                features = response.get("features")
                if not features:
                    continue

                merged_geojson["features"].extend(features)

            except Exception as e:
                self.logger.error(
                    f"地価公示・地価調査のポイント（点） 呼び出し失敗:{e}"
                )

        return merged_geojson

    def exchange(self):
        self.logger.info("地価公示・地価調査のポイント（点） excange開始")
        try:
            # 外部APIにリクエストする
            data = self._call_get_api()

            # APIから有効なデータが取得できなかった場合
            if not data or not data.get("features"):
                self.logger.info("地価公示・地価調査のポイント（点）の該当データなし")
                return None

            # パラメータできた半径距離内にある情報を取得
            distance = self.req_body.get("distance")

            # 距離による絞り込み
            filtered_features = filter_distance(
                features=data["features"],
                latlon=(self.converted["lat"], self.converted["lon"]),
                distance=distance,
            )
            if not filtered_features:
                self.logger.info("地価公示・地価調査のポイント（点）の該当データなし")
                return None

            data["features"] = filtered_features

        except Exception as e:
            self.logger.error(f"地価公示・地価調査のポイント（点） excange エラー:{e}")
            return None

        return {
            "file_name": "地価公示・地価調査のポイント（点）.geojson",
            "data": data,
        }

```

---

*本書は v1.0。仕様変更・機能追加のたびに版を上げ、第16章・第18章へ追記すること。*
