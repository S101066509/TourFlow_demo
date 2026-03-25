from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Min
from django.contrib import messages
from django.urls import reverse
from datetime import date
from django.db import transaction
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Tour, Departure, Location, Tag, Order, Banner
from .forms import OrderForm
#=======================首頁=======================
def home(request):
    """
    4.1 首頁 (Home Page)
    大圖輪播與搜尋表單。可以先呈現精選的幾項熱門行程。
    """
    locations = Location.objects.all()
    # 呈現首頁幾個精選的Tour (例如前 3 個)
    featured_tours = Tour.objects.filter(is_active=True).order_by('-id')[:3]
    # 取得啟用的 Banner
    banners = Banner.objects.filter(is_active=True)
    
    return render(request, 'tours_app/home.html', {
        'locations': locations,
        'featured_tours': featured_tours,
        'banners': banners
    })
#=======================搜尋功能=======================
def search(request):
    """
    4.2 搜尋成果頁 (Search Results)
    接收 GET 參數，使用model內的 Q 物件 與 annotate 等進行篩選及排序。
    """
    q = request.GET.get('q', '')
    location_id = request.GET.get('location', '')
    sort = request.GET.get('sort', '')
    days = request.GET.get('days', '')
    tag_id = request.GET.get('tag', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    today = date.today()

    # 基礎 QuerySet：僅顯示有“未來” 且 “有位子”梯次的行程
    tours = Tour.objects.filter(
        is_active=True,                     #上架中
        departure__start_date__gte=today,   #日期大於今天
        departure__available_seats__gt=0    #數量大於0
    ).annotate(
        min_price=Min('departure__price'),  #取最小價格
        first_departure=Min('departure__start_date') #取最早日期
    ).distinct()
    
    #根據條件做篩選
    if q:
        tours = tours.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q)
        )
    
    if location_id:
        tours = tours.filter(location_id=location_id)
        
    if days:
        try:
            tours = tours.filter(days__lte=int(days))
        except ValueError:
            pass

    if tag_id:
        tours = tours.filter(tags__id=tag_id)

    if start_date_str:
        try:
            tours = tours.filter(departure__start_date__gte=start_date_str)
        except (ValueError, TypeError):
            pass

    if end_date_str:
        try:
            tours = tours.filter(departure__start_date__lte=end_date_str)
        except (ValueError, TypeError):
            pass

    # 依照要求進行排序
    if sort == 'price_asc':
        tours = tours.order_by('min_price')
    elif sort == 'price_desc':
        tours = tours.order_by('-min_price')
    elif sort == 'date_asc':
        tours = tours.order_by('first_departure')
    else:
        # 預設排序：最新的行程在前
        tours = tours.order_by('-id')
    #查出全部的地點與標籤
    locations = Location.objects.all()
    tags = Tag.objects.all()
    # 將結果傳回 search.html
    return render(request, 'tours_app/search.html', {
        'tours': tours,
        'q': q,
        'location_id': location_id,
        'sort': sort,
        'days': days,
        'tag_id': tag_id,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'locations': locations,
        'tags': tags,
    })

#=======================行程詳細=======================
def tour_detail(request, pk):
    """
    4.3 行程詳細與日期選擇頁 (Tour Detail)
    """
    tour = get_object_or_404(Tour, pk=pk, is_active=True)
    today = date.today()
    
    # 找出該行程所有未過期且 available_seats > 0 的 Departure
    departures = Departure.objects.filter(
        tour=tour,
        start_date__gte=today,
        available_seats__gt=0
    ).order_by('start_date')

    return render(request, 'tours_app/tour_detail.html', {
        'tour': tour,
        'departures': departures
    })

#=======================訂單=======================
#套上交易原子性
@transaction.atomic 
def checkout(request, departure_id):
    """
    4.4 訂單資料填寫頁 (Checkout) - 雙軌處理
    """
    # 如果是不允許報名的狀況 (人數滿或時間過)，這裡可以做阻擋 (或者在 POST 時擋)
    # 使用 select_for_update 避免併發 (Concurrency) 扣庫存的問題 (交易安全)
    departure = get_object_or_404(
        Departure.objects.select_for_update(), 
        pk=departure_id, 
        start_date__gte=date.today()
    )
    
    # 1. 資料預填
    initial_data = {}
    if request.user.is_authenticated:
        # 從 Django standard User 取名字
        name = f"{request.user.last_name}{request.user.first_name}"
        if not name.strip():
            name = request.user.username
            
        initial_data = {
            'contact_name': name,
            'contact_email': request.user.email,
        }

    if request.method == 'POST':
        #透過OrderForm產生表單實體，該表單是由自己定義。
        form = OrderForm(request.POST)
        if form.is_valid():
            pax = form.cleaned_data['pax']
            
            # 2. 庫存防呆
            if pax > departure.available_seats:
                form.add_error('pax', f'很抱歉，報名人數({pax}人) 不可大於剩餘機位({departure.available_seats}個)')
            else:
                order = form.save(commit=False)
                # 3. 訂單綁定 (若為訪客則保持 None)
                if request.user.is_authenticated:
                    order.user = request.user
                
                order.departure = departure
                order.total_price = departure.price * pax
                
                # 4. 扣除庫存並存檔
                departure.available_seats -= pax
                departure.save()
                order.save()
                
                return redirect('booking_success', order_number=order.order_number)
    else:
        form = OrderForm(initial=initial_data)

    return render(request, 'tours_app/checkout.html', {
        'form': form,
        'departure': departure
    })

#=======================註冊=======================
def register(request):
    """
    及時註冊頁面 (Registration)
    """
    if request.method == 'POST':
        #透過UserCreationForm產生表單實體，本身已具有帳號 密碼 密碼確認等模板。
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 註冊成功後直接自動登入
            login(request, user)
            messages.success(request, f'註冊成功，歡迎 {user.username}！')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'tours_app/register.html', {'form': form})

#=======================報名成功=======================
def booking_success(request, order_number):
    """
    報名成功頁面
    """
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'tours_app/booking_success.html', {'order': order})

#=======================報名查詢=======================
def booking_search(request):
    """
    報名紀錄查詢頁面
    - 已登入會員：列出所有訂單並分類為未來/歷史行程。
    - 訪客：提供訂單編號查詢機制。
    """
    # 1. 已登入會員邏輯
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
        today = date.today()
        
        future_orders = []
        past_orders = []
        for order in user_orders:
            if order.departure.start_date > today:
                future_orders.append(order)
            else:
                past_orders.append(order)
                
        return render(request, 'tours_app/booking_search.html', {
            'future_orders': future_orders,
            'past_orders': past_orders,
            'is_auth_search': True
        })
        
    # 2. 訪客查詢邏輯
    #先設定預設值，用於初始渲染，因為回傳有  'order': order
    order = None
    error_msg = None
    is_future = None
    
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip()
        if order_number:
            try:
                order = Order.objects.get(order_number=order_number)
                is_future = order.departure.start_date > date.today()
            except Order.DoesNotExist:
                error_msg = "查無此訂單編號，請重新確認。"
        else:
            error_msg = "請輸入訂單編號。"
            
    return render(request, 'tours_app/booking_search.html', {
        'order': order,
        'error_msg': error_msg,
        'is_future': is_future,
        'is_auth_search': False
    })


#=======================施工中頁面=======================
def wip(request):
    """施工中頁面"""
    return render(request, 'tours_app/wip.html')