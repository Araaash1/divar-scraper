import os
import requests
from supabase import create_client, Client

# کلیدهای دیتابیس از تنظیمات امنیتی خوانده می‌شوند
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_divar_cars():
    # لینک جستجوی دیوار برای خودروهای منطقه آزاد و انزلی
    url = "https://api.divar.ir/v8/web-search/anzali/car"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        widgets = data.get('widget_list', [])
        print(f"تعداد آگهی‌های دریافت شده: {len(widgets)}")
        
        for widget in widgets:
            if widget.get('widget_type') == 'POST_ROW':
                data_dict = widget.get('data', {})
                title = data_dict.get('title', '')
                
                # فیلتر کردن آگهی‌های مربوط به منطقه آزاد و گذر موقت
                if "منطقه آزاد" in title or "گذر موقت" in title or "انزلی" in title:
                    price = data_dict.get('middle_description_text', 'توافقی')
                    token = data_dict.get('action', {}).get('payload', {}).get('token', '')
                    image_url = data_dict.get('image_url', '')
                    source_url = f"https://divar.ir/v/{token}" if token else ""
                    
                    plate_type = "منطقه آزاد انزلی" if "منطقه آزاد" in title else "گذر موقت"
                    
                    # ذخیره در دیتابیس Supabase
                    car_data = {
                        "title": title,
                        "price": price,
                        "plate_type": plate_type,
                        "images": [image_url] if image_url else [],
                        "source_url": source_url,
                        "is_active": True
                    }
                    
                    # بررسی تکراری نبودن و ثبت در دیتابیس
                    supabase.table("cars").upsert(car_data, on_conflict="source_url").execute()
                    print(f"ثبت شد: {title}")
                    
    except Exception as e:
        print(f"خطا در دریافت داده‌ها: {e}")

if __name__ == "__main__":
    fetch_divar_cars()
