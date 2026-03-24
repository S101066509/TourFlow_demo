from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # 使用預設登入機制
    path('accounts/', include('django.contrib.auth.urls')),
    # 引入 tours_app 的路由，邏輯主要由此路由進入
    path('', include('tours_app.urls')),
]
#開發階段的圖片路境設置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
