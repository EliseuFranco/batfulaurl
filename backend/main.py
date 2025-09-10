from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select, delete, update, func, distinct, and_
from typing import Annotated, Optional
from urllib.parse import urlparse
from random import choice
from string import ascii_letters , digits
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .utils import *
from models.urls_model import URLS
from models.clicks_model import Clicks
from models.user_model import Users
from .services import *
from math import ceil
from user_agents import parse




class UrlRequest(BaseModel):
    url : str

class ShortenUrlRequest(BaseModel):
    shorten : str

class RegisterData(BaseModel):

    nome : Optional[str]
    email : Optional[str]
    password_hash : Optional[str]


class LoginData(BaseModel):
    email: str
    password_hash : str


class Pagination(BaseModel):
    page : int 

db_name = 'url_db.db'
DATABASE_URL = os.getenv("DATABASE_URL")
database_url = "postgresql://batfula_db_5vse_user:QqmjbNAaQXo8a5a7wJ1WueXQFuHWftK4@dpg-d2vop6odl3ps739dq4pg-a.oregon-postgres.render.com/batfula_db_5vse"
#f'sqlite:///backend/{db_name}' 

connect_args = {"check_same_thread": False} #Apenas funciona para SQLITE
engine = create_engine(database_url)



def db_create_all():
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create_all()
    yield


sessionDP = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

origins = [
    'http://localhost:5173',
    "https://batfulaurl-frontend.onrender.com",
    "https://batfulaurl.vercel.app",
    'https://batfulaurl-git-main-eliseu-samulolos-projects.vercel.app',
    "https://batfulaurl-ek7u9n2b4-eliseu-samulolos-projects.vercel.app",
    'https://batfulaurl.onrender.com'

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_url(url):
    url_parts = urlparse(url)
    return url_parts.scheme in ['http', 'https'] and bool(url_parts.netloc)


def generate_slug(exists_slugs: dict):

    alpha_num = ascii_letters + digits
    while True:
        new_slug = ''.join(choice(alpha_num) for _ in range(6))
        if new_slug not in exists_slugs:
            return new_slug


def generate_shorten_url(slug, url):

    schema = urlparse(url).scheme
    shorten_url = f'{schema}://urlcurta.com/{slug}'
    return shorten_url


def get_original_url(short_url : str, dict_slugs : dict):
    
    try:
        slug = short_url.split('/')[-1]
        return dict_slugs.get(slug, False)

    except Exception as e:
        print("Houve um erro inesperado", str(e))
        return {'error': 'Erro ao obter a url'}
    


@app.post('/create_shorten_url')
async def create_shorten_url(req : UrlRequest, session: sessionDP, request : Request):
    import jwt
    try:
        url = req.url
        user_id = None
        token = ''
        SECRET_KEY = '43wesazxcvbghj'

        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ','')

            try:
                user_d = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')
                user_id = user_d['id']
            
            except Exception as e:
                user_id = None
                
        if not check_url(url):
            return {'error': 'URL inválida'}
        
        existing = session.exec(select(URLS).where(URLS.original_url == url)).first()
        
        if existing:
            return {'shorten_url': generate_shorten_url(existing.slug, url), 'msg': 'Já existe uma url encurtada para essa url'}
        
        exists_slugs = {row.slug : row.original_url for row in session.exec(select(URLS))} or {}
        slug = generate_slug(exists_slugs)

        shorten_url = generate_shorten_url(slug, url=req.url)

        new_slug = URLS(slug=slug, original_url=url, user_id=user_id)
        session.add(new_slug)
        session.commit()
        return {'msg': f'Url criada com sucesso', 'shortened_url': f'{shorten_url}', 'original_url': url, 'click': 20}
    
    except Exception as e:
        print('O erro é: ', str(e))
        session.rollback()
        return {'msg': 'Houve um erro ao criar a ulr'}



@app.post('/original_url')
async def original_url(request : ShortenUrlRequest, session : sessionDP):

    try:
        shorten_url = request.shorten

        all_slugs = {row.slug : row.original_url for row in session.exec(select(URLS))}
        original = get_original_url(shorten_url, all_slugs)

        return {'msg': 'Url obtida com sucesso', 'original_url': original}

    except Exception as e:
        session.rollback()
        return {'msg': 'Houve um erro ao recuperar url', 'error': str(e)} 


import logging

@app.get("/redirect")
async def redirect_to_original(user_slug: str, session: sessionDP, request: Request):
    try:
        # 1. Buscar slug da BD
        slug = session.exec(select(URLS).where(URLS.slug == user_slug)).first()
        if not slug:
            return {"msg": "URL não encontrada ou expirada"}


        ua_string = request.headers.get("user-agent") or request.headers.get("User-Agent") or ""
        logging.info(f"User-Agent recebido: {ua_string}")

        user_agent = parse(ua_string) if ua_string else None

        device = "Desconhecido"
        os = "Desconhecido"
        browser = "Desconhecido"

        if user_agent:
            device = "Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "PC"
            os = user_agent.os.family
            browser = user_agent.browser.family

    
        client_ip_address = request.client.host or "0.0.0.0"
        logging.info(f"IP do cliente: {client_ip_address}")

        try:
            client_address = get_client_data(client_ip_address)
            city = client_address.get("location", {}).get("city", "Desconhecida")
            country = client_address.get("location", {}).get("country", "Desconhecido")
        except Exception as e:
            logging.error(f"Erro a obter geolocalização: {e}")
            city, country = "Desconhecida", "Desconhecido"

        new_click = Clicks(
            shortned_url_id=slug.id,
            ip_address=client_ip_address,
            city=city,
            country=country,
            device=device,
        )

        session.add(new_click)
        session.commit()

        logging.info(f"Redirect para {slug.original_url}")
        return RedirectResponse(slug.original_url)

    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        return {"msg": f"Algo correu mal: {str(e)}"}


        
    except Exception as e:
        print("Erro: ", str(e))
        return {'msg': 'Algo correu mal'}
    
        
@app.get('/metrics')
async def get_metrics(session : sessionDP):
   
    try:

        total_shortned_urls = session.exec(select(func.count(URLS.slug))).all() or []
        total_clicks = session.exec(select(func.count(Clicks.id)))
        unique_users_by_ip = session.exec(select(func.count(distinct(Clicks.ip_address)))).all()

        return {'clicks': get_metric_number(total_clicks),
                'url_shortned': get_metric_number(total_shortned_urls),
                'unique_users': get_metric_number(unique_users_by_ip)}

    except Exception as e:
        return {'msg': 'Houve um erro', 'erro': str(e)}
      

@app.post('/create')
async def create_user(user : RegisterData, session : sessionDP):

    try:
        email = user.email
        nome = user.nome
        password = user.password_hash

        if not all([email,nome, password]):
            return {'msg': 'Todos os campos são obrigatórios',}
        
        exist_user = session.exec(select(Users).where(Users.email == email)).first()
        print("Usuário na base de dados: ", exist_user)

        if exist_user:
            return {'msg': 'Esse utilizador já foi registrado', 'status_code': 409}
        
        new_user = Users()
        new_user.nome = nome
        new_user.email = email
        new_user.hash_password = password

        session.add(new_user)
        session.commit()
        return {'msg': 'Utilizador criado com sucesso', 'status_code': 201}

    except Exception as e:
        session.rollback()
        print('Houve um erro: ', e)
        return {'msg': 'Erro ao criar usuário'}


@app.post('/login')
async def login(user: LoginData, session : sessionDP):

    # Fluxo de funcionamento:
    # API recebe os dados do usuário
    # Valida os dados, verifica se de facto existe um usuário com os dados recebidos
    # Se não existir retorna uma messagem de erro code 404 not found
    # Se existir pega nos dados (id, nome, email e expiração do token) gera um token e envia para o frontend
    # O frontend recebe o token e envia novamente para o backend para a rota de redirecionamento para a dashbord e autentica o user

    try:
        email = user.email
        password = user.password_hash

        _user = Users()
        exist_user = session.exec(select(Users).where(Users.email == email)).first()

        if not exist_user or not _user.check_password(password, exist_user.password_hash):
            return {'msg': 'Email e palavra-passe inválidos', 'status_code': 401}
        
        timestamp_exp = create_exp_timestamp()

        payload = {'id': exist_user.id, 'nome': exist_user.nome, 'email': exist_user.email, 'exp': timestamp_exp}
        token = create_token(payload)

        return {'msg': 'Utilizador autenticado com sucesso', 'status_code': 201, 'token': token}
        
  
    except Exception as e:
        print("Houve um erro", str(e))
        return {'msg': 'Erro ao logar user'}



@app.get('/dashboard')
@token_required
async def dashboard(request: Request, session: sessionDP, page: int):
    user_id = request.state.user_id
    per_page = 3
    offset = (page - 1) * per_page

    data = session.exec(select(Users).where(Users.id == user_id)).first()

    total_urls = get_total_urls(session, user_id) 
    total_clicks = get_total_clicks(session, user_id)
    unique_clicks = get_unique_clicks(session, user_id)
    clicks_last_7d = get_7d_clicks(session, user_id)
    unique_clicks_7d = get_unique_clicks_7d(session, user_id)
    clicks_by_devices = get_clicks_by_devices(session, user_id)
    clicks_by_cities = get_clicks_by_cities(session, user_id)
 

    urls_page = get_url_pages(session, user_id, offset)

    urls_serialized = serialize_urls(urls_page) or []
    serialized_7d = serialize_7d_clicks(clicks_last_7d) or []
    serialized_unique_7d = serialize_7d_clicks(unique_clicks_7d) or []
    serialized_device = serialize_device(clicks_by_devices) or []
    city_serialized = serialize_cities(clicks_by_cities) or []

    
    return {
        'user_data': data,
        'all_urls': {
            'urls': urls_serialized,
            'total_urls': total_urls,
            'page': page,
            'total_pages': ceil(total_urls / per_page),
            'seven_days_clicks': serialized_7d,
            'unique_7d_clicks': serialized_unique_7d,
            'devices': serialized_device,
            'cities': city_serialized      
        },
        'header': {
            'total_clicks': total_clicks,
            'unique_clicks': unique_clicks,
        },
        'status_code': 201
    }

@app.delete('/delete_url')
async def delete_url(id : int, session : sessionDP):

    try:
       session.exec(delete(URLS).where(URLS.id == id))
       session.commit()

       return {'msg': 'URL removida com sucesso', 'status_code': 201}

    except Exception as e:
        session.rollback()
        print('Houve um erro ao eliminar url', str(e))
        return {'erro': 'Não foi possível remover a url' , 'error': str(e)}
