import os
import requests
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("کلیدهای SUPABASE_URL یا SUPABASE_KEY یافت نشدند!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_divar_cars():
    url = "https://api.divar.ir/v8/web-search/anzali/car"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        widgets = data.get('web_widgets', {}).get('post_list', [])
        if not widgets:
            widgets = data.get('widget_list', [])
            
        print(f"تعداد آگهی‌های یافت شده: {len(widgets)}")
        
        for widget in widgets:
            data_dict = widget.get('data', {})
            title = data_dict.get('title', '')
            
            if any(term in title for term in ["منطقه آزاد", "گذر موقت", "انزلی"]):
                price = data_dict.get('middle_description_text', 'توافقی')
                token = data_dict.get('action', {}).get('payload', {}).get('token', '')
                image_url = data_dict.get('image_url', '')
                source_url = f"https://divar.ir/v/{token}" if token else f"https://divar.ir/{title}"
                
                plate_type = "منطقه آزاد انزلی" if "منطقه آزاد" in title else "گذر موقت"
                
                car_data = {
                    "title": title,
                    "price": price,
                    "plate_type": plate_type,
                    "images": [image_url] if image_url else [],
                    "source_url": source_url,
                    "is_active": True
                }
                
                try:
                    supabase.table("cars").upsert(car_data).execute()
                    print(f"با موفقیت ثبت شد: {title}")
                except Exception as db_err:
                    print(f"خطا در ثبت دیتابیس برای {title}: {db_err}")
                    
    except Exception as e:
        print(f"خطای اصلی: {e}")

if __name__ == "__main__":
    fetch_divar_cars()
