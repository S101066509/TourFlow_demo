import os
import django
from datetime import date, timedelta
import random

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tours_app.models import Location, Tag, Tour, Departure

print("開始建立大量測試資料...")

# 為了避免重複執行導致資料重複，先清除現有資料
Departure.objects.all().delete()
Tour.objects.all().delete()
Tag.objects.all().delete()
Location.objects.all().delete()

# 1. 建立多元地點
loc_names = ["日本", "韓國", "歐洲", "美洲", "東南亞", "紐澳"]
locations = {}
for name in loc_names:
    locations[name] = Location.objects.create(name=name)

print(f"建立 {len(locations)} 個目的地。")

# 2. 建立標籤
tag_hot = Tag.objects.create(name="熱門")
tag_guaranteed = Tag.objects.create(name="保證出團")
tag_sale = Tag.objects.create(name="促銷")
tag_new = Tag.objects.create(name="最新上架")
tag_family = Tag.objects.create(name="親子同遊")
all_tags = [tag_hot, tag_guaranteed, tag_sale, tag_new, tag_family]

print(f"建立 {len(all_tags)} 個標籤。")

# 3. 建立大量行程
tours_data = [
    # 日本
    ("東京5日暢遊", "體驗東京繁華與傳統之美，包含迪士尼樂園與淺草寺。", 5, "日本"),
    ("京都大阪賞楓", "千年古都與美食巡禮，體驗清水寺與道頓堀。", 6, "日本"),
    ("北海道雪國之旅", "粉雪滑雪體驗與夢幻雪祭，享受道地溫泉。", 5, "日本"),
    ("沖繩自駕4日", "享受熱帶風情與絕美海灘，品嚐黑豬肉料理。", 4, "日本"),
    ("九州湯布院溫泉", "搭乘特色列車，享受日本第一的溫泉鄉。", 5, "日本"),
    # 韓國
    ("首爾5日購物樂", "韓劇景點與東大門血拼，品嚐道地烤肉與泡菜。", 5, "韓國"),
    ("釜山海景風光", "海雲台沙灘與太宗台絕美海景。", 4, "韓國"),
    ("濟州島度假假期", "世界自然遺產與海島悠閒體驗。", 5, "韓國"),
    # 歐洲
    ("英法雙國10天", "倫敦大笨鐘與巴黎鐵塔，浪漫雙國深度遊。", 10, "歐洲"),
    ("德瑞仙境12天", "阿爾卑斯山脈與新天鵝堡夢幻城堡之旅。", 12, "歐洲"),
    ("義大利文藝復興", "羅馬競技場、佛羅倫斯烏菲茲與威尼斯水都。", 11, "歐洲"),
    ("東歐奧匈捷10日", "布拉格廣場與多瑙河遊船，感受中世紀風情。", 10, "歐洲"),
    # 美洲
    ("美西大峽谷8天", "一覽世界七大奇景，體驗拉斯維加斯不夜城。", 8, "美洲"),
    ("紐約時報廣場6日", "感受大蘋果的活力，欣賞百老匯音樂劇。", 6, "美洲"),
    ("加拿大洛磯山脈", "絕美冰河湖與壯麗山脈，尋找野生動物的蹤跡。", 9, "美洲"),
    # 東南亞
    ("泰國曼谷芭達雅", "水上市場與人妖秀，享受泰式古法按摩。", 5, "東南亞"),
    ("越南峴港會安5日", "走訪黃金橋與古鎮燈籠，體驗東方夏威夷。", 5, "東南亞"),
    ("峇里島浪漫度假", "叢林鞦韆與無邊際泳池，享受海島慢活時光。", 5, "東南亞"),
    # 紐澳
    ("澳洲雪梨黃金海岸", "歌劇院與無尾熊抱抱，體驗陽光與沙灘。", 8, "紐澳"),
    ("紐西蘭南北島10天", "魔戒拍攝地與螢火蟲洞，沉浸在純粹的自然環境。", 10, "紐澳"),
]

tours = []
for title, desc, days, loc_name in tours_data:
    tour = Tour.objects.create(
        title=title,
        description=desc,
        days=days,
        location=locations[loc_name],
        is_active=True
    )
    # 隨機分配 1 到 3 個標籤
    tour.tags.set(random.sample(all_tags, random.randint(1, 3)))
    tours.append(tour)

print(f"建立 {len(tours)} 個行程。")

# 4. 為每個行程建立多個出發梯次
today = date.today()
dep_count = 0

for tour in tours:
    # 每個行程隨機產生 4 ~ 8 個梯次
    num_deps = random.randint(4, 8)
    for i in range(num_deps):
        # 隨機決定出發日 (未來 10 天 ~ 180 天內)
        start_delay = random.randint(10, 180)
        start_date = today + timedelta(days=start_delay)
        end_date = start_date + timedelta(days=tour.days - 1)
        
        # 根據天數與地區亂數決定合理的價格
        base_price = tour.days * random.randint(3000, 6000)
        price = round(base_price, -3) # 四捨五入到千位
        
        # 決定位子數量
        total_seats = random.choice([15, 20, 25, 30, 40])
        # 決定剩餘座位 (從0到全部)
        available_seats = random.randint(0, total_seats)
        
        Departure.objects.create(
            tour=tour,
            start_date=start_date,
            end_date=end_date,
            price=price,
            total_seats=total_seats,
            available_seats=available_seats
        )
        dep_count += 1

print(f"建立 {dep_count} 個出發梯次。")
print(f"🎉 測試資料擴充完成！總計 {len(locations)} 地點, {len(all_tags)} 標籤, {len(tours)} 行程, {dep_count} 梯次。")
