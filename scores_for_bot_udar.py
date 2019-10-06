import change_data_for_bot_udar as ch_d

data = ch_d.data


def add_defeats(user, score_num):
    if user in data['score']:
        score_d = data['score'][user]['defeats']
        score_d += score_num
        ch_d.change_data('score', user, score_d, 'defeats')
    else:
        ch_d.change_data('score', user, {'victories': 0, 'defeats': 0})
        score_d = data['score'][user]['defeats']
        score_d += score_num
        ch_d.change_data('score', user, score_d, 'defeats')


def add_victories(user, score_num):
    if user in data['score']:
        score_d = data['score'][user]['victories']
        score_d += score_num
        ch_d.change_data('score', user, score_d, 'victories')
    else:
        ch_d.change_data('score', user, {'victories': 0, 'defeats': 0})
        score_d = data['score'][user]['victories']
        score_d += score_num
        ch_d.change_data('score', user, score_d, 'victories')
