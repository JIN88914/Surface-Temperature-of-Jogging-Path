
import requests
import polyline
import csv
from math import cos, radians
from google.colab import files

# 配置
ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"  # 替換為你的 Strava Access Token
BASE_URL_EXPLORE = "https://www.strava.com/api/v3/segments/explore"
BASE_URL_SEGMENT = "https://www.strava.com/api/v3/segments/{id}"

# 台北小巨蛋中心座標
CENTER_LAT, CENTER_LON = 25.0514, 121.5511
RADIUS_KM = 4  # 半徑 4 公里

# 計算緯度與經度步長
LAT_DELTA = 1.5 / 111  # 緯度每步長 1.5 公里
LON_DELTA = 1.5 / (111 * cos(radians(CENTER_LAT)))  # 經度需考慮緯度縮放

# 計算初始範圍
lat_min, lon_min = CENTER_LAT - RADIUS_KM / 111, CENTER_LON - RADIUS_KM / (111 * cos(radians(CENTER_LAT)))
lat_max, lon_max = CENTER_LAT + RADIUS_KM / 111, CENTER_LON + RADIUS_KM / (111 * cos(radians(CENTER_LAT)))

# 初始化結果
segments_with_points = {}

# 分塊搜尋
lat = lat_min
while lat < lat_max:
    lon = lon_min
    while lon < lon_max:
        # 計算子區域邊界
        sub_bounds = f"{lat},{lon},{lat + LAT_DELTA},{lon + LON_DELTA}"

        # 發送請求
        response = requests.get(BASE_URL_EXPLORE, params={
            "bounds": sub_bounds,
            "access_token": ACCESS_TOKEN
        })

        if response.status_code == 200:
            sub_segments = response.json().get("segments", [])
            for segment in sub_segments:
                segment_id = segment["id"]

                # 避免重複請求已處理過的 Segment
                if segment_id not in segments_with_points:
                    # 獲取每段 Segment 詳細資訊
                    segment_response = requests.get(BASE_URL_SEGMENT.format(id=segment_id), params={
                        "access_token": ACCESS_TOKEN
                    })

                    if segment_response.status_code == 200:
                        segment_data = segment_response.json()
                        polyline_encoded = segment_data.get("map", {}).get("polyline", "")

                        if polyline_encoded:
                            points = polyline.decode(polyline_encoded)
                            segments_with_points[segment_id] = {
                                "name": segment_data["name"],
                                "points": points
                            }

        lon += LON_DELTA
    lat += LAT_DELTA

# 設定檔案名為當前工作目錄
output_file = "segments_with_points.csv"

# 將資料寫入 CSV 檔案
try:
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # 寫入標題行
        writer.writerow(["Segment ID", "Name", "Point Index", "Latitude (Y)", "Longitude (X)"])

        # 寫入每個 Segment 的資料
        for segment_id, segment in segments_with_points.items():
            for idx, (lat, lon) in enumerate(segment["points"]):
                writer.writerow([segment_id, segment["name"], idx, lat, lon])

    print(f"Total Segments with Points: {len(segments_with_points)}")
    print(f"Data saved to {output_file}")

    # 自動下載 CSV 檔案
    files.download(output_file)

except Exception as e:
    print(f"Error saving file: {e}")