from config import ebay_token
from requests_cache import CachedSession


def ebay_api_call(query: str, limit: int):
    # Replace spaces in query with '+' for url
    editedQuery = query.replace(" ", "+")
    # Construct url string with query and limit input
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={editedQuery}&limit={limit}"
    # Construct headers with ebay application token and set desired eBay marketplace location
    headers = {
        "Authorization": f"Bearer {ebay_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }

    # Create Session class with caching, expires after five minutes
    session = CachedSession('http_cache', backend='sqlite', expire_after=300)

    # Send request and store response
    response = session.get(url, headers=headers)
    return response
