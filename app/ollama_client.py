import requests
from flask import current_app

# Build the Farsi research method prompt based on user responses
def build_prompt(responses: dict) -> str:
    joined_tools = ", ".join(responses.get("2", [])) if isinstance(responses.get("2", []), list) else responses.get("2", "")
    return f"""
شما یک پژوهشگر حرفه‌ای هستید و وظیفه دارید بر اساس پاسخ‌های زیر، یک گزارش کامل و دقیق از روش تحقیق ارائه دهید.

پاسخ‌های کاربر به سوالات طراحی تحقیق به شرح زیر است:

1. موضوع تحقیق و دلیل انتخاب آن:
{responses.get("0", "")}

2. منابع بررسی‌شده و یافته‌های کلیدی:
{responses.get("1", "")}

3. ابزارهای گردآوری داده:
{joined_tools}

4. نوع روش تحقیق انتخاب‌شده:
{responses.get("3", "")}

5. روش تحلیل داده‌ها:
{responses.get("4", "")}

6. مدت زمان و چالش‌های احتمالی:
{responses.get("5", "")}

لطفاً با توجه به اطلاعات بالا، یک تحلیل دقیق و ساختارمند از روش تحقیق این فرد ارائه دهید. گزارش شما باید شامل بخش‌های زیر باشد:

- بیان مسئله و ضرورت تحقیق  
- نوع تحقیق و رویکرد کلی آن  
- روش گردآوری داده‌ها و دلیل انتخاب ابزارها  
- شیوه تحلیل داده‌ها و توجیه انتخاب آن  
- مدت زمان و برنامه زمانی تحقیق  
- چالش‌های پیش‌رو و پیشنهادهایی برای رفع آن‌ها  

خروجی را به زبان فارسی، رسمی، و قابل استفاده در یک پروپوزال دانشگاهی بنویسید.
"""

# Call the Ollama API to get a response from Qwen model
def call_ollama(prompt: str) -> str:
    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {"role": "system", "content": "شما یک دستیار تحقیقاتی هستید."},
            {"role": "user", "content": prompt}
        ]
    }
    url = current_app.config['OLLAMA_URL']
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("message", {}).get("content", "")