import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd
import traceback


def getRanks():
    # initialize data frame
    df = pd.DataFrame()
    url = 'https://www.streetfighter.com/6/buckler/ranking/master'
    headers = {
        'Cookie': 'cookie information goes here',
        'User-Agent': 'user-agent goes here',
        'Host': 'www.streetfighter.com',
        'referer': url,

    }

    # starting page number
    page_no = 1

    # set max pages until later
    max_pages = 200

    # master's rank is 36
    league_rank = 36
    while page_no <= max_pages:
        params = {
            'page': page_no
        }

        r = requests.get(f'{url}', params=params, headers=headers)

        r = r.text

        soup = BeautifulSoup(r, 'html.parser')

        try:
            # gets total number of masters players
            player_count = int(soup.find('span', {'class': 'ranking_ranking_now__last__TghLM'}).text.replace('/ ', ''))
            # since 20 players per page we can divide by 20 get # numer of pages we need to interate through
            max_pages = player_count / 20
        except Exception:
            traceback.print_exc()
            print(f' failed on {page_no}')
            df.to_csv(f'failure_{page_no}.csv', index=False)
            page_no = page_no + 1
            continue

        script = soup.find('script', {'id': '__NEXT__DATA__'})
        if script is not None:
            try:
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

            except Exception:
                traceback.print_exc()
                print(f' failed on {page_no}')
                df.to_csv(f'failure_{page_no}.csv', index=False)
                page_no = page_no + 1
                continue
        df.to_csv(f'finished_ranking.csv', index=False)


if __name__ == "__main__":
    getRanks()
