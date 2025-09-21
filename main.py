import os
import requests
from dotenv import load_dotenv
from vk_api import is_shorten_link, shorten_link, count_clicks, VKAPIError


def main():
    load_dotenv()

    token = os.getenv('VK_API_TOKEN')

    if not token:
        print("Токен не найден. Проверьте файл .env")
        return

    user_input = input("Введите ссылку: ").strip()

    if not user_input:
        print("Вы не ввели ссылку!")
        return

    try:
        if is_shorten_link(token, user_input):
            clicks = count_clicks(token, user_input)
            print(f"Количество кликов: {clicks}")
        else:
            short_url = shorten_link(token, user_input)
            print(short_url)

    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
    except VKAPIError as e:
        print(f"Ошибка VK API: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
