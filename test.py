from parsel import Selector
from scrapfly import ScrapeConfig, ScrapflyClient
from urllib.parse import quote

# import scrapfly

scrapfly = ScrapflyClient("scp-live-b8a1a7829f974c8f9455986a4dc04b5a")

def scrape_search(query: str, page=1, country="US"):
    """scrape search results for a given keyword"""
    # retrieve the SERP
    url = f"https://www.google.com/search?hl=en&q={quote(query)}" + (f"&start={10*(page-1)}" if page > 1 else "")
    print(f"{url=}")
    print(f"scraping {query=} {page=}")
    result = scrapfly.scrape(ScrapeConfig(url, asp=True, proxy_pool='public_datacenter_pool'))
    
    # with open('output.html', 'w', encoding='utf-8') as f:
    #     f.write(result.content)
    results  = parse_search_results(result.selector)
    return results


def parse_search_results(selector: Selector):
    """parse search results from google search page"""
    results = []
    return selector.css(".related-question-pair span::text").getall()
print(scrape_search('laptop'))



result = scrapfly.scrape(ScrapeConfig(
    "https://www.google.com/search?hl=en&q=laptop",
    # enable browser rendering
    wait_for_selector="div[class='.related-question-pair']",
    render_js=True,
    js_scenario=[
        # wait to load
        # click search button
        {"click": {"selector": "div[class='.related-question-pair'][4]"}},
        
        {"wait_for_navigation": {"timeout": 0}}

    ]
))
a = result.selector.css(".related-question-pair span::text").getall()
for i in a:
    print(i)
# print(a)