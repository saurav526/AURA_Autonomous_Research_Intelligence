# tool calling for web search using DuckDuckGo's HTML interface
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse

async def web_search(query: str, limit: int = 8):
    url = "https://html.duckduckgo.com/html/?q=" + quote(query)
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for item in soup.select(".result")[:limit]:
        anchor = item.select_one(".result__a")
        snippet = item.select_one(".result__snippet")
        if not anchor:
            continue

        href = anchor.get("href", "")
        results.append({
            "title": anchor.get_text(" ", strip=True),
            "url": href,
            "snippet": snippet.get_text(" ", strip=True) if snippet else "",
            "domain": urlparse(href).netloc
        })

    return results
