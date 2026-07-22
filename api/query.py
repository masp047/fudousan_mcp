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
