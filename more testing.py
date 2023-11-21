import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd
import math
import traceback

df = pd.DataFrame()
url = 'https://www.streetfighter.com/6/buckler/ranking/master'
headers = {
    'Cookie': 'buckler_r_id=b2930a74-ab86-48e7-b4a6-403a472fc442; buckler_praise_date=1700179834903; '
              'buckler_id=m7niM9Mnoo8GCKIPp8vOe9BCdy-9GC4wpdXz63dIDsZWglCjUS3ATvk7o6YNOUPT',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Host': 'www.streetfighter.com',
    'referer': url,

}
#initialize max pages
max_pages = 200

# starting page number
page_no = 1


# master's rank is 36
league_rank = 36

while page_no <= max_pages:
    params = {
        'page': page_no
    }
    r = requests.get(f'{url}', params=params, headers=headers)

    r = r.text
    soup = BeautifulSoup(r, 'html.parser')

    player_count = int(soup.find('span', {'class': 'ranking_ranking_now__last__TghLM'}).text.replace('/ ', ''))
    # since 20 players per page we can divide by 20 get # numer of pages we need to interate through
    max_pages = math.ceil(player_count / 20)

    print(max_pages)
    print(player_count)

    script = soup.find('script', {'id': '__NEXT_DATA__'})

    j = json.loads(script.get_text())

    page_data = j['props']['pageProps']['master_rating_ranking']['ranking_fighter_list']
    df = pd.concat([df, pd.json_normalize(page_data)], ignore_index=True)
    df = df.loc[:, ['fighter_banner_info.personal_info.fighter_id',
                    'fighter_banner_info.personal_info.platform_name',
                    'character_name',
                    'league_point',
                    'league_rank',
                    'rating',
                    'fighter_banner_info.home_name'
                    ]]
    print(f'Page {page_no} finished')
    page_no += 1


df.to_csv(f'finished_ranking_csv',index=False)