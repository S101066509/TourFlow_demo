from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

def generate_order_number():
    date_str = timezone.now().strftime('%Y%m%d')
    random_str = uuid.uuid4().hex[:4].upper()
    return f"TG{date_str}{random_str}"

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="地點名稱")

    class Meta:
        db_table = 'tours_location'
        verbose_name = "目的地"
        verbose_name_plural = "目的地"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="標籤名稱")

    class Meta:
        db_table = 'tours_tag'
        verbose_name = "標籤"
        verbose_name_plural = "標籤"

    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="行程名稱")
    description = models.TextField(verbose_name="行程介紹")
    days = models.PositiveIntegerField(verbose_name="旅遊天數")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="目的地")
    image = models.ImageField(upload_to='tours/', null=True, blank=True, verbose_name="行程封面圖")
    tags = models.ManyToManyField(Tag, verbose_name="可多選標籤", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="上下架狀態")

    class Meta:
        db_table = 'tours_tour'
        verbose_name = "行程"
        verbose_name_plural = "行程"

    def __str__(self):
        return self.title

class Departure(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="關聯行程")
    start_date = models.DateField(verbose_name="出發日期")
    end_date = models.DateField(verbose_name="回程日期")
    price = models.PositiveIntegerField(verbose_name="單人售價")
    total_seats = models.PositiveIntegerField(verbose_name="總機位數量")
    available_seats = models.PositiveIntegerField(verbose_name="剩餘可售位數量")

    class Meta:
        db_table = 'tours_departure'
        verbose_name = "出發梯次"
        verbose_name_plural = "出發梯次"

    def __str__(self):
        return f"{self.tour.title} ({self.start_date})"

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number, verbose_name="訂單編號")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="會員")
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE, verbose_name="關聯梯次")
    contact_name = models.CharField(max_length=100, verbose_name="聯絡人姓名")
    contact_phone = models.CharField(max_length=50, verbose_name="聯絡人電話")
    contact_email = models.EmailField(verbose_name="聯絡人信箱")
    pax = models.PositiveIntegerField(
        verbose_name="報名人數",
        validators=[MinValueValidator(1)]
    )
    total_price = models.PositiveIntegerField(verbose_name="訂單總價")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        db_table = 'tours_order'
        verbose_name = "報名訂單"
        verbose_name_plural = "報名訂單"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
            # 確保唯一性 (避免碰撞)
            while Order.objects.filter(order_number=self.order_number).exists():
                self.order_number = generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.contact_name}"

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Banner 標題")
    # 圖片會上傳到 media/banners/ 目錄下
    image = models.ImageField(upload_to='banners/', verbose_name="Banner 圖片")
    link_url = models.CharField(max_length=500, blank=True, verbose_name="點擊跳轉網址")
    order = models.PositiveIntegerField(default=0, verbose_name="排序權重")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")

    class Meta:
        db_table = 'tours_banner'
        verbose_name = "首頁 Banner"
        verbose_name_plural = "首頁 Banner"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title
