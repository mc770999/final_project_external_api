from typing import List, Dict
from external_api.api_request.groq_api import post_groq_api
from external_api.utils.json_util import extract_data_flat

def try_groq(art):
    try:
        groq = post_groq_api(art)
        return groq
    except Exception as e:
        print(e)
        return {}

def add_groq_and_normal_data(articles):
    articles_with_groq = [extract_data_flat({**art, "groq": try_groq(art)}) for art in articles["articles"]["results"]]
    return articles_with_groq

