# TourFlow_demo Project

這是一個基於 Django 開發的簡單旅遊網站。

---

## 主要功能 

### 1. 搜尋功能
*   **條件篩選**：支援關鍵字、目的地、旅遊天數上限、專屬標籤以及出發時間等條件篩選。

### 2. 訪客或會員報名功能
*   **雙模式報名**：支援「會員登入」與「快速訪客」報名模式。
*   **庫存鎖定**：使用資料庫交易鎖 (Transaction Locks) 機制，確保不會產生超賣問題。
*   **注意**：本展示專案尚未加入金流串接相關服務。

### 3. 個人化報名記錄 Dashboard
*   **旅程記錄**：可查看所有歷史訂單。自動分類為「即將出發 (Upcoming)」與「回憶之旅 (History)」。
*   **訪客訂單查詢**：訪客輸入訂單編號和原聯絡信箱後，使用寄到該信箱的限時查詢碼查看訂單。既有訂單也適用。請在 `.env` 設定 SMTP 的 `EMAIL_HOST`、`EMAIL_PORT`、`DEFAULT_FROM_EMAIL`，以及郵件服務要求的 `EMAIL_HOST_USER`、`EMAIL_HOST_PASSWORD`、`EMAIL_USE_TLS` 或 `EMAIL_USE_SSL`。

### 4. 後台管理與動態 Banners
*   **django admin**：可從後台管理行程與訂單。

---

## Tech Stack

*   **後端框架**：Django 5.2 (Python 3.11+)
*   **資料庫**：PostgreSQL
*   **前端開發**：Django Template搭配Bootstrap 5.3的後端渲染模式 
*   **安全防護**：Django 內建密碼強度校驗與 CSRF 防護。

---

## 快速安裝與啟動

### 1. 安裝環境依賴
```bash
pip install -r requirements.txt
```

### 2. 環境變數設定
請複製 `.env.example` 並重新命名為 `.env`，填入您的資料庫資訊與 `SECRET_KEY`。
以下為env範例
`
SECRET_KEY="your-secret-key-here"
DEBUG=True
ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

```

### 3. 資料庫遷移與建檔
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 建立測試資料 
透過/script 內兩隻腳本進行假資料建立。
```bash
python seed_data.py            # 建立結構資料
python download_tour_images.py # 下載實體圖片
```

### 5. 啟動開發伺服器
```bash
python manage.py runserver
```
開啟瀏覽器進入 `http://127.0.0.1:8000/` 


