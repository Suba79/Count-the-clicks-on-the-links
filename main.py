import os
from dotenv import load_dotenv
from vk_api import is_shorten_link, shorten_link, count_clicks

load_dotenv()

def main():
    token = os.getenv('VK_API_TOKEN')
    
    if not token:
        print("Токен не найден. Проверьте файл .env")
        return
    
    user_input = input("Введите ссылку: ").strip()
    
    if not user_input:
        print("Вы не ввели ссылку!")
        return
    
    if not user_input.startswith(('http://', 'https://')):
        user_input = 'https://' + user_input
    
    try:
        if is_shorten_link(user_input):
            clicks = count_clicks(token, user_input)
            print(f"Количество кликов: {clicks}")
        else:
            short_url = shorten_link(token, user_input)
            clicks = count_clicks(token, short_url)
            print(short_url)
            print(f"Количество кликов: {clicks}")
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()