from datetime import datetime, timedelta
import re
from elasticsearch.helpers import bulk

def clean_views(views_str: str):
    views_str= views_str.replace('k', '000').replace('M', '000000')
    views_int= int(re.sub(r'[^\d]', '', views_str))
    formatted_views = '{:,.0f}'.format(views_int).replace(',', ' ')

    return formatted_views

def clean_date(date_str: str):
    today = datetime.today()
    
    if any(unit in date_str for unit in ["jour", "heure", "minute", "seconde"]):
        days = int(re.search(r'(\d+)', date_str).group(1))
        return (today - timedelta(days=days)).date()
    elif "hier" in date_str:
        return (today - timedelta(days=1)).date()
    elif "semaine" in date_str:
        weeks = int(re.search(r'(\d+)', date_str).group(1))
        return (today - timedelta(weeks=weeks)).date()
    elif "mois" in date_str:
        months = int(re.search(r'(\d+)', date_str).group(1))
        return (today - timedelta(days=months * 30)).date()
    elif "an" in date_str:
        years = int(re.search(r'(\d+)', date_str).group(1))
        return (today - timedelta(days=years * 365)).date()
    else:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

def process_data(data):
    data["Views"]= data["Views"].apply(clean_views)
    data["Date"]= data["Date"].apply(clean_date)
    return data

def generate_data(data):
    for docu in data:
        yield {
            "_index": "yt_twitch",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

def insert_data(es,data):
    if es.indices.exists(index='yt_twitch')==True:
        es.indices.delete(index='yt_twitch')
        bulk(es, generate_data(data))
    else :
        bulk(es, generate_data(data))