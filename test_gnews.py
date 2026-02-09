from services.gnews_fetcher import GNewsFetcher

API_KEY = "69872e57ea29b49a4a49dbae78677d5e"

fetcher = GNewsFetcher(API_KEY)

articles = fetcher.fetch_articles(
    query="military",
    max_records=3
)

print("Articles fetched:", len(articles))

if articles:
    print("Sample keys:", articles[0].keys())
    print("Sample content preview:")
    print(articles[0].get("content")[:300])
