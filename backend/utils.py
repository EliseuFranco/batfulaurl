import requests
import jwt
from functools import wraps
import datetime 
from fastapi import Request
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
import os


SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
GEO_IFY_SECRET_KEY = os.environ.get('GEO_IFY_SECRET_KEY')

def get_client_data(ip):

    try:
        request = requests.get(f'https://geo.ipify.org/api/v2/country,city?apiKey={GEO_IFY_SECRET_KEY}&ipAddress={ip}')
        data = request.json()
        return data
        
    except requests.exceptions.Timeout:
        return {'error': 'Tempo de resposta da api excedido'}
    
    except requests.exceptions.ConnectTimeout as e:
        return {'error': 'Tempo de resposta da api excedido'}
    
    except Exception as e:
        return {'error': 'Houve um erro ao obter dados do client', 'error_type': str(e)}
   

def get_metric_number(values):

    if not values:
        return 0
    for value in values:
        return value


def create_exp_timestamp(hour = 1):

    try:
        return datetime.datetime.timestamp(datetime.datetime.today().now() + datetime.timedelta(hours=hour))

    except Exception as e:
        print('Algo correu mal ao criar tempo de expiração', str(e))
        return 'erro ao criar tempo de expiração'

def create_token(payload):

    try:
        header = {
            'algorithm': 'HS256',
            'type': 'JWT'
            }
        token = jwt.encode(headers=header, key=SECRET_KEY, payload=payload)
        return token

    except Exception as e:
        print('Erro ao gerar token')
        return {'msg': 'Houve um erro ao gerar o token', 'erro': str(e)}


def token_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):

        request : Request = kwargs.get('request') or args[0]

        try:
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer '):
                return {'msg': 'Token mal formatado'}
            
            token = auth_header.split(' ')[-1]

            user_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms='HS256')
            request.state.user_id = user_data['id']
            return await fn(*args, **kwargs)
        
        except jwt.exceptions.ExpiredSignatureError as e:
            return {'msg': 'Token expirado faça login'}
        except jwt.exceptions.DecodeError as e:
            return {'msg': 'Token inválido'}
        except Exception as e:
            return {'msg':'Houve um erro ao obter usuário', 'erro': str(e)}
        
    return wrapper


def get_year_month_day(date_time):
    print(date_time)
    return date_time.strftime('%d/%m/%Y')


def generate_shorten_url(slug, url):

    schema = urlparse(url).scheme
    shorten_url = f'{schema}://urlcurta.com/{slug}'
    return shorten_url


def serialize_urls(urls):
    allUrls = []

    if not urls:
        return []
    
    for url in urls:
        id, slug, data, original_url, unique_clicks , total_clicks = url
        allUrls.append({'id': id, 'data': data,'slug':slug, 'original_url': original_url, 'shortened_url': generate_shorten_url(slug=slug, url=original_url) ,'unique_clicks': unique_clicks, 'total_clicks': total_clicks})
    
    return allUrls

def serialize_7d_clicks(urls):
    return [{'data': url[0], 'clicks':url[1]} for url in urls]

def serialize_device(devices):
    return [{device[0]: device[1]} for device in devices]


def serialize_cities(city_data):
    data = []

    for city in city_data:
        city_name , hour, total_clicks , unique_clicks = city
        data.append({'city': city_name, 'hour': int(hour) + 1 , 'total_clicks': total_clicks, 'unique_clicks': unique_clicks})
    
    return data
