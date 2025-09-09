from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete, update, func, distinct, and_, extract
from models.clicks_model import Clicks
from models.urls_model import URLS
from models.user_model import Users
from .utils import get_year_month_day
from urllib.parse import urlparse
from datetime import datetime, timedelta


def generate_shorten_url(slug, url):

    schema = urlparse(url).scheme
    shorten_url = f'{schema}://urlcurta.com/{slug}'
    return shorten_url


def get_total_urls(session, user_id):
    return session.exec(
        select(func.count(URLS.id)).where(URLS.user_id == user_id)
    ).one()


def get_total_clicks(session, user_id):
    return session.exec(
        select(func.count(Clicks.id))
        .join(URLS, URLS.id == Clicks.shortned_url_id)
        .where(URLS.user_id == user_id)
    ).one()


def get_unique_clicks(session, user_id):
    return session.exec(
        select(func.count(distinct(Clicks.ip_address)))
        .join(URLS, URLS.id == Clicks.shortned_url_id)
        .where(URLS.user_id == user_id)
    ).one()



def serialize_url(url):
    return {
        'original_url': url.original_url,
        'data': get_year_month_day(url.created_at),
        'slug': url.slug,
        'shortened_url': generate_shorten_url(slug=url.slug, url=url.original_url)
    }


def get_7d_clicks(session, user_id):

    today = datetime.today().date()
    seven_days_ago = today - timedelta(days=7)
    
    return session.exec(
        select(func.date(Clicks.clicked_at),func.count(func.date(Clicks.clicked_at))
               .label('total_clicks'))
               .join(URLS, URLS.id == Clicks.shortned_url_id)
               .where(
                   and_(URLS.user_id == user_id, func.date(Clicks.clicked_at) >= seven_days_ago)
               )
               .group_by(func.date(Clicks.clicked_at))

    ).all()

def get_url_pages(session, user_id, offset,per_page=3):

    return session.exec(
    select(
        URLS.id,
        URLS.slug,
        func.date(URLS.created_at).label('created_date'),
        URLS.original_url,
        func.count(distinct(Clicks.ip_address)).label('unique_clicks'),
        func.count(Clicks.id).label('total_clicks')
        )
        .join(Clicks, URLS.id == Clicks.shortned_url_id, isouter=True) 
        .where(URLS.user_id == user_id)
        .group_by(URLS.slug, URLS.created_at, URLS.original_url, URLS.id)
        .order_by(URLS.created_at.desc())
        .limit(per_page)
        .offset(offset)
    ).all()

def get_unique_clicks_7d(session, user_id):
    today = datetime.today().date()
    seven_days_ago = today - timedelta(days=7)
    
    query = (
        select(
            func.date(Clicks.clicked_at).label("date"),
            func.count(distinct(Clicks.ip_address)).label("unique_clicks")
        )
        .join(URLS, Clicks.shortned_url_id == URLS.id)
        .where(
            and_(
                URLS.user_id == user_id,
                func.date(Clicks.clicked_at) >= seven_days_ago
            )
        )
        .group_by(func.date(Clicks.clicked_at))
        .order_by(func.date(Clicks.clicked_at))
    )

    return session.exec(query).all()

def get_clicks_by_country(session, user_id):
    pass


def get_clicks_by_devices(session, user_id):
    return session.exec(select(Clicks.device, func.count(Clicks.device).label('clicks_per_device'))
                               .join(URLS, URLS.id == Clicks.shortned_url_id)
                               .where(URLS.user_id == user_id)
                               .group_by(Clicks.device)).all()


def get_clicks_by_cities(session, user_id):
    return session.exec(
        select(Clicks.city,
                extract("hour", Clicks.clicked_at)
                ,func.count(Clicks.id).label('total_clicks'),
                func.count(distinct(Clicks.city)))
                .join(URLS, URLS.id == Clicks.shortned_url_id)
                .where(URLS.user_id == user_id).
                group_by(extract('hour', Clicks.clicked_at), Clicks.city)
    ).all()
