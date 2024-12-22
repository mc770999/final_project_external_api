import requests

def fetch_articles(api_key, keyword, articles_page=1, articles_count=100):
    try:
        url = "https://eventregistry.org/api/v1/article/getArticles"
        payload = {
            "action": "getArticles",
            "keyword": keyword,
            "ignoreSourceGroupUri": "paywall/paywalled_sources",
            "articlesPage": articles_page,
            "articlesCount": articles_count,
            "articlesSortBy": "socialScore",
            "articlesSortByAsc": False,
            "dataType": ["news", "pr"],
            "forceMaxDataTimeWindow": 31,
            "resultType": "articles",
            "apiKey": api_key
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(str(e))
        return None


