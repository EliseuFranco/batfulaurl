import requests
import jwt
from functools import wraps
from datetime import datetime, timedelta


SECRET_KEY = '43wesazxcvbghj'

def get_client_data(ip):

    try:
        request = requests.get(f'https://geo.ipify.org/api/v2/country,city?apiKey=at_kp1RbpHZoD8Xi5EWwt6nbCVAcaOKG&ipAddress={ip}')
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
        return datetime.timestamp(datetime.today().now() + timedelta(hours=hour))

    except Exception as e:
        print('Algo correu mal ao criar tempo de expiração')
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
    def wrapper(*args, **kwargs):

        if 'token' not in kwargs:
            return 'Acesso negado ou token expirado'
        
        try:
            user_data = jwt.decode(jwt=kwargs.get('token'), key=kwargs.get('key'), algorithms='HS256')
            return fn(user_data)
        
        except jwt.exceptions.ExpiredSignatureError as e:
            return 'Token expirado faça login'
        except jwt.exceptions.DecodeError as e:
            return 'Token inválido'
        except Exception as e:
            return 'Houve um erro ao obter usuário'
    return wrapper


@token_required
def admin_template(data):
    return 'Administrador: ', data

exp = create_exp_timestamp()
token = create_token({'id':1, 'nome':'Eliseu', 'role':'admin', 'exp': exp})

res = admin_template(token = token, key='43wesazxcvbghj')
print(res)


print(create_exp_timestamp())




# def higger(fn):
#     def wrapper(data):
#         return fn(data)
#     return wrapper

# @higger
# def soma(numero : list):
#     return sum(numero)


# res = soma([1,3,4,5,2])
# print(res)