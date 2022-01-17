import requests
import operator

CLIENT_ID = "64c86150da1760e0ec09e4aecafcead0"

ops = {
    'Before':operator.le,
    'After':operator.ge,
    'During':operator.eq,
    '<':operator.le,
    '>':operator.ge,
    '=':operator.eq
}

def generate_link(anime:dict)->str:
    return f'https://myanimelist.net/anime/{anime["node"]["id"]}'

def generate_image(anime:dict)->str:
    return anime["node"]["main_picture"]["medium"]



def verify_account(username: str) -> int:
    # Verify if inputted account is valid
    # return 0 on success, 1 on error
    global CLIENT_ID
    try:
        url = f'https://api.myanimelist.net/v2/users/{username}/animelist'
        response = requests.get(url, headers={'X-MAL-CLIENT-ID': CLIENT_ID})
        response.raise_for_status()
        response.close()
    except requests.exceptions.HTTPError:
        return 1
    return 0

def generate_ptw(username: str) -> dict:
    url = f'https://api.myanimelist.net/v2/users/{username}/animelist?status=plan_to_watch&limit=1000&sort=anime_start_date&fields=start_date,mean,genres'
    response = requests.get(url, headers={'X-MAL-CLIENT-ID': CLIENT_ID})
    response.raise_for_status()
    ptw = response.json()
    response.close()
    return ptw

def sort_ptw(ptw: dict) -> dict:
    # Sort ptw by score
    ptw = sorted(ptw['data'], key=lambda x: x['node']['mean'] if 'mean' in x['node'] else 0, reverse=True)

    for index in range(len(ptw)):
        # Changing format of 'genres'
        ptw[index]['node']['genres'] = {x['name'] for x in ptw[index]['node']['genres']}
        if 'start_date' in ptw[index]['node']:
            ptw[index]['node']['start_date'] = ptw[index]['node']['start_date'][0:4]
    return ptw

def get_suggestion(ptw: dict, time: str, genres = {}) -> dict:
    global ops
    time_check = False
    genre_check = False
    if time != "Any":
        time_check = True
        time = time.split()
    if len(genres) > 0:
        genre_check = True

    for anime in ptw:
        if not time_check and not genre_check:
            return anime
        else:
            success_time = False
            success_genre = False
            if time_check and 'start_date' in anime['node'] and ops[time[0]](anime['node']['start_date'], time[1]):
                success_time = True
            if genre_check and 'genres' in anime['node'] and all([1 if x in anime['node']['genres'] else 0 for x in anime['node']['genres'] ]):
                success_genre = True
            if time_check == success_time and success_genre == genre_check:
                return anime
    return {}