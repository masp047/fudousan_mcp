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
