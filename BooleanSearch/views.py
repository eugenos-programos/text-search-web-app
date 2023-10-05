import html2text
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect

from BooleanSearch.models import Document, Search
import trafilatura


def index(request):
    return render(request, 'index.html')


def help(request):
    return render(request, 'help.html')


def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        new_search, _ = Search.objects.update_or_create(query=query)
        results = new_search.search(new_search.query)
        return render(request, 'search_results.html', {'results': results, 'query': query})


def search_results(request):
    return render(request, 'search_results.html')


def refresh_database(request):
    Document.objects.all().delete()
    print('here')

    url_list = [
        'https://arstechnica.com/gadgets/2023/09/raspberry-pi-5-available-for-preorder-is-faster-and-has-a-custom-i-o-chip/?comments=1',
        'https://arstechnica.com/gadgets/2023/09/macos-14-sonoma-the-ars-technica-review/',
        'https://arstechnica.com/gadgets/2023/09/raspberry-pi-5-available-for-preorder-is-faster-and-has-a-custom-i-o-chip/',
        'https://arstechnica.com/science/2023/09/ai-is-getting-better-at-hurricane-forecasting/',
        'https://arstechnica.com/health/2023/09/big-dairy-still-sour-over-plant-based-milk-labels-tries-to-outlaw-them/',
        'https://arstechnica.com/information-technology/2023/09/jony-ive-and-openais-altman-reportedly-collaborating-on-mysterious-ai-device/',
        'https://arstechnica.com/security/2023/09/china-state-hackers-are-camping-out-in-cisco-routers-us-and-japan-warn/',
        'https://arstechnica.com/tech-policy/2023/09/google-deal-may-have-kept-apple-from-building-search-engine-exec-says/',
        'https://arstechnica.com/gaming/2023/09/kerbal-space-program-2-has-a-big-pre-launch-issue-windows-registry-stuffing/',
        'https://arstechnica.com/google/2023/09/smartphone-sales-down-22-percent-in-q2-the-worst-performance-in-a-decade/',
        'https://arstechnica.com/gaming/2023/09/fifa-23-delisted-from-digital-stores-as-ea-sports-fc-24-launches/',
        'https://arstechnica.com/information-technology/2023/09/spotify-tests-using-ai-to-automatically-clone-and-translate-podcast-voices/',
        'https://arstechnica.com/tech-policy/2023/09/google-fights-to-hide-embarrassing-but-not-confidential-doj-trial-exhibit/',
        'https://arstechnica.com/health/2023/09/how-climate-change-could-make-fungal-diseases-worse/'
    ]
    for url in url_list:  # category all articles on habr has 50 pages


        article_source_page = requests.get(url)
        if article_source_page.status_code != 200:
            print('Unable to get article', url)
            continue

        text = trafilatura.fetch_url(url)

        if text is not None and text != 'None\n\n\n':
                    Document.objects.update_or_create(title=url.split('/')[-2], url=url, text=text, snippet='')
                    print('Got article: Title:', url.split('/')[-2], '. Url: ', url)

    return render(request, 'index.html')
