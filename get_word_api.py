import change_data_for_bot_udar as ch_d
import requests

data = ch_d.data
api_url = 'https://stepik.akentev.com/api/stress'


def get_response(letter):
    if letter == 'любая':
        return requests.get(api_url).json()
    else:
        return requests.get(
                api_url,
                params={
                    'first_letter': letter,
                }
                ).json()
