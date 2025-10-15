import requests
from urllib.parse import urlparse


class VKAPIError(Exception):
    pass


def is_shorten_link(token, url):
    parsed_url = urlparse(url)

    if parsed_url.netloc != 'vk.cc' or not parsed_url.path.strip('/'):
        return False

    link_key = parsed_url.path.strip('/').split('/')[-1]

    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link_key,
        'interval': 'forever'
    }
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    
    api_response = response.json()

    if 'error' in api_response and api_response['error'].get('error_code') == 100:
        return False
        
    return True


def shorten_link(token, url):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.199',  
        'url': url,
        'private': 0
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    api_response = response.json()

    if 'error' in api_response:
        error_code = api_response['error'].get('error_code')
        error_msg = api_response['error'].get('error_msg')
        if error_code == 100:
            raise VKAPIError("Неверная ссылка. Проверьте правильность ввода.")
        raise VKAPIError(f"Ошибка API ({error_code}): {error_msg}")
    
    if 'response' not in api_response:
        raise VKAPIError("Неизвестная ошибка при сокращении ссылки")
    
    return api_response['response']['short_url']


def count_clicks(token, short_url):
    parsed_url = urlparse(short_url)
    
    link_key = parsed_url.path.strip('/').split('/')[-1]
    
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link_key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    api_response = response.json()

    if 'error' in api_response:
        error_code = api_response['error'].get('error_code')
        error_msg = api_response['error'].get('error_msg')
        raise VKAPIError(f"Ошибка при получении статистики ({error_code}): {error_msg}")

    if 'response' not in api_response:
        raise VKAPIError("Неизвестная ошибка при получении статистики")
    
    stats = api_response['response'].get('stats', [])
    return stats[0].get('views', 0) if stats else 0


def main():
    
    token = "your_token_here"
    
    try:
        url = "https://vk.cc/example"
        is_short = is_shorten_link(token, url)
        print(f"Является короткой ссылкой: {is_short}")

        long_url = "https://example.com"
        short_url = shorten_link(token, long_url)
        print(f"Сокращенная ссылка: {short_url}")
        
        clicks = count_clicks(token, short_url)
        print(f"Количество кликов: {clicks}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
    except VKAPIError as e:
        print(f"Ошибка VK API: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
