import requests
from django.conf import settings

logger = settings.LOGGER


def get_client_ip(request):
    """
    요청의 'HTTP_X_FORWARDED_FOR'이나 'REMOTE_ADDR'을 이용해 유저 IP 얻어 내는 함수
    return: ip(str) | None
    """
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_weather_info(request):
    """
    weather api(https://www.weatherapi.com/) 에서
    유저가 있는 곳(IP 기준, default=Seoul)의 현재 날씨 받아 오는 함수

    return: current_weather(str)
    에러 발생시 None 반환
    """
    client_info = get_client_ip(request)
    if not client_info:
        client_info = 'Seoul'

    url = 'http://api.weatherapi.com/v1'
    api = '/current.json'
    params = {
        'key': settings.WEATHER_API_KEY,
        'q': client_info,
        'lang': 'ko',
    }
    response = requests.get(f'{url}{api}', params=params).json()

    # weather api error 처리
    if 'error' in response:
        error_code = response['error']['code']
        error_message = response['error']['message']
        logger.error(f"ERROR: weather API [ERR {error_code}] {error_message}")
        return None

    current_weather = response['current']['condition']['text']
    return current_weather


