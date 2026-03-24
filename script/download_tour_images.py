import os
import django
import urllib.request

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from tours_app.models import Tour

print("開始下載與綁定實體圖片...")

tours_dir = os.path.join(settings.MEDIA_ROOT, 'tours')
os.makedirs(tours_dir, exist_ok=True)

# 為每個「行程」準備專屬的高畫質 Unsplash 圖片網址，確保每個行程不會長得一模一樣
tour_image_map = {
    # 日本
    "東京5日暢遊": "https://images.unsplash.com/photo-1542051845915-d3ec4614ff73?w=1200&h=800&fit=crop", 
    "京都大阪賞楓": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200&h=800&fit=crop", 
    "北海道雪國之旅": "https://images.unsplash.com/photo-1510008851416-5fbac458eb03?w=1200&h=800&fit=crop", 
    "沖繩自駕4日": "https://images.unsplash.com/photo-1596489392224-bca2626d0bbd?w=1200&h=800&fit=crop", 
    "九州湯布院溫泉": "https://images.unsplash.com/photo-1624253321171-1be53e12f5f4?w=1200&h=800&fit=crop", 
    # 韓國
    "首爾5日購物樂": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1200&h=800&fit=crop", 
    "釜山海景風光": "https://images.unsplash.com/photo-1620022756611-e63cc72338f0?w=1200&h=800&fit=crop", 
    "濟州島度假假期": "https://images.unsplash.com/photo-1624445859341-a1286f3bb915?w=1200&h=800&fit=crop", 
    # 歐洲
    "英法雙國10天": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&h=800&fit=crop", 
    "德瑞仙境12天": "https://images.unsplash.com/photo-1527668752968-14dc70a27c95?w=1200&h=800&fit=crop", 
    "義大利文藝復興": "https://images.unsplash.com/photo-1515542622106-78b28af7815d?w=1200&h=800&fit=crop", 
    "東歐奧匈捷10日": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=1200&h=800&fit=crop", 
    # 美洲
    "美西大峽谷8天": "https://images.unsplash.com/photo-1474044159687-1ee9f3a51722?w=1200&h=800&fit=crop", 
    "紐約時報廣場6日": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1200&h=800&fit=crop", 
    "加拿大洛磯山脈": "https://images.unsplash.com/photo-1550586678-f7225b1eeae6?w=1200&h=800&fit=crop", 
    # 東南亞
    "泰國曼谷芭達雅": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1200&h=800&fit=crop", 
    "越南峴港會安5日": "https://images.unsplash.com/photo-1534971701383-7c25143a41e9?w=1200&h=800&fit=crop", 
    "峇里島浪漫度假": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&h=800&fit=crop", 
    # 紐澳
    "澳洲雪梨黃金海岸": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200&h=800&fit=crop", 
    "紐西蘭南北島10天": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&h=800&fit=crop"
}

# 為了防止 Unsplash 阻擋，加上 User-Agent 標頭
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

tours = Tour.objects.all()
for tour in tours:
    # 針對行程「名稱」提取圖片，沒對應到就給預設大圖
    img_url = tour_image_map.get(tour.title, "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&h=800&fit=crop")
    
    file_name = f"tour_{tour.id}.jpg"
    local_path = os.path.join(tours_dir, file_name)
    
    print(f"正在為 [ {tour.title} ] 重新下載專屬圖片...")
    try:
        urllib.request.urlretrieve(img_url, local_path)
        # 更新資料庫紀錄 (只存取相對路徑 tours/xxx.jpg)
        tour.image = f"tours/{file_name}"
        tour.save()
        print(f"✅ 成功綁定圖片：{tour.image}")
    except Exception as e:
        print(f"❌ 下載失敗：{e}，使用備用圖...")
        fallback_url = "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&h=800&fit=crop"
        urllib.request.urlretrieve(fallback_url, local_path)
        tour.image = f"tours/{file_name}"
        tour.save()

print("所有行程圖片均已下載並儲存至資料庫關聯！")
