import json

MAIN_STATE = 'main'
ASK_STATE = 'ask_state'
WORD_STATE = 'word_state'

way_file = 'for_bot_udar_3.4.json'

try:
    data = json.load(
        open(
            way_file,
            'r',
            encoding='utf-8'
        )
    )
    # encording - это юникод, чтобы видеть все русскими буквами
except FileNotFoundError:
    data = {
        'users': {},
        'states': {},
        'score': {},
        'user_word': {},
        'user_let': {},
        MAIN_STATE: {},
        ASK_STATE: {},
        WORD_STATE: {},
    }


def change_data(key, user_id, value, score_='a'):
    if score_ != 'a':
        data[key][user_id][score_] = value
    else:
        data[key][user_id] = value
    json.dump(
        data,
        open(
            way_file,
            'w',
            encoding='utf-8'
        ),
        indent=2,
        ensure_ascii=False
        # чтобы русские символы латиницей не передавались. ДЛя http юникоды не подходят
    )
