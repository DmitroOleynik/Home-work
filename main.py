from fastapi import FastAPI, Query, HTTPException
from bs4 import BeautifulSoup
import httpx


app = FastAPI()


async def get_html(url):
    """
    Make a http request for url and return soup(BeautifulSoup(response_url, 'html.parser') - Tools for working with html
    :param url:
    :return:
    """
    async with httpx.AsyncClient() as async_client:
        response_url = await async_client.get(url)
        response_text = response_url.text

    soup = BeautifulSoup(response_text, 'html.parser')
    return soup


async def parse_data(url):
    try:
        soup = await get_html(url)
        data = soup.find('table', class_='infobox vevent')
        tags_tr = data.find_all('tr')
        response = {}
        if tags_tr:
            for i in tags_tr:
                tag_th = i.find('th')
                tag_td = i.find('td')
                if tag_td and tag_th:
                    tag_th_text = tag_th.text
                    tag_td_text = tag_td.text
                    response.update({tag_th_text: tag_td_text})
                    if tag_th_text == 'Website':
                        break
        return response
    except Exception:
        raise HTTPException(status_code=404, detail='Sorry, scraper can`t scraping site')


@app.get('/')
async def main_endpoint(url: str = Query(min_length=9)):
    lst_url = url.split(',')
    data = []
    for i in lst_url:
        data.append(await parse_data(i))
    return data