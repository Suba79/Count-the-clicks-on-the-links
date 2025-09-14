import requests
from urllib.parse import urlparse

def is_shorten_link(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc == 'vk.cc' and bool(parsed_url.path.strip('/'))
    except:
        return False

def shorten_link(token, url):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.199',  
        'url': url,
        'private': 0
    }
    
    response = requests.get(api_url, params=params)
    result = response.json()
    
    if 'error' in result:
        error_code = result['error'].get('error_code')
        error_msg = result['error'].get('error_msg')
        if error_code == 100:
            raise Exception("Неверная ссылка. Проверьте правильность ввода.")
        else:
            raise Exception(f"Ошибка API ({error_code}): {error_msg}")
    
    if 'response' in result:
        return result['response']['short_url']
    else:
        raise Exception("Неизвестная ошибка при сокращении ссылки")

def count_clicks(token, short_url):
    parsed_url = urlparse(short_url)
    link_key = parsed_url.path.strip('/')
    
    if '/' in link_key:
        link_key = link_key.split('/')[-1]
    
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link_key,
        'interval': 'forever'
    }
    
    response = requests.get(api_url, params=params)
    result = response.json()
    
    if 'error' in result:
        error_code = result['error'].get('error_code')
        error_msg = result['error'].get('error_msg')
        raise Exception(f"Ошибка при получении статистики ({error_code}): {error_msg}")
    
    if 'response' in result:
        stats = result['response'].get('stats', [])
        return stats[0].get('views', 0) if stats else 0
    else:
        raise Exception("Неизвестная ошибка при получении статистики")