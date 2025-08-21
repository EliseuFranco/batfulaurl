from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete, update, func, distinct
from typing import Annotated, Optional
from urllib.parse import urlparse
from random import choice
from string import ascii_letters , digits
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from utils import get_client_data, create_token, create_exp_timestamp, token_required, get_year_month_day
from models.urls_model import URLS
from models.clicks_model import Clicks
from models.user_model import Users




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

db_name = 'url_db.db'
database_url = f'sqlite:///{db_name}'

connect_args = {"check_same_thread": False}
engine = create_engine(database_url, connect_args=connect_args)


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
    'http://localhost:5173'
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
            user_d = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')
            user_id = user_d['id']

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



@app.get('/redirect')
async def redirect_to_original(user_slug : str, session : sessionDP, request: Request):

    try:
        slug = session.exec(select(URLS).where(URLS.slug == user_slug)).first()

        if not slug:
            return {'msg': 'URL não encontrada ou expirada'}
        
        client_ip_address = request.client.host or '0.0.0.0'

        client_address = get_client_data(client_ip_address)
        city = client_address['location']['city'] 
        country = client_address['location']['country']

            
        new_click = Clicks(shortned_url_id=slug.id,
                        ip_address=client_ip_address,
                        city=city,
                        country=country)
        
        session.add(new_click)
        session.commit()

        return RedirectResponse(slug.original_url)

        
    except Exception as e:
        print("Erro: ", str(e))
        return {'msg': 'Algo correu mal'}
    
        
@app.get('/metrics')
async def get_metrics(session : sessionDP):
    from utils import get_metric_number

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
async def dashboard(request: Request, session : sessionDP):
    
    try:
        user_id = request.state.user_id
        data = session.exec(select(Users).where(Users.id == user_id)).first()
        urls = session.exec(select(URLS).where(URLS.user_id == user_id)).all()

        all_URLS_serialized = [{'original_url': url.original_url, 'data': get_year_month_day(url.created_at), 'slug': url.slug,
                                 'shortened_url': generate_shorten_url(slug=url.slug, url=url.original_url)} for url in urls]
        

        statement = (
            select(URLS.slug, func.count(Clicks.id))
            .join(URLS, Clicks.shortned_url_id == URLS.id)
            .group_by(Clicks.shortned_url_id)
        )

        results = session.exec(statement).all()
        total_clicks = session.exec(select(func.count(Clicks.id)).join(URLS, URLS.id == Clicks.shortned_url_id)
                                    .where(URLS.user_id == user_id)).one()

        total_by_country = session.exec(
                                        select(func.count(Clicks.country))
                                        .join(URLS, URLS.id == Clicks.shortned_url_id)
                                        .where(URLS.user_id == user_id)).one()

        total_unique_clicks = session.exec(select(func.count(distinct(Clicks.ip_address)))
                                           .join(URLS, URLS.user_id == user_id)
                                           .where(URLS.id == user_id)).one()

    
        header = {'total_click': total_clicks, 'unique_clicks': total_unique_clicks, 'total_click_country': total_by_country}

        return {'msg': 'Rota de redirecionamento',
                'user_data': data,
                'all_urls': all_URLS_serialized,
                'header': header}
       
    except Exception as e:
        return
    

    